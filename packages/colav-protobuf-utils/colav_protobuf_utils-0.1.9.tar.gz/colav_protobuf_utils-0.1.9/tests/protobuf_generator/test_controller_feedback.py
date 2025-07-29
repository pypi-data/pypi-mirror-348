# from colav_protobuf_utils.protobuf_generator import (
#     gen_controller_feedback,
#     CtrlMode,
#     CtrlStatus,
# )
# from colav_protobuf.examples import controller_feedback
# from colav_protobuf_utils import Stamp
# import pytest


# def test_gen_controller_feedback():
#     """pytest assertion tests for generation of protobuf controller feedback"""
#     proto_utils_controller_feedback = gen_controller_feedback(
#         mission_tag=controller_feedback.mission_tag,
#         agent_tag=controller_feedback.agent_tag,
#         mode=CtrlMode(controller_feedback.mode),
#         status=CtrlStatus(controller_feedback.status),
#         velocity=controller_feedback.cmd.velocity,
#         yaw_rate=controller_feedback.cmd.yaw_rate,
#         stamp=Stamp(
#             sec = controller_feedback.stamp.sec,
#             nanosec=controller_feedback.stamp.nanosec
#         )
#     )

#     assert (
#         proto_utils_controller_feedback.mission_tag == controller_feedback.mission_tag
#     )
#     assert proto_utils_controller_feedback.agent_tag == controller_feedback.agent_tag
#     assert proto_utils_controller_feedback.mode == controller_feedback.mode
#     assert (
#         proto_utils_controller_feedback.status == controller_feedback.status
#     )
#     assert (
#         proto_utils_controller_feedback.cmd.velocity
#         == controller_feedback.cmd.velocity
#     )
#     assert (
#         proto_utils_controller_feedback.cmd.yaw_rate
#         == controller_feedback.cmd.yaw_rate
#     )
#     assert proto_utils_controller_feedback.stamp.sec == controller_feedback.stamp.sec
#     assert proto_utils_controller_feedback.stamp.nanosec == controller_feedback.stamp.nanosec
