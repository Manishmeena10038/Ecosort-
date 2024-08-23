import os
import time
import picamera
import RPi.GPIO as GPIO

# Function to capture an image
def capture_image(capture_images, filename):
    # Ensure the directory exists
    if not os.path.exists(capture_images):
        os.makedirs(capture_images)

    # Initialize the PiCamera
    with picamera.PiCamera() as camera:
        # Adjust camera settings if needed
        camera.resolution = (1920, 1080)  # Set resolution
        # camera.rotation = 180             # Set rotation

        # Capture an image
        camera.start_preview()
        # Add a delay to allow the camera to adjust to light levels
        time.sleep(2)
        camera.capture(os.path.join(capture_images, filename))
        camera.stop_preview()

# Function to read content from a text file
def read_text_file(directory, filename):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {filename} does not exist in the directory {directory}.")
        return None

# Main function
def main():
    capture_imagesectory = "/home/pi/Desktop/GarbageDetection/PhotoOutput"  # Directory to save captured images
    filename = "image.jpg"  # Name of the captured image file

    # Set up the IR sensor pin
    ir_sensor_pin = 7  # Define the GPIO pin connected to the IR sensor
    GPIO.setmode(GPIO.BOARD)  # Set GPIO mode to BOARD
    GPIO.setup(ir_sensor_pin, GPIO.IN)  # Set IR sensor pin as input

    # Wait for object detection via IR sensor
    print("Waiting for object detection...")
    try:
        while True:
            if GPIO.input(ir_sensor_pin) == GPIO.LOW:  # Detect object presence
                print("Object detected! Capturing image...")
                capture_image(capture_imagesectory, filename)  # Capture image when object is detected
                print(f"Image captured and saved to {os.path.join(capture_imagesectory, filename)}")
                break
            time.sleep(0.1)  # Small delay to prevent CPU overload
    except KeyboardInterrupt:
        print("Interrupted by user")

    # Read the content from the prediction output text file
    directory = '/home/pi/Desktop/GarbageDetection/TextInput'  # Directory containing the prediction output text file
    text_filename = 'prediction_output.txt'  # Name of the prediction output text file
    file_content = read_text_file(directory, text_filename)  # Read content from the text file

    if file_content is not None:
        print(file_content)  # Print the content of the text file

        # Define GPIO pins for different materials based on the file content
        if file_content == "BIODEGRADABLE":
            control_pins = [11, 13, 15, 19]
        elif file_content in ["CARDBOARD", "GLASS", "METAL", "PAPER", "PLASTIC"]:
            control_pins = [29, 31, 33, 35]
        else:
            control_pins = []

        if control_pins:
            # Initialize GPIO pins
            for pin in control_pins:
                GPIO.setup(pin, GPIO.OUT)  # Set control pins as output
                GPIO.output(pin, 0)  # Set initial state to LOW

            # Define the sequence for the stepper motor
            seq = [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1],
            ]

            # Rotate the stepper motor
            for i in range(512):  # Number of steps
                for halfstep in range(8):  # Half-step sequence
                    for pin in range(4):  # Iterate over control pins
                        GPIO.output(control_pins[pin], seq[halfstep][pin])  # Set pin state
                    time.sleep(0.001)  # Small delay for motor step timing

            GPIO.cleanup()  # Clean up GPIO settings

if __name__ == "__main__":
    main()  # Run the main function


