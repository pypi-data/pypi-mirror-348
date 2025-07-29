from colav_protobuf import UnsafeSet  # Assuming Vertex is the correct message type
from .stamp import Stamp
from typing import List, Tuple


def gen_unsafe_set(
        mission_tag: str,
        stamp: Stamp,
        vertices: List[Tuple[float, float, float]]
) -> UnsafeSet:
    """Generate a protobuf message for UnsafeSet"""
    unsafe_set = UnsafeSet()
    unsafe_set.mission_tag = mission_tag
    unsafe_set.stamp.sec = stamp.sec
    unsafe_set.stamp.nanosec = stamp.nanosec
    
    for coordinate in vertices:
        vertex = unsafe_set.vertices.add() 
        vertex.x = coordinate[0]
        vertex.y = coordinate[1]
        vertex.z = coordinate[2]  

    return unsafe_set  
