from colav_protobuf_utils.protobuf_generator import gen_mission_request, VesselType, GoalWaypoint
from colav_protobuf.examples import mission_request
from colav_protobuf_utils import Stamp
import pytest


def test_gen_mission_request():
    """test gen_mission_request"""
    goal_waypoints = [
        GoalWaypoint(
            position=(1.0, 2.0, 3.0),
            acceptance_radius=1.0
        ),
        GoalWaypoint(
            position=(2.0, 5.0, 2.0),
            acceptance_radius=1.0
        )
    ]
    proto_utils_mission_request = gen_mission_request(
        tag=mission_request.tag,
        stamp=Stamp(
            sec = mission_request.stamp.sec,
            nanosec = mission_request.stamp.nanosec
        ),
        vessel_tag=mission_request.vessel.tag,
        vessel_type=VesselType(mission_request.vessel.type),
        vessel_max_acceleration=mission_request.vessel.constraints.max_acceleration,
        vessel_max_deceleration=mission_request.vessel.constraints.max_deceleration,
        vessel_max_velocity=mission_request.vessel.constraints.max_velocity,
        vessel_min_velocity=mission_request.vessel.constraints.min_velocity,
        vessel_max_yaw_rate=mission_request.vessel.constraints.max_yaw_rate,
        vessel_loa=mission_request.vessel.geometry.loa,
        vessel_beam=mission_request.vessel.geometry.beam,
        vessel_safety_radius=mission_request.vessel.geometry.safety_radius,
        cartesian_init_position=(
            mission_request.init_position.x,
            mission_request.init_position.y,
            mission_request.init_position.z,
        ),
        goal_waypoints=goal_waypoints
    )
    assert proto_utils_mission_request.tag == mission_request.tag
    assert proto_utils_mission_request.stamp.sec == mission_request.stamp.sec
    assert proto_utils_mission_request.stamp.nanosec == mission_request.stamp.nanosec

