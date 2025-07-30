#! /usr/bin/env python3
# coding: utf-8

import copy
import time
from collections import deque
from typing import Tuple, Optional

from kuavo_humanoid_sdk.kuavo.core.ros.param import make_robot_param, EndEffectorType
from kuavo_humanoid_sdk.common.logger import SDKLogger
from kuavo_humanoid_sdk.interfaces.data_types import (AprilTagData)
import roslibpy
from kuavo_humanoid_sdk.common.websocket_kuavo_sdk import WebSocketKuavoSDK

try:
    import rospy
    from std_msgs.msg import Float64
    from nav_msgs.msg import Odometry
    from sensor_msgs.msg import JointState
    from apriltag_ros.msg import AprilTagDetectionArray
    from geometry_msgs.msg import TransformStamped, PoseStamped
    import tf2_ros
    import tf2_geometry_msgs
except ImportError:
    pass

class KuavoRobotVisionCore:
    """Handles vision-related data processing for Kuavo humanoid robot.
    
    Attributes:
        tf_buffer (tf2_ros.Buffer): TF2 transform buffer
        tf_listener (tf2_ros.TransformListener): TF2 transform listener
        tf_broadcaster (tf2_ros.TransformBroadcaster): TF2 transform broadcaster
    """
    
    def __init__(self):
        """Initializes vision system components including TF and AprilTag subscribers."""
        if not hasattr(self, '_initialized'):
            self.tf_buffer = tf2_ros.Buffer()
            self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
            self.tf_broadcaster = tf2_ros.TransformBroadcaster()
            self._apriltag_data_camera_sub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self._apriltag_data_callback_camera)
            self._apriltag_data_base_sub = rospy.Subscriber('/robot_tag_info', AprilTagDetectionArray, self._apriltag_data_callback_base)

            # 添加TF2监听器
            self._tf_buffer = tf2_ros.Buffer()
            self._tf_listener = tf2_ros.TransformListener(self._tf_buffer)

            """ data """
            self._apriltag_data_from_camera = AprilTagData(
                id = [],
                size = [],
                pose = []
            )

            self._apriltag_data_from_base = AprilTagData(
                id = [],
                size = [],
                pose = []
            )

            self._apriltag_data_from_odom = AprilTagData(
                id = [],
                size = [],
                pose = []
            )

    def _apriltag_data_callback_camera(self, data):
        """Callback for processing AprilTag detections from camera.
        
        Args:
            data (AprilTagDetectionArray): Raw detection data from camera
        """
        # 清空之前的数据
        self._apriltag_data_from_camera.id = []
        self._apriltag_data_from_camera.size = []
        self._apriltag_data_from_camera.pose = []
        
        # 处理每个标签检测
        for detection in data.detections:
            # 添加ID
            for id in detection.id:
                self._apriltag_data_from_camera.id.append(id)
            
            # 添加尺寸 (从size数组中获取)
            if detection.size and len(detection.size) > 0:
                self._apriltag_data_from_camera.size.append(detection.size[0])
            else:
                self._apriltag_data_from_camera.size.append(0.0)
            
            # 添加姿态
            self._apriltag_data_from_camera.pose.append(detection.pose.pose.pose)
        # # debug
        # rospy.loginfo("Apriltag data from camera: %s", self._apriltag_data_from_camera)

    def _apriltag_data_callback_base(self, data):
        """Callback for processing AprilTag detections from base link.
        
        Args:
            data (AprilTagDetectionArray): Raw detection data from base frame
        """
        # 清空之前的数据
        self._apriltag_data_from_base.id = []
        self._apriltag_data_from_base.size = []
        self._apriltag_data_from_base.pose = []
        
        # 处理每个标签检测
        for detection in data.detections:
            # 添加ID
            for id in detection.id:
                self._apriltag_data_from_base.id.append(id)
            
            # 添加尺寸 (从size数组中获取)
            if detection.size and len(detection.size) > 0:
                self._apriltag_data_from_base.size.append(detection.size[0])
            else:
                self._apriltag_data_from_base.size.append(0.0)
            
            # 添加姿态
            self._apriltag_data_from_base.pose.append(detection.pose.pose.pose)

        # # debug
        # rospy.loginfo("Apriltag data from base: %s", self._apriltag_data_from_base)

        # 在基础数据处理完后，尝试进行odom坐标系的变换
        self._transform_base_to_odom()

    def _transform_base_to_odom(self):
        """Transforms AprilTag poses from base_link to odom coordinate frame.
        
        Performs:
            - Coordinate transformation using TF2
            - TF broadcasting for transformed poses
            - Data validation and error handling
            
        Raises:
            tf2_ros.LookupException: If transform is not available
            tf2_ros.ConnectivityException: If transform chain is broken
            tf2_ros.ExtrapolationException: If transform time is out of range
        """
        # 添加节点状态检查
        if rospy.is_shutdown():
            return
        
        # 清空之前的数据
        self._apriltag_data_from_odom.id = []
        self._apriltag_data_from_odom.size = []
        self._apriltag_data_from_odom.pose = []
        
        # 如果base数据为空，则不处理
        if not self._apriltag_data_from_base.id:
            SDKLogger.warn("No base tag data, skip transform")
            return
        
        try:
            # 获取从base_link到odom的变换
            transform = self._tf_buffer.lookup_transform(
                "odom",             
                "base_link",        
                rospy.Time(0),      
                rospy.Duration(1.0) 
            )
            
            # 复制ID和尺寸信息
            self._apriltag_data_from_odom.id = self._apriltag_data_from_base.id.copy()
            self._apriltag_data_from_odom.size = self._apriltag_data_from_base.size.copy()
            
            # 对每个姿态进行变换
            for idx, (tag_id, pose) in enumerate(zip(self._apriltag_data_from_base.id, self._apriltag_data_from_base.pose)):
                # 创建PoseStamped消息
                pose_stamped = PoseStamped()
                pose_stamped.header.frame_id = "base_link"
                pose_stamped.header.stamp = rospy.Time.now()
                pose_stamped.pose = pose
                
                # 执行变换
                transformed_pose = tf2_geometry_msgs.do_transform_pose(pose_stamped, transform)
                
                # 将变换后的姿态添加到odom数据中
                self._apriltag_data_from_odom.pose.append(transformed_pose.pose)
                
                # 创建并广播TF
                transform_stamped = TransformStamped()
                transform_stamped.header.stamp = rospy.Time.now()
                transform_stamped.header.frame_id = "odom"
                transform_stamped.child_frame_id = f"tag_odom_{tag_id}"
                transform_stamped.transform.translation.x = transformed_pose.pose.position.x
                transform_stamped.transform.translation.y = transformed_pose.pose.position.y
                transform_stamped.transform.translation.z = transformed_pose.pose.position.z
                transform_stamped.transform.rotation = transformed_pose.pose.orientation
                
                # 发送变换前再次检查节点状态
                if not rospy.is_shutdown():
                    self.tf_broadcaster.sendTransform(transform_stamped)
                
        except (tf2_ros.LookupException, 
               tf2_ros.ConnectivityException,
               tf2_ros.ExtrapolationException,
               rospy.ROSException) as e:  # 添加ROSException捕获
            SDKLogger.warn(f"TF变换异常: {str(e)}")
    
    @property 
    def apriltag_data_from_camera(self) -> AprilTagData:
        """AprilTag detection data in camera coordinate frame.
        
        Returns:
            AprilTagData: Contains lists of tag IDs, sizes and poses
        """
        return self._apriltag_data_from_camera
    
    @property
    def apriltag_data_from_base(self) -> AprilTagData:
        """AprilTag detection data in base_link coordinate frame.
        
        Returns:
            AprilTagData: Contains lists of tag IDs, sizes and poses
        """
        return self._apriltag_data_from_base
    
    @property
    def apriltag_data_from_odom(self) -> AprilTagData:
        """AprilTag detection data in odom coordinate frame.
        
        Returns:
            AprilTagData: Contains lists of tag IDs, sizes and transformed poses
        """
        return self._apriltag_data_from_odom

    def _get_data_by_id(self, target_id: int, data_source: str = "base") -> Optional[dict]:
        """Retrieves AprilTag data by specific ID from selected source.
        
        Args:
            target_id (int): AprilTag ID to search for
            data_source (str): Data source selector, valid options: 
                "camera", "base", "odom"
        
        Returns:
            Optional[dict]: Dictionary containing 'sizes' and 'poses' lists if found,
                None if no matching data
        
        Raises:
            ValueError: If invalid data_source is specified
        """
        data_map = {
            "camera": self._apriltag_data_from_camera,
            "base": self._apriltag_data_from_base,
            "odom": self._apriltag_data_from_odom
        }
        
        if data_source not in data_map:
            SDKLogger.error(f"Invalid data source: {data_source}, must be one of {list(data_map.keys())}")
            return None
        
        data = data_map[data_source]
        
        # 查找所有匹配的索引
        indices = [i for i, tag_id in enumerate(data.id) if tag_id == target_id]
        
        if not indices:
            SDKLogger.debug(f"No data found for tag ID {target_id} in {data_source} source")
            return None
        
        return {
            "sizes": [data.size[i] for i in indices],
            "poses": [data.pose[i] for i in indices]
        }

class KuavoRobotVisionCoreWebsocket:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            try:
                self.websocket = WebSocketKuavoSDK()
                if not self.websocket.client.is_connected:
                    SDKLogger.error("Failed to connect to WebSocket server")
                    raise ConnectionError("Failed to connect to WebSocket server")
                
                # Initialize subscribers for vision-related topics
                self._sub_apriltag_camera = roslibpy.Topic(self.websocket.client, '/tag_detections', 'apriltag_ros/AprilTagDetectionArray')
                self._sub_apriltag_base = roslibpy.Topic(self.websocket.client, '/robot_tag_info', 'apriltag_ros/AprilTagDetectionArray')
                
                # Initialize TF-related topics
                self._sub_tf = roslibpy.Topic(self.websocket.client, '/tf', 'tf2_msgs/TFMessage')
                self._sub_tf_static = roslibpy.Topic(self.websocket.client, '/tf_static', 'tf2_msgs/TFMessage')
                
                # Subscribe to topics
                self._sub_apriltag_camera.subscribe(self._apriltag_camera_callback)
                self._sub_apriltag_base.subscribe(self._apriltag_base_callback)
                self._sub_tf.subscribe(self._tf_callback)
                self._sub_tf_static.subscribe(self._tf_static_callback)
                
                # Initialize data structures
                self._apriltag_data_from_camera = AprilTagData(
                    id = [],
                    size = [],
                    pose = []
                )
                self._apriltag_data_from_base = AprilTagData(
                    id = [],
                    size = [],
                    pose = []
                )
                self._apriltag_data_from_odom = AprilTagData(
                    id = [],
                    size = [],
                    pose = []
                )
                
                # TF buffer for storing transforms
                self._tf_buffer = {}
                self._tf_static_buffer = {}
                
                self._initialized = True
            except Exception as e:
                SDKLogger.error(f"Failed to initialize KuavoRobotVisionCoreWebsocket: {e}")
                raise

    def _tf_callback(self, msg):
        """Callback for TF messages."""
        for transform in msg['transforms']:
            key = (transform['header']['frame_id'], transform['child_frame_id'])
            self._tf_buffer[key] = transform

    def _tf_static_callback(self, msg):
        """Callback for static TF messages."""
        for transform in msg['transforms']:
            key = (transform['header']['frame_id'], transform['child_frame_id'])
            self._tf_static_buffer[key] = transform

    def _get_transform(self, target_frame, source_frame):
        """Get transform between two frames.
        
        Args:
            target_frame (str): Target frame ID
            source_frame (str): Source frame ID
            
        Returns:
            dict: Transform data if found, None otherwise
        """
        # Check both dynamic and static transforms
        key = (source_frame, target_frame)
        if key in self._tf_buffer:
            return self._tf_buffer[key]
        if key in self._tf_static_buffer:
            return self._tf_static_buffer[key]
        return None

    def _transform_pose(self, pose, transform):
        """Transform a pose using the given transform.
        
        Args:
            pose (dict): Pose to transform
            transform (dict): Transform to apply
            
        Returns:
            dict: Transformed pose
        """
        # Extract transform components
        t = transform['transform']
        translation = t['translation']
        rotation = t['rotation']
        
        # Extract pose components
        p = pose['position']
        o = pose['orientation']
        
        # TODO: Implement actual pose transformation
        # This is a placeholder - actual implementation would involve
        # proper quaternion and vector math
        transformed_pose = {
            'position': {
                'x': p['x'] + translation['x'],
                'y': p['y'] + translation['y'],
                'z': p['z'] + translation['z']
            },
            'orientation': {
                'x': o['x'],
                'y': o['y'],
                'z': o['z'],
                'w': o['w']
            }
        }
        
        return transformed_pose

    def _apriltag_camera_callback(self, msg):
        """Callback for AprilTag detections in camera frame."""
        # Clear previous data
        self._apriltag_data_from_camera.id = []
        self._apriltag_data_from_camera.size = []
        self._apriltag_data_from_camera.pose = []
        
        # Process each detection
        for detection in msg['detections']:
            # Add ID
            for tag_id in detection['id']:
                self._apriltag_data_from_camera.id.append(tag_id)
            
            # Add size
            if detection.get('size') and len(detection['size']) > 0:
                self._apriltag_data_from_camera.size.append(detection['size'][0])
            else:
                self._apriltag_data_from_camera.size.append(0.0)
            
            # Add pose
            self._apriltag_data_from_camera.pose.append(detection['pose']['pose']['pose'])

    def _apriltag_base_callback(self, msg):
        """Callback for AprilTag detections in base frame."""
        # Clear previous data
        self._apriltag_data_from_base.id = []
        self._apriltag_data_from_base.size = []
        self._apriltag_data_from_base.pose = []
        
        # Process each detection
        for detection in msg['detections']:
            # Add ID
            for tag_id in detection['id']:
                self._apriltag_data_from_base.id.append(tag_id)
            
            # Add size
            if detection.get('size') and len(detection['size']) > 0:
                self._apriltag_data_from_base.size.append(detection['size'][0])
            else:
                self._apriltag_data_from_base.size.append(0.0)
            
            # Add pose
            self._apriltag_data_from_base.pose.append(detection['pose']['pose']['pose'])
        
        # Transform base data to odom frame
        self._transform_base_to_odom()

    def _transform_base_to_odom(self):
        """Transform AprilTag poses from base_link to odom coordinate frame."""
        # Clear previous odom data
        self._apriltag_data_from_odom.id = []
        self._apriltag_data_from_odom.size = []
        self._apriltag_data_from_odom.pose = []
        
        # If no base data, skip transformation
        if not self._apriltag_data_from_base.id:
            SDKLogger.warn("No base tag data, skip transform")
            return
        
        # Get transform from base_link to odom
        transform = self._get_transform("odom", "base_link")
        if not transform:
            SDKLogger.warn("Transform from base_link to odom not available")
            return
        
        # Copy ID and size information
        self._apriltag_data_from_odom.id = self._apriltag_data_from_base.id.copy()
        self._apriltag_data_from_odom.size = self._apriltag_data_from_base.size.copy()
        
        # Transform each pose
        for pose in self._apriltag_data_from_base.pose:
            transformed_pose = self._transform_pose(pose, transform)
            self._apriltag_data_from_odom.pose.append(transformed_pose)

    @property
    def apriltag_data_from_camera(self):
        return self._apriltag_data_from_camera
    
    @property
    def apriltag_data_from_base(self):
        return self._apriltag_data_from_base
    
    @property
    def apriltag_data_from_odom(self):
        return self._apriltag_data_from_odom

    def get_data_by_id(self, tag_id: int, frame: str = "odom"):
        """Get AprilTag data for a specific tag ID from the specified frame.
        
        Args:
            tag_id (int): The ID of the AprilTag to get data for
            frame (str): The frame to get data from ("camera", "base", or "odom")
            
        Returns:
            dict: The AprilTag data for the specified ID and frame, or None if not found
        """
        if frame == "camera":
            data = self._apriltag_data_from_camera
        elif frame == "base":
            data = self._apriltag_data_from_base
        elif frame == "odom":
            data = self._apriltag_data_from_odom
        else:
            SDKLogger.error(f"Invalid frame: {frame}")
            return None
            
        if not data or not data.id:
            return None
            
        # Find all matching indices
        indices = [i for i, id in enumerate(data.id) if id == tag_id]
        
        if not indices:
            return None
            
        return {
            "sizes": [data.size[i] for i in indices],
            "poses": [data.pose[i] for i in indices]
        }

# if __name__ == "__main__":

#     kuavo_robot_vision_core = KuavoRobotVisionCore()
#     time.sleep(5)
#     print("apriltag_data_from_camera:")
#     print(kuavo_robot_vision_core.apriltag_data_from_camera)
#     print("apriltag_data_from_base:")
#     print(kuavo_robot_vision_core.apriltag_data_from_base)
#     print("apriltag_data_from_odom:")
#     print(kuavo_robot_vision_core.apriltag_data_from_odom)
#     rospy.spin()