import tkinter as tk

speed = 0

def speed_increaser():
    # Create the main window
    root = tk.Tk()
    root.title("Henry Control")

    # Create a frame to contain the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=20)

    # Create and configure buttons
    # Note: The lambda function is used to pass a parameter to the function called by the button
    # Note: IN THE FUTURE, the command parameters should call functions that change the robot's state
    button_forward = tk.Button(button_frame, text="Forward", command=lambda: robot.set_state(States.MOVING_FORWARD))
    button_reverse = tk.Button(button_frame, text="Reverse", command=lambda: robot.set_state(States.MOVING_BACKWARD))
    button_left = tk.Button(button_frame, text="Left", command=lambda: robot.set_state(States.TURNING_LEFT))

    # Pack the buttons
    button_forward.pack(side=tk.LEFT, padx=10)
    button_reverse.pack(side=tk.LEFT, padx=10)
    button_left.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter main loop
    root.mainloop()

speed_increaser()