from colav_protobuf_utils.deserialization import deserialize_protobuf
from colav_protobuf_utils.serialization import serialize_protobuf
from colav_protobuf_utils import ProtoType
from colav_protobuf.examples import mission_request

def test_mission_request_validation():
    deserialized_proto = deserialize_protobuf(
        serialize_protobuf(mission_request),
        ProtoType.MISSION_REQUEST
    )

    assert deserialized_proto.tag == mission_request.tag, "mission_tag assertion failed"
    assert deserialized_proto.stamp.sec == mission_request.stamp.sec
    assert deserialized_proto.stamp.nanosec == mission_request.stamp.nanosec

    assert deserialized_proto.vessel.tag == mission_request.vessel.tag
    assert deserialized_proto.vessel.type  == mission_request.vessel.type 
    assert deserialized_proto.vessel.constraints.max_acceleration == mission_request.vessel.constraints.max_acceleration
    assert deserialized_proto.vessel.constraints.max_deceleration  == mission_request.vessel.constraints.max_deceleration 
    assert deserialized_proto.vessel.constraints.max_velocity == mission_request.vessel.constraints.max_velocity
    assert deserialized_proto.vessel.constraints.min_velocity == mission_request.vessel.constraints.min_velocity
    assert deserialized_proto.vessel.constraints.max_yaw_rate  == mission_request.vessel.constraints.max_yaw_rate 
    assert deserialized_proto.vessel.geometry.safety_radius == mission_request.vessel.geometry.safety_radius
    assert deserialized_proto.vessel.geometry.loa == mission_request.vessel.geometry.loa
    assert deserialized_proto.vessel.geometry.beam  == mission_request.vessel.geometry.beam 

def test_mission_request_validation_edge_case_0_timestamp():
    test_mission_request_update = mission_request
    test_mission_request_update.stamp.sec = int(0)
    test_mission_request_update.stamp.nanosec = int(0)
    deserialized_proto = deserialize_protobuf(
        serialize_protobuf(test_mission_request_update),
        ProtoType.MISSION_REQUEST
    )
    assert deserialized_proto.stamp.sec == test_mission_request_update.stamp.sec
    assert deserialized_proto.stamp.nanosec == test_mission_request_update.stamp.nanosec
