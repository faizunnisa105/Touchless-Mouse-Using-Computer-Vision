import cv2
import mediapipe as mp
import pyautogui
import random
import time
import util
from pynput.mouse import Button, Controller

mouse = Controller()

screen_width, screen_height = pyautogui.size()

# ---------------- HAND DETECTION ----------------
mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# ---------------- SETTINGS ----------------
last_action_time = 0
cooldown = 0.7

# Cursor smoothing
previous_x = 0
previous_y = 0
smooth_factor = 0.3


# ---------------- FIND INDEX FINGER ----------------
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]

        index_finger_tip = hand_landmarks.landmark[
            mpHands.HandLandmark.INDEX_FINGER_TIP
        ]

        return index_finger_tip

    return None


# ---------------- MOVE MOUSE ----------------
def move_mouse(index_finger_tip):

    global previous_x, previous_y

    if index_finger_tip is not None:

        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)

        # Smooth movement
        smooth_x = int(
            previous_x + (x - previous_x) * smooth_factor
        )

        smooth_y = int(
            previous_y + (y - previous_y) * smooth_factor
        )

        pyautogui.moveTo(smooth_x, smooth_y)

        previous_x = smooth_x
        previous_y = smooth_y


# ---------------- CLICK CONDITIONS ----------------
def is_left_click(landmark_list, thumb_index_dist):

    return (
        util.get_angle(
            landmark_list[5],
            landmark_list[6],
            landmark_list[8]
        ) < 50
        and
        util.get_angle(
            landmark_list[9],
            landmark_list[10],
            landmark_list[12]
        ) > 90
        and
        thumb_index_dist > 50
    )


def is_right_click(landmark_list, thumb_index_dist):

    return (
        util.get_angle(
            landmark_list[9],
            landmark_list[10],
            landmark_list[12]
        ) < 50
        and
        util.get_angle(
            landmark_list[5],
            landmark_list[6],
            landmark_list[8]
        ) > 90
        and
        thumb_index_dist > 50
    )


def is_double_click(landmark_list, thumb_index_dist):

    return (
        util.get_angle(
            landmark_list[5],
            landmark_list[6],
            landmark_list[8]
        ) < 50
        and
        util.get_angle(
            landmark_list[9],
            landmark_list[10],
            landmark_list[12]
        ) < 50
        and
        thumb_index_dist > 50
    )


def is_screenshot(landmark_list, thumb_index_dist):

    return (
        util.get_angle(
            landmark_list[5],
            landmark_list[6],
            landmark_list[8]
        ) < 50
        and
        util.get_angle(
            landmark_list[9],
            landmark_list[10],
            landmark_list[12]
        ) < 50
        and
        thumb_index_dist < 50
    )


# ---------------- SCROLL ----------------
def scroll_mouse(landmark_list):

    if len(landmark_list) < 21:
        return False

    index_y = landmark_list[8][1]
    middle_y = landmark_list[12][1]

    # Both fingers extended
    index_angle = util.get_angle(
        landmark_list[5],
        landmark_list[6],
        landmark_list[8]
    )

    middle_angle = util.get_angle(
        landmark_list[9],
        landmark_list[10],
        landmark_list[12]
    )

    if index_angle > 90 and middle_angle > 90:

        if index_y < 0.35 and middle_y < 0.35:
            pyautogui.scroll(3)
            return True

        elif index_y > 0.65 and middle_y > 0.65:
            pyautogui.scroll(-3)
            return True

    return False


# ---------------- ACTION COOLDOWN ----------------
def can_perform_action():

    global last_action_time

    current_time = time.time()

    if current_time - last_action_time > cooldown:

        last_action_time = current_time
        return True

    return False


# ---------------- GESTURE DETECTION ----------------
def detect_gesture(frame, landmark_list, processed):

    if len(landmark_list) < 21:
        return

    index_finger_tip = find_finger_tip(processed)

    thumb_index_dist = util.get_distance(
        [landmark_list[4], landmark_list[5]]
    )

    # -------- MOUSE MOVEMENT --------
    if (
        thumb_index_dist < 50
        and
        util.get_angle(
            landmark_list[5],
            landmark_list[6],
            landmark_list[8]
        ) > 90
    ):

        move_mouse(index_finger_tip)

        cv2.putText(
            frame,
            "MOVE",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # -------- SCROLL --------
    elif scroll_mouse(landmark_list):

        cv2.putText(
            frame,
            "SCROLL",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

    # -------- LEFT CLICK --------
    elif is_left_click(landmark_list, thumb_index_dist):

        if can_perform_action():

            mouse.press(Button.left)
            mouse.release(Button.left)

        cv2.putText(
            frame,
            "LEFT CLICK",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # -------- RIGHT CLICK --------
    elif is_right_click(landmark_list, thumb_index_dist):

        if can_perform_action():

            mouse.press(Button.right)
            mouse.release(Button.right)

        cv2.putText(
            frame,
            "RIGHT CLICK",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # -------- DOUBLE CLICK --------
    elif is_double_click(landmark_list, thumb_index_dist):

        if can_perform_action():

            pyautogui.doubleClick()

        cv2.putText(
            frame,
            "DOUBLE CLICK",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

    # -------- SCREENSHOT --------
    elif is_screenshot(landmark_list, thumb_index_dist):

        if can_perform_action():

            im1 = pyautogui.screenshot()

            label = random.randint(1, 1000)

            im1.save(
                f"my_screenshot_{label}.png"
            )

        cv2.putText(
            frame,
            "SCREENSHOT",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )


# ---------------- MAIN ----------------
def main():

    draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    try:

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            frameRGB = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            processed = hands.process(frameRGB)

            landmark_list = []

            if processed.multi_hand_landmarks:

                hand_landmarks = processed.multi_hand_landmarks[0]

                draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mpHands.HAND_CONNECTIONS
                )

                for lm in hand_landmarks.landmark:

                    landmark_list.append(
                        (lm.x, lm.y)
                    )

            detect_gesture(
                frame,
                landmark_list,
                processed
            )

            cv2.imshow(
                "Touchless Mouse",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()