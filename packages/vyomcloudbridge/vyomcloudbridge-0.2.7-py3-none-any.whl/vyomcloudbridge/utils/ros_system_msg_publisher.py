import importlib
import json
import rclpy
from rclpy.node import Node
from rosidl_runtime_py import set_message_fields
from vyomcloudbridge.constants import topics_list
from vyomcloudbridge.utils.logger_setup import setup_logger


class RosSystemMsgPublisher(Node):
    def __init__(self):
        self.logger = setup_logger(
            name=self.__class__.__module__ + "." + self.__class__.__name__,
            show_terminal=False,
        )
        try:
            rclpy.init(args=None)
        except Exception as e:
            self.logger.warning(f"Failed to initialize ROS: {e}")
        super().__init__("ros_system_msg_publisher")
        self.msg_publishers = {}  # { topic_name : (publisher, msg_instance) }
        self.logger.info("ROS System Message Publisher Node started.")
        self._is_destroyed = False

    def get_message_class(self, msg_name):
        """Try to load message class from available packages."""
        for package in topics_list.MSG_PKGS:
            try:
                module = importlib.import_module(f"{package}.msg")
                msg_class = getattr(module, msg_name)
                self.logger.info(
                    f"Loaded message '{msg_name}' from package '{package}'"
                )
                return msg_class
            except (ModuleNotFoundError, AttributeError):
                continue
        raise AttributeError(
            f"Message '{msg_name}' not found in any of: {topics_list.MSG_PKGS}"
        )

    def setup_publisher(self, typ, msg_data):
        msg_class = self.get_message_class(typ)
        topic_name = typ.lower()

        publisher = self.create_publisher(msg_class, topic_name, 10)

        msg_instance = msg_class()
        if isinstance(msg_data, dict):
            try:
                set_message_fields(msg_instance, msg_data)
            except Exception as e:
                self.logger.error(f"Failed to set message fields: {e}")
                return
        else:
            if hasattr(msg_instance, "data"):
                msg_instance.data = msg_data
            else:
                self.logger.error(f"Provided 'msg' is not valid for message type {typ}")
                return

        self.msg_publishers[topic_name] = (publisher, msg_instance)
        self.logger.info(
            f"Publisher created for topic: '{topic_name}' with message type: '{msg_class.__module__}.{typ}'"
        )

    def publish_all(self):
        for topic, (publisher, msg_instance) in self.msg_publishers.items():
            publisher.publish(msg_instance)
            self.logger.info(f"Published on '{topic}': {msg_instance}")

    def spin_once(self, timeout_sec=1.0):
        """Spin once to allow time for ROS graph to recognize publishers."""
        if self._is_destroyed:
            self.logger.error("Cannot spin: Node has been destroyed")
            return
        try:
            rclpy.spin_once(self, timeout_sec=timeout_sec)
        except Exception as e:
            self.logger.error(f"Error in rclpy.spin_once: {e}")

    def cleanup(self, shutdown_ros=False):  # dont shutdown rclpy by default
        """Clean up resources. Optionally shut down ROS."""
        try:
            self.destroy_node()
            self._is_destroyed = True
            self.logger.info("Node destroyed successfully")
        except Exception as e:
            self.logger.error(f"Error in destroying node: {e}")

        if shutdown_ros:
            try:
                rclpy.shutdown()
                self.logger.info("ROS shutdown completed")
            except Exception as e:
                self.logger.error(f"Error during ROS shutdown: {e}")


def main(args=None):
    ros_msg_publisher = RosSystemMsgPublisher()

    input_json = """
    [
        {
            "typ": "MissionStatus",
            "msg": {
                "mission_id": 42,
                "mission_status": 1,
                "user_id": 101,
                "bt_id": "navigate_tree",
                "mission_feedback": "Mission is currently in progress."
            }
        },
        {
            "typ": "Dvid",
            "msg": {"device_id": 5005}
        },
        {
            "typ": "Auth",
            "msg": {"auth_key": "sample_auth_key"}
        },
        {
            "typ": "Accessinfo",
            "msg": {
                "end_time": 1714321230,
                "current_date": 1714321220,
                "user_id": 1001
            }
        },
        {
            "typ": "Access",
            "msg": {"encrypted": "sample_encrypted_text"}
        },
        {
            "typ": "Ack",
            "msg": {"msgid": "msg001", "chunk_id": 10}
        }
    ]
    """
    input_data = json.loads(input_json)

    for item in input_data:
        ros_msg_publisher.setup_publisher(item["typ"], item["msg"])

    # Allow time for ROS graph to recognize publishers before publishing
    # rclpy.spin_once(ros_msg_publisher, timeout_sec=1.0) # TODO deepak, check on this, all functionality should be inside functions

    ros_msg_publisher.publish_all()
    ros_msg_publisher.cleanup(shutdown_ros=True)


if __name__ == "__main__":
    main()
