from colav_protobuf import ControllerFeedback
from enum import Enum, auto
from .stamp import Stamp


class CtrlMode(Enum):
    UNKNOWN = auto()
    CRUISE = auto()
    T2LOS = auto()
    T2Theta = auto()
    FB = auto()
    WAYPOINT_REACHED = auto()
    FINAL = auto()
    ERROR = auto()


class CtrlStatus(Enum):
    ACTIVE = auto()  # Actively evaluating modes, invariants, and transitions
    COMPLETED = auto()  # Reached a final mode or goal condition
    FAILED = auto()  # Invariant violation with no valid transition
    ABORTED = auto()  # Stopped externally
    TRANSITIONING = auto()
    AWAITING_MODE = auto()
    AWAITING_STATE = auto()


def gen_controller_feedback(
    mission_tag: str,
    agent_tag: str,
    mode: CtrlMode,
    status: CtrlStatus,
    velocity: float,
    yaw_rate: float,
    stamp: Stamp,
):
    feedback = ControllerFeedback()
    feedback.mission_tag = mission_tag
    feedback.agent_tag = agent_tag
    feedback.mode = ControllerFeedback.CtrlMode.Value(mode.name)
    feedback.status = ControllerFeedback.CtrlStatus.Value(status.name)
    feedback.cmd.velocity = velocity
    feedback.cmd.yaw_rate = yaw_rate
    feedback.stamp.sec = stamp.sec
    feedback.stamp.nanosec = stamp.nanosec
    return feedback
