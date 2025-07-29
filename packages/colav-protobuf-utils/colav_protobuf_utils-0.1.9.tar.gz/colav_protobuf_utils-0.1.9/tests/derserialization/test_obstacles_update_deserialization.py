from colav_protobuf_utils.deserialization import deserialize_protobuf
from colav_protobuf_utils.serialization import serialize_protobuf
from colav_protobuf_utils import ProtoType
from colav_protobuf.examples import obstacles_update

def test_obstacles_update_deserialization():

    deserialized_proto = deserialize_protobuf(
        serialize_protobuf(obstacles_update),
        ProtoType.OBSTACLES_UPDATE
    )
    assert deserialized_proto.mission_tag == obstacles_update.mission_tag

    # assert deserialized_proto.mission_tag == agent_update.mission_tag, "mission_tag assertion failed"
    # assert deserialized_proto.agent_tag == agent_update.agent_tag
    # assert deserialized_proto.stamp.sec == agent_update.stamp.sec
    # assert deserialized_proto.stamp.nanosec == agent_update.stamp.nanosec
    # assert deserialized_proto.state.pose.position.x == agent_update.state.pose.position.x
    # assert deserialized_proto.state.pose.position.y == agent_update.state.pose.position.y
    # assert deserialized_proto.state.pose.position.z == agent_update.state.pose.position.z
    # assert deserialized_proto.state.pose.orientation.x == agent_update.state.pose.orientation.x
    # assert deserialized_proto.state.pose.orientation.y == agent_update.state.pose.orientation.y
    # assert deserialized_proto.state.pose.orientation.z == agent_update.state.pose.orientation.z
    # assert deserialized_proto.state.pose.orientation.w == agent_update.state.pose.orientation.w

def test_agent_update_validation_edge_case_0_timestamp():
    test_obstacles_update = obstacles_update
    test_obstacles_update.stamp.sec = int(0)
    test_obstacles_update.stamp.nanosec = int(0)
    deserialized_proto = deserialize_protobuf(
        serialize_protobuf(test_obstacles_update),
        ProtoType.OBSTACLES_UPDATE
    )
    assert deserialized_proto.stamp.sec == test_obstacles_update.stamp.sec
    assert deserialized_proto.stamp.nanosec == test_obstacles_update.stamp.nanosec