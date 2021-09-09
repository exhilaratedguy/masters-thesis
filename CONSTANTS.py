from enum import Enum
import mediapipe as mp

mp_hands = mp.solutions.hands

#region HANDS CONSTANTS
MAX_NUM_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.8

class Poses(Enum):
    Fist = "Fist"
    One = "One"
    Two = "Two"
    Three = "Three"
    Four = "Four"
    Five = "Five"
    Okay = "Okay"
    Rock = "Rock"
    Spiderman = "Spiderman"
    Telephone = "Telephone"
    ERROR = "Error"

class Fingers(Enum):
    Thumb = mp_hands.HandLandmark.THUMB_MCP.value
    Index = mp_hands.HandLandmark.INDEX_FINGER_PIP.value
    Middle = mp_hands.HandLandmark.MIDDLE_FINGER_PIP.value
    Ring = mp_hands.HandLandmark.RING_FINGER_PIP.value
    Pinky = mp_hands.HandLandmark.PINKY_PIP.value
    Thumbtip = mp_hands.HandLandmark.THUMB_TIP.value
    Indextip = mp_hands.HandLandmark.INDEX_FINGER_TIP.value
#endregion


#region Mouse control type
class MouseControl(Enum):
    Raw = "Raw"
    Trackpad = "Trackpad"
    Vector = "Vector"
#endregion


#region Interface

THUMBNAIL_WIDTH = 200
THUMBNAIL_SPACING = 10

#endregion


#region Video Player

# For 480p resolution
#VIDEO_WIDTH = 852
#VIDEO_HEIGHT = 480
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

# Accounting for buttons and sliders underneath
HEIGHT_OFFSET = 50

# Overlay icon png codes
class ICONS(Enum):
    Play = 1
    Pause = 2
    VolumeUp = 3
    VolumeDown = 4

#endregion