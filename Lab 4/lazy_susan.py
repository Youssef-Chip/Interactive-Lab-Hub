import time
import qwiic_button
import pi_servo_hat

# Initialize the Qwiic Button
button = qwiic_button.QwiicButton()

# Initialize the SparkFun Servo pHAT
servo_hat = pi_servo_hat.PiServoHat()
servo_hat.restart()

# Set up variables
servo_channel = 0
is_facing_away = False

# Ensure starting position (facing you) and LED off
servo_hat.move_servo_position(servo_channel, 0)
button.LED_off()


try:
    while True:
        if button.is_button_pressed():
            if is_facing_away:
                print("Ad over. Rotating back to watch.")
                button.LED_off()
                
                # Sweep slowly from 180 back down to 0
                for angle in range(180, -1, -2):
                    servo_hat.move_servo_position(servo_channel, angle)
                    time.sleep(0.02)
                is_facing_away = False
            else:
                print("Ad playing. Rotating away.")
                button.LED_on(255) 
                
                # Sweep slowly from 0 up to 180
                for angle in range(0, 181, 2):
                    servo_hat.move_servo_position(servo_channel, angle)
                    time.sleep(0.02)
                is_facing_away = True
            
            # 0.5 second delay prevents double-triggering from a single tap
            time.sleep(0.5) 
        
        # Small delay to keep the loop running smoothly
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("\nStopping script")
    button.LED_off()