from RightHand.righthand import RightHand
from LeftHand.lefthand import LeftHand
import CONSTANTS

import pyrealsense2 as rs
import mediapipe as mp
import numpy as np
import cv2
import pyautogui


def main(aMainWindow, notifier):
    # Get the user's screen resolution
    screen_res = pyautogui.size()

    # Initialize the realsense pipeline
    pipeline = rs.pipeline()

    # Initialize and enable the depth stream at 30 fps
    """config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)"""
    try:
        cam = cv2.VideoCapture(0)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        quit(-1)

    # Initialize both hand classes
    right_hand = RightHand(screen_res, CONSTANTS.MouseControl.Trackpad)
    left_hand = LeftHand(aMainWindow, notifier)

    # Initialize the solution to track hands
    mp_hands = mp.solutions.hands

    # Initialize the solution to draw hand skeleton
    mp_drawing = mp.solutions.drawing_utils

    cv2.namedWindow("Video Feed", cv2.WINDOW_NORMAL)

    with mp_hands.Hands(
            max_num_hands=CONSTANTS.MAX_NUM_HANDS,
            min_detection_confidence=CONSTANTS.MIN_DETECTION_CONFIDENCE) as hands:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to get frame from camera")
                quit(-1)

            # Colorize the depth frame and transform it to a numpy array
            frame_data = np.asanyarray(frame)

            # Flip the image around y-axis for correct handedness output
            image = cv2.flip(frame_data, 1)

            # To improve performance, optionally mark the image as not writeable to pass by reference
            image.flags.writeable = False
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # To draw the hand annotations on the image
            image.flags.writeable = True

            # If a hand is in frame
            # Store which hand is 'left' and which is 'right'
            if results.multi_handedness:
                # Get the first hand and turn its classification info to a string object
                # Looks like the following:
                """classification {
                  index: 1
                  score: 0.9999889135360718
                  label: "Right"
                }"""
                # With max_num_hands=2 the left hand will always have
                # the label 'index: 0' and right hand always 'index: 1'
                first_hand = str(results.multi_handedness[0])
                #print(results.multi_handedness[0])

                # If the object of the first hand contains 'label: "Right"'
                if "Right" in first_hand:
                    # Processes relative to right hand and mouse control
                    right_hand.run(results.multi_hand_landmarks[0], image)

                    # Draw skeleton on frame
                    mp_drawing.draw_landmarks(
                        image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

                    # Detect if 2nd hand is in frame
                    try:
                        # Will raise an IndexError exception if 2nd hand is not in the frame
                        results.multi_handedness[1]

                        # Draw skeleton on frame
                        mp_drawing.draw_landmarks(
                            image, results.multi_hand_landmarks[1], mp_hands.HAND_CONNECTIONS)

                        # If there's a 2nd hand then it's the LEFT hand
                        left_hand.run(results.multi_hand_landmarks[1], image)
                    except IndexError:
                        pass
                # This means that the hand has 'label: "Left"'
                else:
                    # Processes relative to the left hand and gestures prediction
                    left_hand.run(results.multi_hand_landmarks[0], image)

                    # Draw skeleton on frame
                    mp_drawing.draw_landmarks(
                        image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

                    # Detect if 2nd hand is in frame
                    try:
                        # Will raise an IndexError exception if 2nd hand is not in the frame
                        results.multi_handedness[1]

                        # Draw skeleton on frame
                        mp_drawing.draw_landmarks(
                            image, results.multi_hand_landmarks[1], mp_hands.HAND_CONNECTIONS)

                        # If there's a 2nd hand then it's the RIGHT hand
                        right_hand.run(results.multi_hand_landmarks[1], image)
                    except IndexError:
                        pass

            cv2.imshow("Video Feed", image)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:   # ESC
                break
    # Free up memory
    pipeline.stop()
    cv2.destroyAllWindows()


"""if __name__ == '__main__':
    main()"""
