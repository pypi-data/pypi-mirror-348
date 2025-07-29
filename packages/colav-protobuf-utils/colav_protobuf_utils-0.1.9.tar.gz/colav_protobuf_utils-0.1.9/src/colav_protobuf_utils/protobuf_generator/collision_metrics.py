from colav_protobuf import CollisionMetrics
from typing import List 
from .stamp import Stamp

def gen_dynamic_obstacle_with_collision_metric(
    obstacle_tag: str,
    tcpa: float,
    dcpa: float
) -> CollisionMetrics.DynamicObstacleCollisionMetrics:
    msg = CollisionMetrics.DynamicObstacleCollisionMetrics()
    msg.obstacle_tag = obstacle_tag
    msg.tcpa = tcpa
    msg.dcpa = dcpa
    return msg


def gen_static_obstacle_with_collision_metric(
    obstacle_tag: str,
    min_distance: float,
    time_to_min_distance: float
) -> CollisionMetrics.StaticObstacleCollisionMetrics:
    msg = CollisionMetrics.StaticObstacleCollisionMetrics()
    msg.obstacle_tag = obstacle_tag
    msg.min_distance = min_distance
    msg.time_to_min_distance = time_to_min_distance
    return msg

def gen_collision_metrics(
    agent_tag: str,
    stamp: Stamp,
    dynamics_obstacles_w_collision_metrics: List[CollisionMetrics.DynamicObstacleCollisionMetrics],
    static_obstacles_w_collision_metrics: List[CollisionMetrics.StaticObstacleCollisionMetrics]
) -> CollisionMetrics:
    """gen collision metric protobuf"""
    msg = CollisionMetrics()
    msg.agent_tag = agent_tag
    msg.stamp.sec = stamp.sec
    msg.stamp.nanosec = stamp.nanosec

    for d in dynamics_obstacles_w_collision_metrics:
        entry = msg.dynamic_obstacle_collision_metrics.add()
        entry.obstacle_tag = d.obstacle_tag
        entry.tcpa = d.tcpa
        entry.dcpa = d.dcpa

    for s in static_obstacles_w_collision_metrics:
        entry = msg.static_obstacle_collision_metrics.add()
        entry.obstacle_tag = s.obstacle_tag
        entry.min_distance = s.min_distance
        entry.time_to_min_distance = s.time_to_min_distance

    return msg

# def main():
#     # Create example stamp
#     stamp = Stamp(sec=1234567890, nanosec=987654321)

#     # Create dynamic obstacle metrics
#     dynamic1 = gen_dynamic_obstacle_with_collision_metric("obstacle_d1", tcpa=10.5, dcpa=25.0)
#     dynamic2 = gen_dynamic_obstacle_with_collision_metric("obstacle_d2", tcpa=5.2, dcpa=30.0)

#     # Create static obstacle metrics
#     static1 = gen_static_obstacle_with_collision_metric("obstacle_s1", min_distance=12.3, time_to_min_distance=3.0)
#     static2 = gen_static_obstacle_with_collision_metric("obstacle_s2", min_distance=8.0, time_to_min_distance=1.5)

#     # Generate final CollisionMetrics message
#     collision_metrics_msg = gen_collision_metrics(
#         agent_tag="ego_agent_1",
#         stamp=stamp,
#         dynamics_obstacles_w_collision_metrics=[dynamic1, dynamic2],
#         static_obstacles_w_collision_metrics=[static1, static2]
#     )

#     # Print output
#     print("Serialized CollisionMetrics:")
#     print(collision_metrics_msg)  # human-readable
#     print("Raw Bytes:")
#     print(collision_metrics_msg.SerializeToString())  # for transmission


# if __name__ == "__main__":
#     main()