import RPi.GPIO as GPIO
import time
import math

class Motor:
    """
    A class to control the motors of a two-wheeled robot using GPIO pins.
    Supports forward/backward motion with optional angle steering, and in-place rotation.
    """

    def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
        """
        Initializes motor control pins and sets up PWM for speed control.

        Args:
            ain1, ain2, ena: GPIO pins for right motor direction and enable.
            bin1, bin2, enb: GPIO pins for left motor direction and enable.
        """
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena
        self.ENB = enb

        # Calibration factors
        self.speed_calibration = 120.0  # seconds per cm at 100% speed CORRECTED
        self.angle_calibration = 2.75  # steering sensitivity
        
        self.x = 0.0  # current x position in cm
        self.y = 0.0  # current y position in cm
        self.heading = 0.0  # in degrees (0 = facing right / +X)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        self.pwmA = GPIO.PWM(self.ENA, 500)
        self.pwmB = GPIO.PWM(self.ENB, 500)
        self.pwmA.start(0)
        self.pwmB.start(0)

        self.stop()

    def _forward(self, speed, angle=0):
        """
        Internal method to move the robot forward with optional angle adjustment.
        """
        speed = max(0, min(100, speed))
        angle = max(-100, min(100, angle)) * self.angle_calibration

        left_speed = speed
        right_speed = speed

        if angle > 0:
            right_speed *= (1 - abs(angle) / 100)
        elif angle < 0:
            left_speed *= (1 - abs(angle) / 100)

        self.set_motor(left_speed, right_speed)

    def _backward(self, speed, angle=0):
        """
        Internal method to move the robot backward with optional angle adjustment.
        """
        speed = max(0, min(100, speed))
        angle = max(-100, min(100, angle)) * self.angle_calibration

        left_speed = -speed
        right_speed = -speed

        if angle > 0:
            right_speed *= (1 - abs(angle) / 100)
        elif angle < 0:
            left_speed *= (1 - abs(angle) / 100)

        self.set_motor(left_speed, right_speed)
        
    def move_distance(self, distance, duration, angle=0):
        """
        Rotates the robot in place to the given relative angle,
        then moves forward/backward for the specified distance and duration.

        Args:
            distance (float): Distance in cm (positive = forward, negative = backward).
            duration (float): Duration in seconds to complete the movement.
            angle (float): Relative angle in degrees (-180 to 180) to turn before moving.
        """
        if distance == 0 or duration <= 0:
            print("No movement needed or invalid duration.")
            return

        # --- Step 1: Rotate in place to desired angle ---
        angle = max(-180, min(180, angle))
        rotation_speed = 30  # You can tune this rotation speed

        if angle != 0:
            direction = 1 if angle > 0 else -1
            rotation_time = abs(angle) / (abs(self.angle_calibration) * 100)
            self.set_motor(-rotation_speed * direction, rotation_speed * direction)
            time.sleep(rotation_time)
            self.stop()

            # Update heading
            self.heading = (self.heading + angle) % 360

        # --- Step 2: Move straight ---
        speed = (abs(distance) / (self.speed_calibration * duration)) * 100
        speed = max(1, min(100, speed))

        if distance > 0:
            self._forward(speed)
        else:
            self._backward(speed)

        time.sleep(duration)
        self.stop()

        # --- Step 3: Update position ---
        rad = math.radians(self.heading)
        dx = distance * math.cos(rad)
        dy = distance * math.sin(rad)
        self.x += dx
        self.y += dy
        
        time.sleep(1)

        print(f"Moved to ({self.x:.2f}, {self.y:.2f}) at heading {self.heading:.2f}°")
     
    def move(self, target_x, target_y, duration):
        """
        Moves the robot in a straight line from its current position to the specified (x, y) position.
        The movement speed is calculated based on the given duration.

        Args:
            target_x (float): Target x-coordinate in cm.
            target_y (float): Target y-coordinate in cm.
            duration (float): Desired duration of movement in seconds.
        """
        # Calculate displacement
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)  # Euclidean distance

        if distance == 0:
            print("Already at the target position.")
            return

        # Calculate desired heading
        angle_to_target = math.degrees(math.atan2(dy, dx))
        angle_diff = (angle_to_target - self.heading) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Move to the new position
        self.move_distance(distance, duration, angle_diff)
        
        # Update heading
        self.set_heading(angle_to_target)
        
        # Update position
        self.x += dx
        self.y += dy
        
    def look_around(self, duration=2):
        """
        Rotates the robot in place for a given duration by calculating required speed.

        Args:
            duration (float): Time (in seconds) to complete the turn.
        """

        # Compute necessary speed to complete 360° in the given time
        speed = 0.55 / max(duration, 0.01) * 100
        print(speed)
        speed = max(0, min(100, speed))  # clamp to [0, 100]
        print(speed)
        self.set_motor(-speed, speed)
        time.sleep(duration)
        self.stop()

    def set_motor(self, left_speed, right_speed):
        """
        Directly sets the motor speeds. Positive = forward, negative = backward.

        Args:
            left_speed (float): Speed for the left motor (-100 to 100).
            right_speed (float): Speed for the right motor (-100 to 100).
        """
        if right_speed >= 0:
            GPIO.output(self.AIN1, GPIO.LOW)
            GPIO.output(self.AIN2, GPIO.HIGH)
        else:
            GPIO.output(self.AIN1, GPIO.HIGH)
            GPIO.output(self.AIN2, GPIO.LOW)
        self.pwmA.ChangeDutyCycle(min(abs(right_speed), 100))

        if left_speed >= 0:
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)
        else:
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(min(abs(left_speed), 100))

    def stop(self):
        """
        Immediately stops both motors.
        """
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def set_speed_calibration(self, factor):
        """
        Sets the speed calibration factor (sec/cm at 100% speed).

        Args:
            factor (float): New calibration value.
        """
        self.speed_calibration = factor

    def set_angle_calibration(self, factor):
        """
        Sets the angle calibration factor for steering sensitivity.

        Args:
            factor (float): New angle adjustment multiplier.
        """
        self.angle_calibration = factor
        
    def get_position(self):
        """
        Returns the current estimated (x, y) position in cm.
        """
        return self.x, self.y

    def set_position(self, x, y):
        """
        Manually sets the robot's (x, y) position in cm.
        Useful for resetting or correcting drift.
        """
        self.x = x
        self.y = y
        
    def set_heading(self, degrees):
        """Sets current heading (0–360°). 0 = facing +X, 90 = +Y."""
        self.heading = degrees % 360

    def get_heading(self):
        """Returns current heading in degrees."""
        return self.heading