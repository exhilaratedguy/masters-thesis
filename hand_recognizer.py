import CONSTANTS as CONSTANTS

import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands


def PrintException():
    import linecache
    import sys

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def getFingerPoint(hand):
    """
    Returns the X and Y coordinates of the index finger.
    :param hand: hand landmarks
    :return: int, int --> coordinate X, coordinate Y
    """

    x = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    y = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    return x, y


def getHandCenter(hand):
    """
    Returns the base point of the middle finger as the center X and Y coordinates of a hand.
    :param hand: hand landmarks
    :return: int, int --> coordinate X, coordinate Y
    """

    x = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
    y = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
    return x, y


def isFingerOpen(hand, n: int, right_hand=True):
    """
    Check if the finger n is extended.
    :param hand: Hand landmarks object
    :param n: finger's landmark PIP value
    :param right_hand: bool to indicate if treating the right hand, defaults to True
    :return: bool --> finger is extended
    """
    # https://google.github.io/mediapipe/images/mobile/hand_landmarks.png

    basePoint = hand.landmark[n]

    # Thumb closes horizontally (x axis)
    if n is 2:
        if right_hand:
            return hand.landmark[n + 1].x < basePoint.x and hand.landmark[n + 2].x < basePoint.x
        else:   # left hand
            return hand.landmark[n + 1].x > basePoint.x and hand.landmark[n + 2].x > basePoint.x

    # Other fingers close vertically (y axis)
    return hand.landmark[n + 1].y < basePoint.y and hand.landmark[n + 2].y < basePoint.y


def isThumbNearIndex(thumb_landmark_tip, index_landmark_tip):
    """
    Check if the fingers thumb and index are near each other.
    :param thumb_landmark_tip: thumb's fingertip landmark value
    :param index_landmark_tip: index's fingertip landmark value
    :return: bool --> fingers' tips are near each other
    """
    thumb = np.array((thumb_landmark_tip.x, thumb_landmark_tip.y))
    index = np.array((index_landmark_tip.x, index_landmark_tip.y))
    return np.linalg.norm(thumb - index) < 0.1


def calculateFingers(hand, right_hand=True):
    """
    Returns if the operation was successful and the the number of fingers extended.
    :param hand: Hand landmarks object
    :param right_hand: bool to indicate if treating the right hand, defaults to True
    :return: bool, int --> operation was successful, number of fingers extended
    """
    # Save which fingers are open as booleans
    try:
        thumb = isFingerOpen(hand, CONSTANTS.Fingers.Thumb.value, right_hand)
        index = isFingerOpen(hand, CONSTANTS.Fingers.Index.value, right_hand)
        middle = isFingerOpen(hand, CONSTANTS.Fingers.Middle.value, right_hand)
        ring = isFingerOpen(hand, CONSTANTS.Fingers.Ring.value, right_hand)
        pinky = isFingerOpen(hand, CONSTANTS.Fingers.Pinky.value, right_hand)
    except Exception:
        return False, -1

    # True equals 1 so this will return the number of fingers open
    return True, sum([thumb, index, middle, ring, pinky])


def getHandGesture(hand, right_hand=True):
    """
    Returns the gesture the hand is performing as a string.
    :param hand: Hand landmarks object
    :param right_hand: bool to indicate if treating the right hand, defaults to True
    :return: str --> name of the gesture
    """
    try:
        # Save which fingers are open as booleans
        thumb_is_open = isFingerOpen(hand, CONSTANTS.Fingers.Thumb.value, right_hand)
        index_is_open = isFingerOpen(hand, CONSTANTS.Fingers.Index.value, right_hand)
        middle_is_open = isFingerOpen(hand, CONSTANTS.Fingers.Middle.value, right_hand)
        ring_is_open = isFingerOpen(hand, CONSTANTS.Fingers.Ring.value, right_hand)
        pinky_is_open = isFingerOpen(hand, CONSTANTS.Fingers.Pinky.value, right_hand)

        # Boolean for
        thumb_and_index_touching = isThumbNearIndex(hand.landmark[CONSTANTS.Fingers.Thumbtip.value],
                                                    hand.landmark[CONSTANTS.Fingers.Indextip.value])

        # Hand pose recognition
        if not thumb_is_open and not index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
            return CONSTANTS.Poses.Fist       # fist
        elif not thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
            return CONSTANTS.Poses.One        # one
        elif not thumb_is_open and index_is_open and middle_is_open and not ring_is_open and not pinky_is_open:
            return CONSTANTS.Poses.Two        # two
        elif not thumb_is_open and index_is_open and middle_is_open and ring_is_open and not pinky_is_open:
            return CONSTANTS.Poses.Three      # three
        elif not thumb_is_open and index_is_open and middle_is_open and ring_is_open and pinky_is_open:
            return CONSTANTS.Poses.Four       # four
        elif thumb_is_open and index_is_open and middle_is_open and ring_is_open and pinky_is_open:
            return CONSTANTS.Poses.Five       # five
        elif not index_is_open and middle_is_open and ring_is_open and pinky_is_open and thumb_and_index_touching:
            return CONSTANTS.Poses.Okay       # okay
        elif not thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and pinky_is_open:
            return CONSTANTS.Poses.Rock       # rock
        elif thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and pinky_is_open:
            return CONSTANTS.Poses.Spiderman  # spiderman
        elif thumb_is_open and not index_is_open and not middle_is_open and not ring_is_open and pinky_is_open:
            return CONSTANTS.Poses.Telephone  # telephone
        else:
            return CONSTANTS.Poses.ERROR
    except Exception:
        print("\tgetHandGesture")
        PrintException()