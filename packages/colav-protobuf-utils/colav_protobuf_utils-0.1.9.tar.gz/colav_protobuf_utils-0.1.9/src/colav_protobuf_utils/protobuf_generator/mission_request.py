from colav_protobuf import MissionRequest
from typing import Tuple, List
from enum import Enum
from dataclasses import dataclass, field
from typing import Tuple
from .stamp import Stamp

class VesselType(Enum):
    UNSPECIFIED = 0
    HYDROFOIL = 1

@dataclass
class GoalWaypoint:
    position: Tuple[float, float, float]
    acceptance_radius: float

def gen_mission_request(
    tag: str,
    stamp: Stamp,
    vessel_tag: str,
    vessel_type: VesselType,
    vessel_max_acceleration: float,
    vessel_max_deceleration: float,
    vessel_max_velocity: float,
    vessel_min_velocity: float,
    vessel_max_yaw_rate: float,
    vessel_loa: float,
    vessel_beam: float,
    vessel_safety_radius: float,
    cartesian_init_position: Tuple[float, float, float],
    goal_waypoints: List[GoalWaypoint]
) -> MissionRequest:
    """Generates a protobuf message for MissionRequest"""
    try:
        if len(goal_waypoints) <= 0:
            raise Exception("goal_waypoints must have at least one element") 
        req = MissionRequest()
        req.tag = tag
        req.stamp.sec = stamp.sec
        req.stamp.nanosec = stamp.nanosec
        req.vessel.tag = vessel_tag
        req.vessel.type = MissionRequest.Vessel.VesselType.Value(vessel_type.name)
        req.vessel.constraints.max_acceleration = vessel_max_acceleration
        req.vessel.constraints.max_deceleration = vessel_max_deceleration
        req.vessel.constraints.max_velocity = vessel_max_velocity
        req.vessel.constraints.min_velocity = vessel_min_velocity
        req.vessel.constraints.max_yaw_rate = vessel_max_yaw_rate
        req.vessel.geometry.loa = vessel_loa
        req.vessel.geometry.beam = vessel_beam
        req.vessel.geometry.safety_radius = vessel_safety_radius
        req.init_position.x = cartesian_init_position[0]
        req.init_position.y = cartesian_init_position[1]
        req.init_position.z = cartesian_init_position[2]
        
        for idx, goal_waypoint in enumerate(goal_waypoints):
            req.goal_waypoints.add()

            req.goal_waypoints[idx].position.x = goal_waypoint.position[0]
            req.goal_waypoints[idx].position.y = goal_waypoint.position[1]
            req.goal_waypoints[idx].position.z = goal_waypoint.position[2]
            req.goal_waypoints[idx].acceptance_radius = goal_waypoint.acceptance_radius  # TODO: Change this to be acceptance radius instead of safety radius.
    except Exception as e:
        raise Exception(e)

    return req
