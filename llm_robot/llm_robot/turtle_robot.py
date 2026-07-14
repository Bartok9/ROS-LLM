#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa
#
# Copyright 2023 Herman Ye @Auromix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Description:
# This example demonstrates simulating function calls for any robot,
# such as controlling velocity and other service commands.
# By modifying the content of this file,
# A calling interface can be created for the function calls of any robot.
# The Python script creates a ROS 2 Node
# that controls the movement of the TurtleSim
# by creating a publisher for cmd_vel messages and a client for the reset service.
# It also includes a ChatGPT function call server
# that can call various functions to control the TurtleSim
# and return the result of the function call as a string.
#
# Author: Herman Ye @Auromix

# ROS related
import rclpy
from rclpy.node import Node
from llm_interfaces.srv import ChatGPT
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

# LLM related
import json
from llm_config.user_config import UserConfig
from llm_robot.cmd_vel_sanitize import sanitize_cmd_vel_float

# Global Initialization
config = UserConfig()


class TurtleRobot(Node):
    def __init__(self):
        super().__init__("turtle_robot")
        # Client for reset
        self.reset_client = self.create_client(Empty, "/reset")
        # Publisher for cmd_vel
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        while not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service /reset not available, waiting again...")
        # Server for function call
        self.function_call_server = self.create_service(
            ChatGPT, "/ChatGPT_function_call_service", self.function_call_callback
        )
        # Node initialization log
        self.get_logger().info("TurtleRobot node has been initialized")

    def function_call_callback(self, request, response):
        req = json.loads(request.request_text)
        function_name = req["name"]
        function_args = json.loads(req["arguments"])
        func_obj = getattr(self, function_name)
        try:
            function_execution_result = func_obj(**function_args)
        except Exception as error:
            self.get_logger().info(f"Failed to call function: {error}")
            response.response_text = str(error)
        else:
            response.response_text = str(function_execution_result)
        return response

    def publish_cmd_vel(self, **kwargs):
        """
        Publishes cmd_vel message to control the movement of turtlesim
        """
        linear_x = sanitize_cmd_vel_float(kwargs.get("linear_x", 0.0), "linear_x")
        linear_y = sanitize_cmd_vel_float(kwargs.get("linear_y", 0.0), "linear_y")
        linear_z = sanitize_cmd_vel_float(kwargs.get("linear_z", 0.0), "linear_z")
        angular_x = sanitize_cmd_vel_float(kwargs.get("angular_x", 0.0), "angular_x")
        angular_y = sanitize_cmd_vel_float(kwargs.get("angular_y", 0.0), "angular_y")
        angular_z = sanitize_cmd_vel_float(kwargs.get("angular_z", 0.0), "angular_z")

        twist_msg = Twist()
        twist_msg.linear.x = linear_x
        twist_msg.linear.y = linear_y
        twist_msg.linear.z = linear_z
        twist_msg.angular.x = angular_x
        twist_msg.angular.y = angular_y
        twist_msg.angular.z = angular_z

        self.publisher_.publish(twist_msg)
        self.get_logger().info(f"Publishing cmd_vel message successfully: {twist_msg}")
        return twist_msg

    def reset_turtlesim(self, **kwargs):
        """
        Resets the turtlesim to its initial state and clears the screen
        """
        empty_req = Empty.Request()
        try:
            future = self.reset_client.call_async(empty_req)
            response_text = "Reset turtlesim successfully"
        except Exception as error:
            self.get_logger().info(f"Failed to reset turtlesim: {error}")
            return str(error)
        else:
            return response_text


def main():
    rclpy.init()
    turtle_robot = TurtleRobot()
    rclpy.spin(turtle_robot)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
