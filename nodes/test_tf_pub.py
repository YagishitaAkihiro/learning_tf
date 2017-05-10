import tf2_ros
import geometry_msgs.msg as geometry_msgs

def tf_set_up():
    global tf_buffer, tf_listener, tf_broadcaster
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    #tf_broadcaster = tf2_ros.StaticTransformBroadcaster()
    import tf2_msgs.msg
    tf_broadcaster = rospy.Publisher("/tf_static", tf2_msgs.msg.TFMessage , queue_size=1, latch=True)

def broadcast_static_tf(parent, child, translation, rotation):
    static_tf = geometry_msgs.TransformStamped()
    static_tf.header.stamp = rospy.Time.now()
    static_tf.header.frame_id = parent
    static_tf.child_frame_id = child
    static_tf.transform.translation = translation
    static_tf.transform.rotation = rotation
    tf_broadcaster.publish([static_tf])

class Tf_publisher():
  def __init__(self):
        broadcast_static_tf('odom', 'initial_pose', pose[0], pose[1])

        #TODO: determine with measurement
        pose = geometry_msgs.PoseStamped()
        pose.header.frame_id = BASE_FRAME
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = DESIRED_DISTANCE
        pose.pose.position.y = 0.0
        pose.pose.orientation.w = 1.0
        try:
            pose = tf_buffer.transform(pose, MAP_FRAME, timeout=rospy.Duration(_TF_TIMEOUT))
            broadcast_static_tf(MAP_FRAME, BOOKCASE_FRAME, pose.pose.position, pose.pose.orientation)
        except:
            rospy.logerr('Could not transform bookcase position.')
