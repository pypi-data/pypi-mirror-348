from colav_protobuf import MissionResponse
from enum import Enum
from .stamp import Stamp

class MissionResponseTypeEnum(Enum):
    UNKOWN = MissionResponse.MissionResponseMsg.ResponseTypeEnum.UNKNOWN
    MISSION_STARTING = (
        MissionResponse.MissionResponseMsg.ResponseTypeEnum.MISSION_STARTING
    )
    MISSION_ERROR = MissionResponse.MissionResponseMsg.ResponseTypeEnum.MISSION_ERROR
    MISSION_INVALID = (
        MissionResponse.MissionResponseMsg.ResponseTypeEnum.MISSION_INVALID
    )


def gen_mission_response(
    tag: str,
    stamp: Stamp,
    response_type: MissionResponseTypeEnum,
    response_details: str,
) -> MissionResponse:
    """Generate a protobuf message for MissionResponse"""
    mission_response = MissionResponse()
    mission_response.tag = tag
    mission_response.stamp.sec = stamp.sec
    mission_response.stamp.nanosec = stamp.nanosec
    mission_response.response.type = response_type.value
    mission_response.response.details = response_details

    return mission_response
