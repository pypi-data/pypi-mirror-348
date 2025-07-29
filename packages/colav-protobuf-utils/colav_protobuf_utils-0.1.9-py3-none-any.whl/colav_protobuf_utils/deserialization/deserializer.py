from colav_protobuf import (
    MissionRequest,
    MissionResponse,
    AgentUpdate,
    ObstaclesUpdate,
    ControllerFeedback,
    UnsafeSet,
    AutomatonOutput,
    CollisionMetrics
)
from colav_protobuf_utils import VesselType
from enum import Enum
import math
from typing import Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProtoType(Enum):
    MISSION_REQUEST = "mission_request"
    MISSION_RESPONSE = "mission_response"
    AGENT_UPDATE = "agent_update"
    OBSTACLES_UPDATE = "obstacles_update"
    CONTROLLER_FEEDBACK = "controller_feedback"
    UNSAFE_SET = "unsafe_set"
    AUTOMATON_OUTPUT = "automaton_output"
    COLLISION_METRICS = "collision_metrics"

# Define constants for error messages for easy maintenance
INVALID_MISSION_TAG_MSG = "MissionRequest tag is empty"
INVALID_MISSION_TIMESTAMP_MSG = "MissionRequest timestamp is empty"
INVALID_VESSEL_TAG_MSG = "MissionRequest vessel tag is empty"
INVALID_VESSEL_TYPE_MSG = "MissionRequest vessel type is invalid, Needs to be one of the values assigned in colav_protobuf_utils.protobuf_generator.mission_request.VesselType"
INVALID_CONSTRAINT_MSG = "MissionRequest vessel constraints, {} invalid"
INVALID_GEOMETRY_MSG = "MissionRequest vessel geometry, {} invalid"

# Reusable validation functions
def _validate_constraints(constraints) -> None:
    if constraints.max_acceleration <= 0:
        raise ValueError(INVALID_CONSTRAINT_MSG.format("max_acceleration"))
    if constraints.max_deceleration >= 0:
        raise ValueError(INVALID_CONSTRAINT_MSG.format("max_deceleration"))
    if constraints.max_velocity <= 0:
        raise ValueError(INVALID_CONSTRAINT_MSG.format("max_velocity"))
    if constraints.min_velocity <= 0 or constraints.min_velocity >= constraints.max_velocity:
        raise ValueError(INVALID_CONSTRAINT_MSG.format("min_velocity"))
    if constraints.max_yaw_rate <= 0 or constraints.max_yaw_rate >= 1:
        raise ValueError(INVALID_CONSTRAINT_MSG.format("max_yaw_rate"))

def _validate_geometry(geometry) -> None:
    if not geometry.loa or geometry.loa < 0:
        raise ValueError(INVALID_GEOMETRY_MSG.format("loa"))
    if not geometry.beam or geometry.beam < 0:
        raise ValueError(INVALID_GEOMETRY_MSG.format("beam"))
    if not geometry.safety_radius or geometry.safety_radius < 0:
        raise ValueError(INVALID_GEOMETRY_MSG.format("safety_radius"))

def validate_waypoint(waypoints, vessel_geometry) -> None:
    if not len(waypoints) > 0:
        raise ValueError("MissionRequest goal_waypoints must have at least one waypoint")
    
    for waypoint in waypoints:
        if not waypoint.position:
            raise ValueError("MissionRequest goal_waypoint.position must be given as a tuple of float representing cartesian coordinates of goal position.")
        if not waypoint.acceptance_radius or waypoint.acceptance_radius < _max_radius(beam=vessel_geometry.beam, loa=vessel_geometry.loa):
            raise ValueError(f"MissionRequest goal_waypoint.acceptance_radius must be given and it must be greater than or equal to min radius of geometry {_max_radius(beam=vessel_geometry.beam, loa=vessel_geometry.loa)}")

def _max_radius(beam: float, loa: float) -> float:
    """Calculate the diagonal of vessel geometry and return as min safety radius"""
    diagonal = math.sqrt(beam**2 + loa**2)
    return diagonal / 2

def deserialize_protobuf(protobuf: bytes, proto_type: ProtoType) -> Union[MissionRequest, MissionResponse, AgentUpdate, ObstaclesUpdate, ControllerFeedback, UnsafeSet, AutomatonOutput, CollisionMetrics]:
    """Deserialization dispatcher for colav protobuf messages"""
    try:
        if proto_type == ProtoType.MISSION_REQUEST:
            return _deserialize_mission_request(protobuf)
        if proto_type == ProtoType.MISSION_RESPONSE:
            return _deserialize_mission_response(protobuf)
        if proto_type == ProtoType.AGENT_UPDATE:
            return _deserialize_agent_update(protobuf)
        if proto_type == ProtoType.OBSTACLES_UPDATE:
            return _deserialize_obstacles_update(protobuf)
        if proto_type == ProtoType.CONTROLLER_FEEDBACK:
            return _deserialize_controller_feedback(protobuf)
        if proto_type == ProtoType.UNSAFE_SET:
            return _deserialize_unsafe_set(protobuf)
        if proto_type == ProtoType.AUTOMATON_OUTPUT:
            return _deserialize_automaton_output(protobuf)
        if proto_type == ProtoType.COLLISION_METRICS:
            return _deserialize_collision_metrics(protobuf)
    except ValueError as e:
        logger.error(f"deserializer::deserialize_protobuf: {e}")
        raise
    except Exception as e:
        logger.error(f"deserializer::deserialize_protobuf: Unexpected Exception occurred: {e}")
        raise

def _deserialize_collision_metrics(protobuf: bytes) -> CollisionMetrics:
    """deserialize and validate collision metrics"""
    msg = CollisionMetrics()
    msg.ParseFromString(protobuf)

    return msg

def _deserialize_automaton_output(protobuf: bytes) -> AutomatonOutput:
    """DEserialize and validate automaton output"""
    msg = AutomatonOutput()
    msg.ParseFromString(protobuf)

    return msg

def _deserialize_unsafe_set(protobuf: bytes) -> UnsafeSet:
    """Deserialize UnsafeSet protobuf message and validate its fields"""
    msg = UnsafeSet()
    msg.ParseFromString(protobuf)

    logger.info(msg)

    # if not msg.mission_tag:
    #     raise ValueError(INVALID_MISSION_TAG_MSG)
    # if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
    #     raise ValueError(INVALID_MISSION_TIMESTAMP_MSG)
    
    # TODO: If geometry should validate polyshape is valid for unsafe set
    return msg
    

def _deserialize_mission_request(protobuf: bytes) -> MissionRequest:
    """Deserialize MissionRequest protobuf message and validate its fields"""
    msg = MissionRequest()
    msg.ParseFromString(protobuf)

    logger.info(msg)

    # Validation checks
    if not msg.tag:
        raise ValueError(INVALID_MISSION_TAG_MSG)
    if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
        raise ValueError(INVALID_MISSION_TIMESTAMP_MSG)
    if not msg.vessel.tag:
        raise ValueError(INVALID_VESSEL_TAG_MSG)
    if msg.vessel.type not in [MissionRequest.Vessel.VesselType.Value(type_.name) for type_ in VesselType]:
        raise ValueError(INVALID_VESSEL_TYPE_MSG)
    # Validate vessel constraints
    _validate_constraints(msg.vessel.constraints)
    # Validate vessel geometry
    _validate_geometry(msg.vessel.geometry)
    # Validate init position and goal waypoint
    if not msg.init_position:
        raise ValueError("MissionRequest init_position must be given as a tuple of float representing cartesian coordinates")
    validate_waypoint(msg.goal_waypoints, msg.vessel.geometry)

    return msg

class MissionResponseTypeEnum(Enum):
    UNKNOWN = 0
    MISSION_STARTING = 1
    MISSION_ERROR = 2
    MISSION_INVALID = 3

def _deserialize_mission_response(protobuf: bytes) -> MissionResponse:
    """Deserialize MissionResponse protobuf message and validate its fields"""
    try:
        msg = MissionResponse()
        msg.ParseFromString(protobuf)
        
        if not msg.tag:
            raise ValueError("MissionResponse tag is empty")
        if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
            raise ValueError("MissionResponse timestamp is empty")
        if msg.response.type not in [MissionResponse.MissionResponseMsg.ResponseTypeEnum.Value(type_.name) for type_ in MissionResponseTypeEnum]:
            raise ValueError("MissionResponse response type is invalid, Needs to be one of the values assigned in colav_protobuf_utils.protobuf_generator.mission_response.MissionResponseTypeEnum")
        if msg.response.details == "":
            raise ValueError("MissionResponse response details is empty")
    except Exception as e:
        logger.error(f"deserializer::_deserialize_mission_response: Error deserializing MissionResponse: {e}")
        raise
    return msg

def _deserialize_agent_update(protobuf: bytes) -> AgentUpdate:
    """Deserialize AgentUpdate protobuf message and validate its fields"""
    try:
        msg = AgentUpdate()
        msg.ParseFromString(protobuf)
        
        if not msg.mission_tag:
            raise ValueError("AgentUpdate mission_tag is empty")
        if not msg.agent_tag:
            raise ValueError("AgentUpdate agent_tag is empty")
        if msg.state.pose.position.x is None or msg.state.pose.position.y is None or msg.state.pose.position.z is None:
            raise ValueError("AgentUpdate state.pose.position is empty")
        if msg.state.pose.orientation.x is None or msg.state.pose.orientation.y is None or msg.state.pose.orientation.z is None or msg.state.pose.orientation.w is None:
            raise ValueError("AgentUpdate state.pose.orientation is empty")
        if msg.state.velocity is None or msg.state.velocity < 0:
            raise ValueError("AgentUpdate state.velocity is invalid")
        if msg.state.yaw_rate is None:
            raise ValueError("AgentUpdate state.yaw_rate is invalid")
        if msg.state.acceleration is None:
            raise ValueError("AgentUpdate state.acceleration is invalid")
        if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
            raise ValueError("AgentUpdate timestamp is empty")
    except Exception as e:
        logger.error(f"deserializer::_deserialize_agent_update: Error deserializing AgentUpdate: {e}")
        raise
    return msg

def _deserialize_obstacles_update(protobuf: bytes) -> ObstaclesUpdate:
    """Deserialize ObstaclesUpdate protobuf message and validate its fields"""
    # Implementation needed
    try: 
        msg = ObstaclesUpdate()
        msg.ParseFromString(protobuf)
        
        if not msg.mission_tag:
            raise ValueError("ObstaclesUpdate mission_tag is empty")
        if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
            raise ValueError("ObstaclesUpdate timestamp is empty")
        if len(msg.static_obstacles) > 0: 
            for static_obstacle in msg.static_obstacles: 
                if not static_obstacle.tag:
                    raise ValueError("ObstaclesUpdate static_obstacle tag is empty")
                if not static_obstacle.type:
                    raise ValueError("ObstaclesUpdate static_obstacle type is empty")
                if static_obstacle.pose.position.x is None or static_obstacle.pose.position.y is None or static_obstacle.pose.position.z is None:
                    raise ValueError("ObstaclesUpdate static_obstacle pose.position is empty")
                if static_obstacle.pose.orientation.x is None or static_obstacle.pose.orientation.y is None or static_obstacle.pose.orientation.z is None or static_obstacle.pose.orientation.w is None:
                    raise ValueError("ObstaclesUpdate static_obstacle pose.orientation is empty")
                # TODO: Change geometry to use polyshape points in colav interfaces and validate them.
        if len(msg.dynamic_obstacles) > 0:
            for dynamic_obstacle in msg.dynamic_obstacles:
                if not dynamic_obstacle.tag:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle tag is empty")
                if not dynamic_obstacle.type:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle type is empty")
                if dynamic_obstacle.state.pose.position.x is None or dynamic_obstacle.state.pose.position.y is None or dynamic_obstacle.state.pose.position.z is None:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle state.pose.position is empty")
                if dynamic_obstacle.state.pose.orientation.x is None or dynamic_obstacle.state.pose.orientation.y is None or dynamic_obstacle.state.pose.orientation.z is None or dynamic_obstacle.state.pose.orientation.w is None:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle state.pose.orientation is empty")
                if dynamic_obstacle.state.velocity is None or dynamic_obstacle.state.velocity < 0:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle state.velocity is invalid")
                if dynamic_obstacle.state.yaw_rate is None:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle state.yaw_rate is invalid")
                if dynamic_obstacle.geometry.loa is None or dynamic_obstacle.geometry.loa < 0:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle geometry.loa is invalid")
                if dynamic_obstacle.geometry.beam is None or dynamic_obstacle.geometry.beam < 0:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle geometry.beam is invalid")
                if dynamic_obstacle.geometry.safety_radius is None or dynamic_obstacle.geometry.safety_radius < 0:
                    raise ValueError("ObstaclesUpdate dynamic_obstacle geometry.safety_radius is invalid") 
    except Exception as e: 
        logger.error(f"deserializer::_deserialize_obstacles_update: Error deserializing ObstaclesUpdate: {e}")
        raise
    return msg

class CtrlMode(Enum):
    UNKNOWN = 0
    CRUISE = 1
    T2LOS = 2
    T2Theta = 3
    FB = 4
    WAYPOINT_REACHED = 5
    
class CtrlStatus(Enum):
    UNKNOWN_STATUS = 0
    ACTIVE = 1
    INACTIVE = 2
    ERROR = 3

def _deserialize_controller_feedback(protobuf: bytes) -> ControllerFeedback:
    """Deserialize ControllerFeedback protobuf message and validate its fields"""
    # Implementation needed
    try: 
        msg = ControllerFeedback()
        msg.ParseFromString(protobuf)
        
        if not msg.mission_tag:
            raise ValueError("ControllerFeedback mission_tag is empty")
        if not msg.agent_tag:
            raise ValueError("ControllerFeedback agent_tag is empty")
        if msg.mode not in [ControllerFeedback.CtrlMode.Value(mode_.name) for mode_ in CtrlMode]:
            raise ValueError("ControllerFeedback ctrl_mode is invalid, Needs to be one of the values assigned in colav_protobuf_utils.protobuf_generator.controller_feedback.CtrlMode")
        if msg.status not in [ControllerFeedback.CtrlStatus.Value(status_.name) for status_ in CtrlStatus]:
            raise ValueError("ControllerFeedback ctrl_status is invalid, Needs to be one of the values assigned in colav_protobuf_utils.protobuf_generator.controller_feedback.CtrlStatus")
        if msg.stamp.sec < 0 or msg.stamp.nanosec < 0:
            raise ValueError("ControllerFeedback timestamp is empty")
        if msg.cmd.velocity is None or msg.cmd.yaw_rate is None: 
            raise ValueError("ControllerFeedback ctrl_cmd velocity or yaw_rate is empty")
    except Exception as e: 
        logger.error(f"deserializer::_deserialize_controller_feedback: Error deserializing ControllerFeedback: {e}")
        raise
    return msg