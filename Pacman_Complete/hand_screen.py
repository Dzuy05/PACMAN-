import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_gesture(hand_landmarks, width, height):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    height, width = int(height), int(width)

    if (index_tip.y > index_mcp.y and middle_tip.y > middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y):
        return "FIST"  

    if index_tip.y < index_mcp.y and middle_tip.y > middle_mcp.y:
        return "1"

    if index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y:
        return "2"

    return "NONE"
