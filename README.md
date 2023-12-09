# Hand-Gesture-Controlled-Presentation
cvzone lib
# working video


https://github.com/Psrijith/Hand-Gesture-Controlled-Presentation/assets/118285872/5d3caca9-4fd8-43d7-aca8-3b2ef80ec0f3




This project is a gesture-based presentation control system using computer vision. It allows users to navigate through a presentation using hand gestures. Additionally, it supports a drawing feature, enabling users to annotate slides in real-time using their index finger.

Rules:
Slide Navigation:

Left Gesture: Extend your index finger while keeping the other fingers down to navigate to the previous slide.
Right Gesture: Extend your thumb while keeping the other fingers down to navigate to the next slide.
Pointer Mode:

Raise your index and middle fingers to activate the pointer mode. Move your hand to control the pointer on the screen.
Drawing Mode:

Raise your index finger and lower the rest to enter drawing mode. Move your hand to draw on the screen.
Erasing:

Make a fist to erase the drawn annotations.
How to Run:
Install Required Libraries:

Make sure you have the required libraries installed. You can install them using the following:
Copy code
pip install opencv-python
pip install mediapipe
pip install cvzone
Download Project Files:

Download the project files, including the presentation images and the HandTrackingModule from CVZone.
Run the Code:

Execute the Python script containing the project code.
Copy code
python your_script_name.py
Ensure that your camera is accessible, and you are in a well-lit environment.
Interact with Gestures:

Follow the rules mentioned above to navigate through slides, use the pointer, draw, and erase.
Libraries Used:
OpenCV: A computer vision library for image and video processing.
Mediapipe: A library for hand tracking and pose estimation.
CVZone: A computer vision library that extends OpenCV functionalities.
Note:
Make sure to adjust the path to the presentation folder in the script to match the location of your downloaded presentation images.

Feel free to customize and extend the functionality based on your requirements!
source :- (https://youtu.be/CKmAZss-T5Y?feature=shared)


# Draw on face , inspired from above video 

This hand-tracking drawing application utilizes OpenCV and the CVZone library, allowing users to create drawings on-screen through intuitive hand gestures. By raising three fingers, a pointer is displayed, while pointing two fingers dynamically changes the drawing color based on the color palette. The application enables drawing with the currently selected color using four fingers and offers an erasing function by raising all five fingers. Additionally, users can hold one finger on the desired color in the palette to select it. To run the project, install required libraries, download the CVZone library, and execute the Python script. Follow the defined rules for interaction and exit the application by pressing the 'Q' key. Ensure proper camera access and lighting conditions for optimal hand detection.
