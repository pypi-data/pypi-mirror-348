"""Sweep Action."""

from finesse.exceptions import FinesseException, NotChangeableDuringSimulation
from finesse.components import DegreeOfFreedom
from ...parameter import Parameter, GeometricParameter, ParameterRef
from ...element import ModelElement
from ...solutions import ArraySolution
from ..runners import run_axes_scan
from .base import Action, convert_str_to_parameter
from .folder import Folder
import logging
import numpy as np
import warnings
from finesse.warnings import (
    InvalidSweepVariableWarning,
    ModelParameterSettingWarning,
)
from finesse.env import warn

LOGGER = logging.getLogger(__name__)


def get_sweep_array(start: float, stop: float, steps: int, mode="lin"):
    start = float(start)
    stop = float(stop)
    steps = int(steps)
    if steps <= 0:
        raise Exception("Steps must be greater than 0")

    if mode == "lin":
        arr = np.linspace(start, stop, steps + 1)
    elif mode == "log":
        arr = np.logspace(np.log10(start), np.log10(stop), steps + 1)
    else:
        raise ValueError(f"{mode} should be either lin or log")
    return arr


# IMPORTANT: renaming this class impacts the katscript spec and should be avoided!
class Sweep(Action):
    """An action that sweeps N number of parameters through the values in N arrays.

    Parameters
    ----------
    args : [Parameter, str], array, boolean
        Expects 3 arguments per axis. The first is a full name of a Parameter or
        a Parameter object. The second is an array of values to step this
        parameter over, and lastly a boolean value to say whether this is a
        relative step from the parameters initial value.

    pre_step : Action, optional
        An action to perform before the step is computed

    post_step : Action, optional
        An action to perform after the step is computed

    reset_parameter : boolean, optional
        When true this action will reset the all the parameters it changed to
        the values before it ran.

    name : str
        Name of the action, used to find the solution in the final output.
    """

    def __init__(
        self, *args, pre_step=None, post_step=None, reset_parameter=True, name="sweep"
    ):
        super().__init__(name)
        if len(args) % 3 != 0:
            raise Exception(
                f"Sweep requires triplet of input arguments: parameter, array, relative_change. Not {args}"
            )
        self.args = args
        self.pre_step = pre_step
        self.post_step = post_step
        self.reset_parameter = reset_parameter

        def process_input_parameter(p):
            if isinstance(p, ModelElement):
                if p.default_parameter_name is None:
                    extra = ""
                    if isinstance(p, DegreeOfFreedom):
                        extra = f".\nDid you mean '{p.name}.DC'?"
                    raise ValueError(
                        f"{repr(p)} does not have a default parameter, please specify "
                        "one to use" + extra
                    )
                p = getattr(p, p.default_parameter_name)
            elif isinstance(p, ParameterRef):
                p = p.parameter

            if isinstance(p, Parameter):
                if not p.changeable_during_simulation:
                    raise NotChangeableDuringSimulation(
                        f"Parameter {p.full_name} cannot be changed during a simulation"
                    )
                return p.full_name
            else:
                return p

        self.parameters = tuple(process_input_parameter(p) for p in args[::3])

        self.axes = tuple(np.atleast_1d(_).astype(np.float64) for _ in args[1::3])
        # Convert bool true or false to a 0 or 1, True meaning we sweep around the
        # initial value of the parameter
        self.fractional_offset = np.array(args[2::3], dtype=np.float64)
        self.out_shape = tuple(np.size(_) for _ in self.axes)

    def _requests(self, model, memo, first=True):
        params = tuple(convert_str_to_parameter(model, _) for _ in self.parameters)

        if self.reset_parameter:
            # Get the actual parameter for this xaxis
            for p in params:
                if p.value is None:
                    raise FinesseException(
                        f"Parameters being changed in a simulation must start with a float value not None. Change {repr(p)} to a float value before running the simulation."
                    )

        if any((not p.changeable_during_simulation for p in params)):
            raise NotChangeableDuringSimulation(
                f"The property {p.full_name} cannot be changed during a simulation"
            )

        memo["changing_parameters"].extend(self.parameters)
        if self.pre_step:
            self.pre_step._requests(model, memo)
        if self.post_step:
            self.post_step._requests(model, memo)

    def _do(self, state):
        if state.model is None:
            raise Exception("No model was provided")
        if state.sim is None:
            raise Exception("No simulation was provided")

        # Get all the parameters that need to be tuned in this action and
        # any of its pre/post steps
        rq = self.get_requests(state.model)
        all_params = tuple(
            convert_str_to_parameter(state.model, _) for _ in rq["changing_parameters"]
        )
        # Get the actual parameter for this sweep
        params = tuple(
            convert_str_to_parameter(state.model, _) for _ in self.parameters
        )

        if not all((p.is_tunable for p in all_params)):
            raise Exception(
                f"Not all parameters {params} are tunable in this simulation {state.sim}"
            )

        return self._run_sweep(state, params, changing_parameters=all_params)

    def _run_sweep(self, state, params, changing_parameters):
        # Record intial values of parameters before we go changing
        # anything so we can reset them later
        if self.reset_parameter:
            initial = tuple(float(param.value) for param in changing_parameters)
        float_params = np.array(params, dtype=np.float64)
        nan_entries = np.isnan(float_params)
        if np.any(nan_entries):
            warn(
                f"Parameters {np.array(params)[nan_entries]} have a NaN initial value and may cause issues",
                InvalidSweepVariableWarning,
            )

        inf_entries = np.isinf(float_params)
        inf_offset_sweep_entries = inf_entries & (self.fractional_offset != 0)
        if np.any(inf_offset_sweep_entries):
            warn(
                f"Parameters {np.array(params)[inf_offset_sweep_entries]} have a Inf initial value and are being swept relative to it's self which may result in errors.",
                InvalidSweepVariableWarning,
            )

        sol = ArraySolution(
            self.name,
            None,
            self.out_shape,
            self.axes,
            params,
        )
        sol.enable_update(state.sim.detector_workspaces)
        # compute actual offsets. As from issue 400 need to be more careful when
        # computing offsets as inf * 0 gives nans, and you can't really offset
        # sweep around an inf anyway
        idx = self.fractional_offset != 0
        offsets = np.zeros_like(float_params)
        offsets[idx] = float_params[idx] * self.fractional_offset[idx]

        # Make new folder structure in solution if we have any actions
        # that branch off.
        pre_step = Folder("pre_step", self.pre_step, sol) if self.pre_step else None
        post_step = Folder("post_step", self.post_step, sol) if self.post_step else None
        run_axes_scan(
            state,
            self.axes,
            params,
            offsets,
            self.out_shape,
            sol,
            pre_step,
            post_step,
            progress_bar=True,
            progress_bar_desc=self.name,
        )
        if self.reset_parameter:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ModelParameterSettingWarning)

                # Reset all parameters and if we were changing a geometric parameter
                # reset the beamtrace data to initial state
                for i, param in zip(initial, changing_parameters):
                    param.value = i

                # Ensure the __cvalue of each symbolic parameter gets reset accordingly
                for param in state.sim.changing_parameters:
                    param._reset_cvalue()

                if any(
                    type(p) is GeometricParameter and p.is_symbolic
                    for p in state.sim.changing_parameters
                ):
                    state.model._update_symbolic_abcds()
                # Need to check all changing parameters incase of symbols
                # if any(type(p) is GeometricParameter for p in state.sim.changing_parameters):
                #    state.model.beam_trace()

        return sol
