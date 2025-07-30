import io
import datetime
import logging

from typing import Sequence, Optional, Mapping, Tuple, NoReturn

from pyomo.common.timing import HierarchicalTimer
from pyomo.core.base.constraint import Constraint
from pyomo.core.base.var import Var, VarData
from pyomo.core.base.block import BlockData
from pyomo.core.expr.numvalue import value
from pyomo.core.kernel.objective import minimize, maximize
from pyomo.core.staleflag import StaleFlagManager

from pyomo.common.config import document_kwargs_from_configdict, ConfigValue, Bool
from pyomo.common.dependencies import attempt_import
from pyomo.common.errors import ApplicationError, PyomoException
from pyomo.common.tee import TeeStream, capture_output

from pyomo.repn import generate_standard_repn

from pyomo.contrib.solver.common.base import SolverBase, Availability
from pyomo.contrib.solver.common.config import BranchAndBoundConfig
from pyomo.contrib.solver.common.factory import SolverFactory
from pyomo.contrib.solver.common.results import (
    Results,
    SolutionStatus,
    TerminationCondition,
)
from pyomo.contrib.solver.common.solution_loader import SolutionLoaderBase
from pyomo.contrib.solver.common.util import (
    NoFeasibleSolutionError,
    NoOptimalSolutionError,
    get_objective,
)

logger = logging.getLogger(__name__)

ortools, ortools_available = attempt_import('ortools')

if ortools_available:
    from ortools.sat.python import cp_model
    from ortools.init.python.init import OrToolsVersion


class IncompatibleModelError(PyomoException):
    def __init__(self, message=None):
        if message is None:
            message = (
                'Model is not compatible with the chosen solver.'
                'Please check the model and solver.'
            )

        super().__init__(message)


class CpsatConfig(BranchAndBoundConfig):
    """ """

    def __init__(
        self,
        description=None,
        doc=None,
        implicit=False,
        implicit_domain=None,
        visibility=0,
    ):
        super().__init__(
            description=description,
            doc=doc,
            implicit=implicit,
            implicit_domain=implicit_domain,
            visibility=visibility,
        )

        self.find_infeasible_subsystem: bool = self.declare(
            'find_infeasible_subsystem',
            ConfigValue(
                domain=Bool,
                default=False,
                description='If True, finds a (potentially smaller) subsystem '
                'of infeasible constraints, assuming the model is infeasible. '
                'When True, the values of the keyword arguments '
                'raise_exception_on_nonoptimal_result and load_solutions are ignored.',
            ),
        )


class CpsatSolutionLoader(SolutionLoaderBase):
    """
    Pyomo solution loader for CP-SAT
    """

    def __init__(
        self,
        cpsat_solver: cp_model.CpSolver,
        pyomo_vars: Sequence[VarData],
        pyomo_cpsat_map=Mapping[int, cp_model.IntVar],
    ):
        self.cpsat_solver = cpsat_solver
        self.pyomo_vars = pyomo_vars
        self.pyomo_cpsat_map = pyomo_cpsat_map

    def load_vars(self, vars_to_load: Optional[Sequence[VarData]] = None) -> NoReturn:
        if vars_to_load is None:
            vars_to_load = self.pyomo_vars

        for v in vars_to_load:
            cpsat_var = self.pyomo_cpsat_map[id(v)]
            cpsat_val = self.cpsat_solver.value(cpsat_var)
            v.set_value(cpsat_val, skip_validation=True)

        StaleFlagManager.mark_all_as_stale(delayed=True)


@SolverFactory.register(
    name='cpsat', legacy_name='cpsat', doc='Direct interface to CP-SAT'
)
class Cpsat(SolverBase):
    """
    Pyomo direct solver interface for CP-SAT
    """

    CONFIG = CpsatConfig()

    def __init__(self, **kwds) -> None:
        super().__init__(**kwds)

        self._config = None

        self._solver_model = None
        self._solver_solver = None

        self._model = None

        self._vars = []
        self._pyomo_var_to_solver_var_map = {}

    def available(self) -> Availability:
        if ortools_available:
            return Availability.FullLicense
        else:
            return Availability.NotFound

    def version(self) -> Tuple:
        return (
            OrToolsVersion.major_number(),
            OrToolsVersion.minor_number(),
            OrToolsVersion.patch_number(),
        )

    @document_kwargs_from_configdict(CONFIG)
    def solve(self, model: BlockData, **kwargs) -> Results:
        """
        Solve a Pyomo model with CP-SAT.

        Parameters
        ----------
        model: BlockData
            The Pyomo model to be solved
        **kwargs
            Additional keyword arguments (including solver_options - passthrough
            options; delivered directly to the solver (with no validation))

        Returns
        -------
        results: :class:`Results<pyomo.contrib.solver.common.results.Results>`
            A results object

        Notes on kwargs
        ---------------
        working_dir
            Is ignored - no files are generated by this solver interface.
        symbolic_solver_labels
            Is ignored - names of Pyomo components are always passed to CP-SAT.
        """
        if not self.available():
            c = self.__class__
            raise ApplicationError(
                f'Solver {c.__module__}.{c.__qualname__} is not available '
                f'({self.available()}).'
            )

        start_timestamp = datetime.datetime.now(datetime.timezone.utc)

        self._config = self.config(value=kwargs, preserve_implicit=True)

        if self._config.timer is None:
            self._config.timer = HierarchicalTimer()

        timer = self._config.timer

        StaleFlagManager.mark_all_as_stale()

        self._model = model

        self._solver_model = cp_model.CpModel()
        self._solver_solver = cp_model.CpSolver()

        # CP-SAT options: google/or-tools/ortools/sat/sat_parameters.proto
        if self._config.tee:
            self._solver_solver.parameters.log_search_progress = True

        if self._config.threads is not None:
            self._solver_solver.parameters.num_workers = self._config.threads

        if self._config.time_limit is not None:
            self._solver_solver.parameters.max_time_in_seconds = self._config.time_limit

        if self._config.rel_gap is not None:
            self._solver_solver.parameters.relative_gap_limit = self._config.rel_gap

        if self._config.abs_gap is not None:
            self._solver_solver.parameters.absolute_gap_limit = self._config.abs_gap

        for key, opt in self._config.solver_options.items():
            pyomo_equivalent_keys = {
                'num_workers': 'threads',
                'max_time_in_seconds': 'time_limit',
                'relative_gap_limit': 'rel_gap',
                'absolute_gap_limit': 'abs_gap',
            }

            eq_key = pyomo_equivalent_keys.get(key, None)

            if eq_key is not None:
                if getattr(self._config, eq_key) is not None:
                    raise KeyError(
                        f'CP-SAT solver option {key} can be specified as Pyomo option {eq_key}.'
                    )

            repeating_keys = [
                'RestartAlgorithm',
                'subsolvers',
                'extra_subsolvers',
                'ignore_subsolvers',
            ]

            if key in repeating_keys:
                try:
                    getattr(self._solver_solver.parameters, key).extend(opt)
                except TypeError:
                    raise

            else:
                try:
                    setattr(self._solver_solver.parameters, key, opt)
                except TypeError:
                    raise

        timer.start('add_variables')
        self._add_variables()
        timer.stop('add_variables')

        timer.start('add_constraints')
        self._add_constraints()
        timer.stop('add_constraints')

        timer.start('set_objective')
        self._set_objective()
        timer.stop('set_objective')

        ostreams = [io.StringIO()] + self._config.tee
        with capture_output(output=TeeStream(*ostreams), capture_fd=True):
            timer.start('optimize')
            self._solver_status = self._solver_solver.solve(self._solver_model)
            timer.stop('optimize')

        timer.start('load_results')
        results = self._load_results()
        timer.stop('load_results')

        if self._config.find_infeasible_subsystem:
            self._output_infeasible_subsystem()

        end_timestamp = datetime.datetime.now(datetime.timezone.utc)
        results.timing_info.start_timestamp = start_timestamp
        results.timing_info.wall_time = (
            end_timestamp - start_timestamp
        ).total_seconds()
        results.timing_info.timer = timer

        return results

    def _cpsat_bounds_from_var(self, var):
        if var.is_fixed():
            val = var.value
            return val, val

        if var.has_lb():
            lb = value(var.lb)
        else:
            raise IncompatibleModelError(
                f'Variable ({var.name}) has no lower bound. '
                'CP-SAT cannot solve models with variables without lower bounds.'
            )

        if var.has_ub():
            ub = value(var.ub)
        else:
            raise IncompatibleModelError(
                f'Variable ({var.name}) has no upper bound. '
                'CP-SAT cannot solve models with variables without upper bounds.'
            )

        return lb, ub

    def _add_variables(self):
        vars = self._model.component_data_objects(Var, descend_into=True)

        for v in vars:
            v_id = id(v)

            if v.is_continuous():
                raise IncompatibleModelError(
                    'CP-SAT cannot solve models with continuous variables.'
                )

            lb, ub = self._cpsat_bounds_from_var(v)

            cpsat_var = self._solver_model.new_int_var(lb, ub, v.name)

            self._pyomo_var_to_solver_var_map[v_id] = cpsat_var
            self._vars.append(v)

    def _add_constraints(self):
        enforcement_literals = []

        cons = self._model.component_data_objects(Constraint, descend_into=True)

        for c in cons:
            if not c.active:
                continue

            # If we set quadratic=False in generate_standard_repn(),
            # we only need to check for nonlinear expressions
            repn = generate_standard_repn(c.body, quadratic=False)

            if repn.nonlinear_expr is not None:
                raise IncompatibleModelError(
                    f'Constraint {c.name} contains a nonlinear expression. '
                    'CP-SAT cannot solve models with nonlinear constraints.'
                )

            if len(repn.linear_vars) > 0:
                cpsat_expr = cp_model.LinearExpr.weighted_sum(
                    [
                        self._pyomo_var_to_solver_var_map[id(v)]
                        for v in repn.linear_vars
                    ],
                    repn.linear_coefs,
                )
            else:
                cpsat_expr = 0

            cpsat_expr += repn.constant

            if c.has_lb():
                cpsat_lb = c.lb
            else:
                cpsat_lb = cp_model.INT_MIN

            if c.has_ub():
                cpsat_ub = c.ub
            else:
                cpsat_ub = cp_model.INT_MAX

            cpsat_con = self._solver_model.add_linear_constraint(
                cpsat_expr, cpsat_lb, cpsat_ub
            ).with_name(c.name)

            if self._config.find_infeasible_subsystem:
                v = self._solver_model.new_bool_var(f'{c.name}')
                cpsat_con.only_enforce_if(v)
                enforcement_literals.append(v)

        if self._config.find_infeasible_subsystem:
            self._solver_model.add_assumptions(enforcement_literals)

    def _set_objective(self):
        if self._config.find_infeasible_subsystem:
            return

        obj = get_objective(self._model)

        if obj is None:
            raise ValueError('No active objectives to add to solver.')

        # If we set quadratic=False in generate_standard_repn(),
        # we only need to check for nonlinear expressions
        repn = generate_standard_repn(obj.expr, quadratic=False)

        if repn.nonlinear_expr is not None:
            raise IncompatibleModelError(
                f'Objective {obj.name} contains a nonlinear expression. '
                'CP-SAT cannot solve models with a nonlinear objective.'
            )

        if len(repn.linear_vars) > 0:
            cpsat_expr = cp_model.LinearExpr.weighted_sum(
                [self._pyomo_var_to_solver_var_map[id(v)] for v in repn.linear_vars],
                repn.linear_coefs,
            )
        else:
            cpsat_expr = 0

        cpsat_expr += repn.constant

        if obj.sense == minimize:
            self._solver_model.minimize(cpsat_expr)
        elif obj.sense == maximize:
            self._solver_model.maximize(cpsat_expr)
        else:
            raise ValueError(f'Objective sense {obj.sense} is not recognized.')

    def _load_results(self):
        results = Results()
        results.solver_name = 'CP-SAT'
        results.solver_version = self.version()
        results.solver_config = self._config
        results.solution_loader = CpsatSolutionLoader(
            self._solver_solver, self._vars, self._pyomo_var_to_solver_var_map
        )
        results.timing_info.cpsat_time = self._solver_solver.wall_time

        # CP-SAT solver status: google/or-tools/ortools/sat/cp_model.proto
        if self._solver_status == cp_model.UNKNOWN:
            results.solution_status = SolutionStatus.noSolution
            results.termination_condition = TerminationCondition.unknown
        elif self._solver_status == cp_model.MODEL_INVALID:
            results.solution_status = SolutionStatus.noSolution
            results.termination_condition = TerminationCondition.error
        elif self._solver_status == cp_model.FEASIBLE:
            results.solution_status = SolutionStatus.feasible
            results.termination_condition = TerminationCondition.interrupted
        elif self._solver_status == cp_model.INFEASIBLE:
            results.solution_status = SolutionStatus.infeasible
            results.termination_condition = TerminationCondition.provenInfeasible
        elif self._solver_status == cp_model.OPTIMAL:
            results.solution_status = SolutionStatus.optimal
            results.termination_condition = (
                TerminationCondition.convergenceCriteriaSatisfied
            )
        else:
            raise ValueError('CP-SAT terminated with invalid solver status.')

        if not self._config.find_infeasible_subsystem:
            if (
                results.solution_status != SolutionStatus.optimal
                and self._config.raise_exception_on_nonoptimal_result
            ):
                raise NoOptimalSolutionError

            if self._config.load_solutions:
                if self._solver_status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
                    results.solution_loader.load_vars()
                else:
                    raise NoFeasibleSolutionError

        results.incumbent_objective = self._solver_solver.objective_value
        results.objective_bound = self._solver_solver.best_objective_bound

        return results

    def _output_infeasible_subsystem(self):
        print('Infeasible subsystem of constraints')
        print('-----------------------------------')
        for i in self._solver_solver.sufficient_assumptions_for_infeasibility():
            print(self._solver_model.get_bool_var_from_proto_index(i).name)
        print('')
