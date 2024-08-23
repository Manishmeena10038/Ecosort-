import os
import time
import picamera
import RPi.GPIO as GPIO

print("photo lo")
def capture_image(save_dir, filename):
    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Initialize the PiCamera
    with picamera.PiCamera() as camera:
        # Adjust camera settings if needed
        # camera.resolution = (1920, 1080)  # Set resolution
        # camera.rotation = 180             # Set rotation

        # Capture an image
        camera.start_preview()
        # Add a delay to allow the camera to adjust to light levels
        time.sleep(2)
        camera.capture(os.path.join(save_dir, filename))
        camera.stop_preview()

# Main function
def main():
    save_directory = "/home/pi/Desktop/GarbageDetection/PhotoOutput"
    filename = "image.jpg"  # Change filename as needed
    capture_image(save_directory, filename)
    print(f"Image captured and saved to {os.path.join(save_directory, filename)}")

if __name__ == "__main__":
    main()
    #model wait

print("run kr")
time.sleep(20)



def read_text_file(directory, filename):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {filename} does not exist in the directory {directory}.")
        return None

# Example usage
directory = '/home/pi/Desktop/GarbageDetection/TextInput'  # Replace this with the actual directory path
filename = 'prediction_output.txt'  # Replace this with the name of your text file
file_content = read_text_file(directory, filename)

if file_content is not None:

    print(file_content)

GPIO.setmode(GPIO.BOARD)  # corrected the parameter in setmode method
v=9
if(file_content=="Biodegradable"):
 controlPin = [11, 13, 15, 19]
else:
 controlPin = [29, 31, 33, 35]
for pin in controlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

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

for i in range(512):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(
                controlPin[pin], seq[halfstep][pin]
            )  # corrected 'ping' to 'pin'
        time.sleep(0.001)
        



GPIO.cleanup()



