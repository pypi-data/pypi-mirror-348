from os.path import isdir
from shutil import rmtree
import argparse
from scipy.spatial.transform import Rotation
import rclpy
from rclpy.time import Time
from rclpy.serialization import serialize_message
from geometry_msgs.msg import PoseStamped, TwistStamped, AccelStamped
from rosbag2_py import SequentialWriter, StorageOptions, ConverterOptions, TopicMetadata

from .jpj_signals import jpj_signals


def write_ros2_bag(
    t, x, y, dx, dy, ddx, ddy, z, roll, pitch, yaw, output_path, overwrite=False
):
    # Get rotation
    q = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=True).as_quat()

    # Create rosbag writer
    if isdir(output_path):
        if not overwrite:
            raise Exception(
                "Output file already exist. Please specify another `output_path`, or `overwrite` the existing path"
            )
        rmtree(output_path)
    writer = SequentialWriter()
    storage_options = StorageOptions(uri=output_path, storage_id="sqlite3")
    converter_options = ConverterOptions(
        input_serialization_format="cdr", output_serialization_format="cdr"
    )
    writer.open(storage_options, converter_options)

    # Create topics
    writer.create_topic(
        TopicMetadata(
            name="/pose",
            type="geometry_msgs/msg/PoseStamped",
            serialization_format="cdr",
        )
    )
    writer.create_topic(
        TopicMetadata(
            name="/twist",
            type="geometry_msgs/msg/TwistStamped",
            serialization_format="cdr",
        )
    )
    writer.create_topic(
        TopicMetadata(
            name="/accel",
            type="geometry_msgs/msg/AccelStamped",
            serialization_format="cdr",
        )
    )

    # Convert signals to messages
    rclpy.init()
    for i in range(len(t)):
        # Create time
        time_ns = int(t[i] * 1e9)

        # Create pose
        pose = PoseStamped()
        pose.header.stamp = Time(
            seconds=int(t[i]), nanoseconds=int((t[i] % 1) * 1e9)
        ).to_msg()
        pose.header.frame_id = "base"
        pose.pose.position.x = float(x[i])
        pose.pose.position.y = float(y[i])
        pose.pose.position.z = float(z)
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        writer.write("/pose", serialize_message(pose), time_ns)

        # Create twist
        twist = TwistStamped()
        twist.header.stamp = pose.header.stamp
        twist.header.frame_id = "base"
        twist.twist.linear.x = float(dx[i])
        twist.twist.linear.y = float(dy[i])
        twist.twist.linear.z = 0.0  # Z velocity is 0
        twist.twist.angular.x = 0.0
        twist.twist.angular.y = 0.0
        twist.twist.angular.z = 0.0
        writer.write("/twist", serialize_message(twist), time_ns)

        # Create acceleration
        accel = AccelStamped()
        accel.header.stamp = pose.header.stamp
        accel.header.frame_id = "base"
        accel.accel.linear.x = float(ddx[i])
        accel.accel.linear.y = float(ddy[i])
        accel.accel.linear.z = 0.0  # Z acceleration is 0
        accel.accel.angular.x = 0.0
        accel.accel.angular.y = 0.0
        accel.accel.angular.z = 0.0
        writer.write("/accel", serialize_message(accel), time_ns)

    print(f"✅ ROS 2 bag file written to: {output_path}/{output_path}.bag")


def main():
    parser = argparse.ArgumentParser(
        prog="JPJ bag",
        description="Store JPJ symbol arcs' time signals in a ROS2 bag.",
        epilog="\N{COPYRIGHT SIGN} 2025 Vincenzo Petrone",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--frequency",
        metavar="F",
        type=float,
        default=1000,
        help="The frequency at which signals are generated [Hz]",
    )
    parser.add_argument(
        "-x",
        "--offset-x",
        metavar="X",
        type=float,
        default=0.0,
        help="x-offset [m]",
    )
    parser.add_argument(
        "-y",
        "--offset-y",
        metavar="Y",
        type=float,
        default=0.0,
        help="y-offset [m]",
    )
    parser.add_argument(
        "-r", "--radius", metavar="A", type=float, default=0.2, help="Arc radius [m]"
    )
    parser.add_argument(
        "-v",
        "--velocity",
        metavar="V",
        type=float,
        default=0.1,
        help="Max tangential velocity [m/s]",
    )
    parser.add_argument(
        "-z",
        "--z",
        metavar="Z",
        type=float,
        default=-0.1,
        help="Fixed z-coordinate for Pose [m]",
    )
    parser.add_argument(
        "-R", "--roll", metavar="R", type=float, default=90, help="Roll [°]"
    )
    parser.add_argument(
        "-P", "--pitch", metavar="P", type=float, default=0.0, help="Pitch [°]"
    )
    parser.add_argument(
        "-Y", "--yaw", metavar="Y", type=float, default=-90, help="Yaw [°]"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="B",
        type=str,
        default="jpj_bag",
        help="Output bag directory",
    )
    parser.add_argument(
        "-k",
        "--exist-ok",
        dest="overwrite",
        action="store_true",
        help="Overwrites output directory",
    )
    parser.add_argument(
        "-p", "--plot", action="store_true", help="Plot symbol and time signals"
    )
    args = parser.parse_args()

    # Generate trajectory
    t, x, y, dx, dy, ddx, ddy = jpj_signals(
        frequency=args.frequency,
        radius=args.radius,
        max_speed=args.velocity,
        show_plot=args.plot,
    )

    # Generate bag file
    write_ros2_bag(
        t,
        x,
        y,
        dx,
        dy,
        ddx,
        ddy,
        args.z,
        args.roll,
        args.pitch,
        args.yaw,
        args.output,
        args.overwrite,
    )


if __name__ == "__main__":
    main()
