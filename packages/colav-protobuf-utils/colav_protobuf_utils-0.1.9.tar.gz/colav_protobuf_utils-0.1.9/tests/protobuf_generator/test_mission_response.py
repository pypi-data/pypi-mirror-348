from colav_protobuf_utils.protobuf_generator import (
    gen_mission_response,
    MissionResponseTypeEnum,
)
from colav_protobuf_utils import Stamp
from colav_protobuf.examples import mission_response


def test_proto_gen_mission_response():
    """pytest assertion tests for generation of protobuf mission response"""
    protogen_mission_response = gen_mission_response(
        tag=mission_response.tag,
        stamp=Stamp(
            sec = mission_response.stamp.sec,
            nanosec=mission_response.stamp.nanosec
        ),
        response_type=MissionResponseTypeEnum(mission_response.response.type),
        response_details=mission_response.response.details,
    )
    assert protogen_mission_response.tag == mission_response.tag
    assert protogen_mission_response.stamp.sec == mission_response.stamp.sec
    assert protogen_mission_response.stamp.nanosec == mission_response.stamp.nanosec
    assert protogen_mission_response.response.type == mission_response.response.type
    assert (
        protogen_mission_response.response.details == mission_response.response.details
    )
