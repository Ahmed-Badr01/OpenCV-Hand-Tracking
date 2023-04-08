from HandTrackingModule import HandDetector
import keyboard
import cv2

vid = cv2.VideoCapture(0)
vid.set(3, 1280)
vid.set(4, 720)

detector = HandDetector()

# current_time = 0
# last_twelve_fps_rates = [0 for x in range(12)]

finger_tips = [8, 12, 16, 20]
fingers_up = [0, 0, 0, 0, 0]

while True:
    success, frame = vid.read()
    frame = detector.detect_hands(frame)
    landmarks_list = detector.find_positions(frame, show_all=True)

    if landmarks_list:
        # finger is open if y pos. of its tip > that of its base
        for idx, tip in enumerate(finger_tips):
            if landmarks_list[tip][2] > landmarks_list[tip - 2][2]:
                fingers_up[idx + 1] = 0
            else:
                fingers_up[idx + 1] = 1
        # thumb is open if x pos. of its tip > that of its base
        if landmarks_list[4][1] > landmarks_list[2][1]:
            fingers_up[0] = 1
        else:
            fingers_up[0] = 0

    print(fingers_up)

    # previous_time = current_time
    # current_time = time.time()
    # fps = 1 / (current_time - previous_time)
    #
    # last_twelve_fps_rates.append(fps)
    # last_twelve_fps_rates.pop(0)
    # stabilized_fps = int(sum(last_twelve_fps_rates) / 12)

    # cv2.putText(frame, f'fps: {stabilized_fps}', (100, 100), cv2.FONT_ITALIC, 1.5, (255, 0, 0), 2)

    cv2.imshow('cam feed', frame)
    cv2.waitKey(1)

    if keyboard.is_pressed('q'):
        break

