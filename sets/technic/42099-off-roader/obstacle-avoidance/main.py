from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Port, Direction, Stop
from pybricks.tools import wait

# Initialize the motors and sensor.
steer = Motor(Port.C)
front = Motor(Port.A, Direction.COUNTERCLOCKWISE)
rear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
sensor = ColorDistanceSensor(Port.D)

# Lower the acceleration so the car starts and stops realistically.
front.control.limits(acceleration=1000)
rear.control.limits(acceleration=1000)

# Find the steering endpoint on the left and right. The difference
# between them is the total angle it takes to go from left to right.
# The middle is in between.
left_end = steer.run_until_stalled(-200, then=Stop.HOLD)
right_end = steer.run_until_stalled(200, then=Stop.HOLD)

# We are now at the right limit. We reset the motor angle to the
# limit value, so that the angle is 0 when the steering mechanism is
# centered.
limit = (right_end - left_end) // 2
steer.reset_angle(limit)
steer.run_target(speed=200, target_angle=0, then=Stop.COAST)


# Given a motor speed (deg/s) and a steering motor angle (deg), this
# function makes the car move at the desired speed and turn angle.
# The car keeps moving until you give another drive command.
def drive(drive_motor_speed, steer_angle):
    # Start running the drive motors
    front.run(drive_motor_speed)
    rear.run(drive_motor_speed)

    # Limit the steering value for safety, and then start the steer
    # motor.
    limited_angle = max(-limit, min(steer_angle, limit))
    steer.run_target(200, limited_angle, wait=False)


# Keep driving.
while True:
    # Turn around if an obstacle is detected.
    if sensor.distance() <= 70:

        # Pivot a few times.
        for i in range(2):
            # Backward left.
            drive(-800, -90)
            wait(2000)

            # Forward right.
            drive(800, 90)
            wait(1500)
    else:
        # Otherwise just keep driving forward.
        drive(800, 0)
