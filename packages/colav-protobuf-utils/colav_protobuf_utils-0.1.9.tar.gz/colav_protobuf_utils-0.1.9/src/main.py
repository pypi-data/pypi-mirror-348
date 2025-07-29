from colav_protobuf_utils import ProtoType, Stamp
from colav_protobuf_utils.protobuf_generator import gen_mission_request, VesselType, GoalWaypoint
from colav_protobuf_utils.protobuf_generator import (
    gen_controller_feedback,
    CtrlStatus,
    CtrlMode,
)
from colav_protobuf_utils.protobuf_generator import gen_agent_update
from colav_protobuf_utils.protobuf_generator import (
    gen_obstacles_update,
    gen_static_obstacle,
    gen_dynamic_obstacle,
    StaticObstacleTypeEnum,
    DynamicObstacleTypeEnum,
)
from colav_protobuf_utils.protobuf_generator import (
    gen_mission_response,
    MissionResponseTypeEnum,
)
from colav_protobuf_utils.serialization import serialize_protobuf
from colav_protobuf_utils.deserialization import deserialize_protobuf

def test_mission_request_protogen_creator():
    return gen_mission_request(
        tag="MOCK_MISSION",
        stamp=Stamp(
            sec = int(231),
            nanosec= int(231)
        ),
        vessel_tag="MOCK_AGENTS",
        vessel_type=VesselType.HYDROFOIL,
        vessel_max_acceleration=float(5.0),
        vessel_max_deceleration=float(-2.0),
        vessel_max_velocity=float(30),
        vessel_min_velocity=float(15.0),
        vessel_max_yaw_rate=float(0.2),
        vessel_loa=float(2.0),
        vessel_beam=float(0.5),
        vessel_safety_radius=float(2.0),
        cartesian_init_position=(0,0,0),
        goal_waypoints=[
            GoalWaypoint(
                position=(0, 0, 0),
                acceptance_radius=float(2.0)
            )
        ]
    )

def test_mission_response_protogen_creator():
    return gen_mission_response(
        tag="MOCK_MISSION",
        stamp=Stamp(
            sec = int(231),
            nanosec= int(231)
        ),
        response_type=MissionResponseTypeEnum.MISSION_STARTING,
        response_details="Mission accepted",
    )

def test_agent_update_protogen_creator():
    return gen_agent_update(
        mission_tag="MOCK_MISSION",
        agent_tag="MOCK_AGENT",
        cartesian_position=[0, 0, 0],
        quaternium_orientation=[0, 0, 0, 1],
        velocity=15,
        yaw_rate=0.2,
        acceleration=0.2,
        stamp=Stamp(
            sec = int(231),
            nanosec= int(231)
        ),
    )

def test_dynamic_obstacle_protogen_creator():
    return [
        gen_dynamic_obstacle(
            tag="MOCK_DYNAMIC_OBSTACLE",
            type=DynamicObstacleTypeEnum.VESSEL,
            cartesian_position=[10, 3, 2],
            quaternium_orientation=[0, 0, 0, 1],
            velocity=15,
            yaw_rate=0.2,
            loa=2,
            beam=0.5,
            safety_radius=2,
        )
    ]

def test_static_obstacle_protogen_creator():
    return [
        gen_static_obstacle(
            tag="MOCK_STATIC_OBSTACLE",
            type=StaticObstacleTypeEnum.BUOY,
            cartesian_position=[10, 3, 2],
            quaternium_orientation=[0, 0, 0, 1],
            polyshape_points=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            inflation_radius=2,
        )
    ]

def test_obstacles_update_protogen_creator():
    dynamic_obstacle_list = test_dynamic_obstacle_protogen_creator()
    static_obstacle_list = test_static_obstacle_protogen_creator()

    return gen_obstacles_update(
        mission_tag="MOCK_MISSION",
        dynamic_obstacles=dynamic_obstacle_list,
        static_obstacles=static_obstacle_list,
        stamp=Stamp(
            sec = int(321), 
            nanosec=int(213)
        ),
    )

def test_controller_feedback_protogen_creator():
    return gen_controller_feedback(
        mission_tag="MOCK MISSION",
        agent_tag="mock agent",
        ctrl_mode=CTRLMode.CRUISE,
        ctrl_status=CTRLStatus.ACTIVE,
        velocity=float(15),
        yaw_rate=float(0.2),
        stamp=Stamp(
            sec = int(231),
            nanosec=int(131)
        )
    )

def main():
    proto_mission_request = test_mission_request_protogen_creator()
    serialised_mission_request = serialize_protobuf(proto_mission_request)
    deserialised_mission_request = deserialize_protobuf(serialised_mission_request, proto_type=ProtoType.MISSION_REQUEST)
    print (deserialised_mission_request)
    
    proto_mission_response = test_mission_response_protogen_creator()
    print (proto_mission_response)
    serialised_mission_response = serialize_protobuf(proto_mission_response)
    deserialised_mission_response = deserialize_protobuf(serialised_mission_response, proto_type=ProtoType.MISSION_RESPONSE)
    print (deserialised_mission_response)
    
    proto_agent_update = test_agent_update_protogen_creator()
    serialised_agent_update = serialize_protobuf(proto_agent_update)
    deserialised_agent_update = deserialize_protobuf(serialised_agent_update, proto_type=ProtoType.AGENT_UPDATE)
    print (deserialised_agent_update)

    proto_obstacles_update = test_obstacles_update_protogen_creator()
    serialised_obstacles_update = serialize_protobuf(proto_obstacles_update)
    deserialised_obstacles_update = deserialize_protobuf(serialised_obstacles_update, proto_type=ProtoType.OBSTACLES_UPDATE)
    print (deserialised_obstacles_update)
    
    proto_controller_feedback = test_controller_feedback_protogen_creator()
    serialised_controller_feedback = serialize_protobuf(proto_controller_feedback)
    deserialzed_controller_feedback = deserialize_protobuf(serialised_controller_feedback, proto_type=ProtoType.CONTROLLER_FEEDBACK)
    print (deserialzed_controller_feedback)

if __name__ == "__main__":
    main()
