from colav_protobuf import AutomatonOutput
from typing import Tuple

# from .stamp import Stamp
from dataclasses import dataclass


@dataclass
class Waypoint:
    position: Tuple[float, float, float]
    acceptance_radius: float


@dataclass
class Stamp:
    sec: int
    nanosec: int


def gen_automaton_output(
    automaton_uuid: str,
    automaton_mode: str,
    automaton_status: str,
    controller_name: str,
    velocity: float,
    yaw_rate: float,
    waypoints: list[Waypoint],
    stamp: Stamp,
    elapsed_time: Stamp,
    error: bool,
    error_message: str,
) -> AutomatonOutput:
    """Generates a protobuf message for AutomatonOutput"""
    automaton_output = AutomatonOutput()
    automaton_output.automaton_uuid = automaton_uuid
    automaton_output.mode = automaton_mode
    automaton_output.status = automaton_status
    automaton_output.dynamics.controller_name = controller_name
    automaton_output.dynamics.cmd.velocity = velocity
    automaton_output.dynamics.cmd.yaw_rate = yaw_rate
    automaton_output.stamp.sec = stamp.sec
    automaton_output.stamp.nanosec = stamp.nanosec
    automaton_output.elapsed_time.sec = elapsed_time.sec
    automaton_output.elapsed_time.nanosec = elapsed_time.nanosec

    for waypoint in waypoints:
        automaton_output.waypoints.add()
        automaton_output.waypoints[-1].position.x = waypoint.position[0]
        automaton_output.waypoints[-1].position.y = waypoint.position[1]
        automaton_output.waypoints[-1].position.z = waypoint.position[2]
        automaton_output.waypoints[-1].acceptance_radius = waypoint.acceptance_radius

    automaton_output.error = error
    automaton_output.message = error_message

    return automaton_output


# def main():
#     # Example usage
#     automaton_uuid = "12345"
#     automaton_mode = "CRUISE"
#     automaton_status = "ACTIVE"
#     controller_name = "Controller1"
#     velocity = 1.0
#     yaw_rate = 0.5
#     waypoints = [Waypoint((1.0, 2.0, 3.0), 0.5)]
#     stamp = Stamp(123456789, 987654321)
#     elapsed_time = Stamp(123456789, 987654321)
#     error = False
#     error_message = ""

#     automaton_output = gen_automaton_output(
#         automaton_uuid,
#         automaton_mode,
#         automaton_status,
#         controller_name,
#         velocity,
#         yaw_rate,
#         waypoints,
#         stamp,
#         elapsed_time,
#         error,
#         error_message,
#     )

#     print(automaton_output)


# if __name__ == "__main__":
#     main()
