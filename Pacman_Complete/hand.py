# FILE: hand_controller.py
import cv2
import mediapipe as mp
import threading
from constants import *

class HandController:
    def __init__(self):
        self.direction = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self.process_hand_gestures, daemon=True)
        self.thread.start()

    def process_hand_gestures(self):
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0)  # 0 for the default camera

        with self.lock:
            self.direction = None
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Flip and convert color space (BGR to RGB) for Mediapipe
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process frame and get hand landmarks
                result = hands.process(rgb_frame)

                # Draw landmarks and connections
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                        )

                        # Get index finger tip and base landmarks
                        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                        # Calculate pixel coordinates
                        height, width, _ = frame.shape
                        tip_x, tip_y = int(index_tip.x * width), int(index_tip.y * height)
                        base_x, base_y = int(index_base.x * width), int(index_base.y * height)

                        # Determine direction based on tip and base positions
                        if abs(tip_x - base_x) > abs(tip_y - base_y):  # Horizontal motion
                            if tip_x > base_x:
                                self.direction = RIGHT  # Use constant from constants.py
                                direction_text = "RIGHT"
                            else:
                                self.direction = LEFT
                                direction_text = "LEFT"
                        else:  # Vertical motion
                            if tip_y > base_y:
                                self.direction = DOWN
                                direction_text = "DOWN"
                            else:
                                self.direction = UP
                                direction_text = "UP"
                else:
                    with self.lock:
                        self.direction = None
                        direction_text = "NONE"

                # Vẽ thông tin hướng lên khung hình
                if self.direction is not None:
                    display_text = f"Direction: {direction_text}"
                else:
                    display_text = "Direction: NONE"

                cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 0, 255), 2, cv2.LINE_AA)

                # Display the frame
                cv2.imshow("Hand Pointing Direction", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def get_direction(self):
        with self.lock:
            return self.direction

    def stop(self):
        self.running = False
        self.thread.join()
