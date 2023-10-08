import RPi.GPIO as GPIO
import tkinter as tk
import time
import keyboard

output_pin1 = 32 
output_pin2 = 33
digout_pin1 = 15
digout_pin2 = 16

# Globally scoped variables
p1 = None
p2 = None

def main():
    configure_pwm()
    create_gui()

def configure_pwm()
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set PWM as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
    # set digitalOutput as an output pin with optional initial state of LOW
    GPIO.setup(digout_pin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(digout_pin2, GPIO.OUT, initial=GPIO.LOW)
    # create pwm objects
    p1 = GPIO.PWM(output_pin1, 25000)
    p2 = GPIO.PWM(output_pin2, 25000)

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Henry Control")

    # Create a frame to contain the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=20)

    # Create and configure buttons
    button_forward = tk.Button(button_frame, text="Forward", command=move("forward")
    button_right = tk.Button(button_frame, text="Right", command=move("right")
    button_left = tk.Button(button_frame, text="Left", command=move("left"))
    button_reverse = tk.Button(button_frame, text="Reverse", command=move("reverse")
    button_stop = tk.Button(button_frame, text="Stop", command=move("stop"))

    # Pack the buttons
    button_forward.pack(side=tk.LEFT, padx=10)
    button_right.pack(side=tk.LEFT, padx=10)
    button_left.pack(side=tk.LEFT, padx=10)
    button_reverse.pack(side=tk.LEFT, padx=10)
    button_stop.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter main loop
    root.mainloop()

def move(direction):
    # determine the direction and move accordingly
    stop() # This may not be needed or may cause bugs
    match direction:
        case "forward":
            # Need to check if activating PWM while it is already running will cause issues. If so, we need to check if PWM is active before calling this function
            GPIO.output(digout_pin1, GPIO.LOW) # These values need to be checked
            GPIO.output(digout_pin2, GPIO.LOW)
        case "left":
            GPIO.output(digout_pin1, GPIO.HIGH)
            GPIO.output(digout_pin2, GPIO.LOW)
        case "reverse":
            GPIO.output(digout_pin1, GPIO.HIGH)
            GPIO.output(digout_pin2, GPIO.HIGH)
        case "right":
            GPIO.output(digout_pin1, GPIO.LOW)
            GPIO.output(digout_pin2, GPIO.HIGH)
        case "stop" :
            stop()
        case _ :
            raise ValueError("This movement does not exist")
    activate_pwm() # Orient the direction first, and then activate pwm signal

def stop():
    p1.stop()
    p2.stop()
    
def activate_pwm():
    # start pwm
    p1.start(0)
    p2.start(0)
    print("PWM running. Press CTRL+C to exit.")
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)

if __name__ == "__main__":
    main()
        
        
                
