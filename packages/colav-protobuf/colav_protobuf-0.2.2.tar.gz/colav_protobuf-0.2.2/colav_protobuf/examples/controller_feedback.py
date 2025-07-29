from colav_protobuf import ControllerFeedback

"""mocks controller feedback"""
controller_feedback = ControllerFeedback()
controller_feedback.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
controller_feedback.agent_tag = "EF12_WORKBOAT"
controller_feedback.mode = ControllerFeedback.CtrlMode.Value("CRUISE")
controller_feedback.status = ControllerFeedback.CtrlStatus.Value("ACTIVE")
controller_feedback.cmd.velocity = float(15.0)
controller_feedback.cmd.yaw_rate = float(0.2)

controller_feedback.stamp.sec = int(10000231)
controller_feedback.stamp.nanosec = int(1001230124)
