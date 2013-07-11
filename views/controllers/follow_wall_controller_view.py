#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg
from models.control_state import *

VECTOR_LEN = 0.75 # length of heading vector

FWDIR_LEFT = 0
FWDIR_RIGHT = 1

class FollowWallControllerView:

  def __init__( self, viewer, supervisor ):
    self.viewer = viewer
    self.supervisor = supervisor
    self.follow_wall_controller = supervisor.follow_wall_controller

  # draw a representation of the currently-active side of the follow-wall controller state to the frame
  def draw_active_follow_wall_controller_to_frame( self, frame ):
    # determine which side to renderi
    current_state = self.supervisor.state_machine.current_state
    if current_state == ControlState.SLIDE_LEFT:
      self._draw_follow_wall_controller_to_frame_by_side( frame, FWDIR_LEFT )
    elif current_state == ControlState.SLIDE_RIGHT:
      self._draw_follow_wall_controller_to_frame_by_side( frame, FWDIR_RIGHT )
    else: raise Exception( "applying follow-wall controller when not in a sliding state currently not supported" )

  # draw a representation of both sides of the follow-wall controller to the frame
  def draw_complete_follow_wall_controller_to_frame( self, frame ):
    self._draw_follow_wall_controller_to_frame_by_side( frame, FWDIR_LEFT )
    self._draw_follow_wall_controller_to_frame_by_side( frame, FWDIR_RIGHT )

  # draw the controller to the frame for the indicated side only 
  def _draw_follow_wall_controller_to_frame_by_side( self, frame, side ):
    if side == FWDIR_LEFT:
      surface_line = self.follow_wall_controller.l_wall_surface
      distance_vector = self.follow_wall_controller.l_distance_vector
      perpendicular_component = self.follow_wall_controller.l_perpendicular_component
      parallel_component = self.follow_wall_controller.l_parallel_component
      fw_heading_vector = self.follow_wall_controller.l_fw_heading_vector
    elif side == FWDIR_RIGHT:
      surface_line = self.follow_wall_controller.r_wall_surface
      distance_vector = self.follow_wall_controller.r_distance_vector
      perpendicular_component = self.follow_wall_controller.r_perpendicular_component
      parallel_component = self.follow_wall_controller.r_parallel_component
      fw_heading_vector = self.follow_wall_controller.r_fw_heading_vector
    else: raise Exception( "unrecognized argument: follow-wall direction indicator" )

    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

    # draw the estimated wall surface
    surface_line = linalg.rotate_and_translate_vectors( surface_line, robot_theta, robot_pos )
    frame.add_lines(  [ surface_line ],
                      linewidth = 0.01,
                      color = "black",
                      alpha = 1.0 )

    # draw the measuring line from the robot to the wall
    range_line = [ [ 0.0, 0.0 ], distance_vector ]
    range_line = linalg.rotate_and_translate_vectors( range_line, robot_theta, robot_pos )
    frame.add_lines(  [ range_line ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )

    # # draw the perpendicular component vector
    # perpendicular_component_line = [ [ 0.0, 0.0 ], perpendicular_component ]
    # perpendicular_component_line = linalg.rotate_and_translate_vectors( perpendicular_component_line, robot_theta, robot_pos )
    # frame.add_lines(  [ perpendicular_component_line ],
    #                   linewidth = 0.01,
    #                   color = "blue",
    #                   alpha = 0.8 )

    # # draw the parallel component vector
    # parallel_component_line = [ [ 0.0, 0.0 ], parallel_component ]
    # parallel_component_line = linalg.rotate_and_translate_vectors( parallel_component_line, robot_theta, robot_pos )
    # frame.add_lines(  [ parallel_component_line ],
    #                   linewidth = 0.01,
    #                   color = "red",
    #                   alpha = 0.8 )

    # draw the computed follow-wall vector
    fw_heading_vector = linalg.scale( linalg.unit( fw_heading_vector ), VECTOR_LEN )
    vector_line = [ [ 0.0, 0.0 ], fw_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.02,
                     color = "orange",
                     alpha = 1.0 )