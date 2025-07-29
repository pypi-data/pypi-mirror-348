from colav_protobuf import (
    MissionRequest,
    MissionResponse, 
    ObstaclesUpdate,
    AgentUpdate,
    ControllerFeedback,
    UnsafeSet,
    AutomatonOutput,
    CollisionMetrics
)
from typing import Union


def serialize_protobuf(
    protobuf: Union[
        MissionRequest,
        MissionResponse,
        AgentUpdate,
        ObstaclesUpdate,
        ControllerFeedback,
        UnsafeSet,
        AutomatonOutput,
        CollisionMetrics
    ]
) -> bytes:
    if not isinstance(
        protobuf,
        (
            MissionRequest,
            MissionResponse,
            AgentUpdate,
            ObstaclesUpdate,
            ControllerFeedback,
            UnsafeSet,
            AutomatonOutput,
            CollisionMetrics
        ),
    ):
        raise TypeError("protobuf must be one of the defined types in the Union")

    try:
        return protobuf.SerializeToString()
    except Exception as e:
        raise Exception(f"Error serializing protobuf: {e}")
