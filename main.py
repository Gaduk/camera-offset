import numpy as np
import cv2 as cv
import time
import datetime

ESC_KEY_CODE = 27


def detect_offset(delay):
    cap = cv.VideoCapture(0)
    cap.read()
    ret, frame = cap.read()

    if not ret:
        print('Невозможно получить кадр')

    previous_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    while 1:
        ret, frame = cap.read()
        if not ret:
            print('Невозможно получить кадр')
            break
        next_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        (x_offset, y_offset), _ = cv.phaseCorrelate(previous_frame.astype(np.float32), next_frame.astype(np.float32))
        offset = np.sqrt(x_offset**2 + y_offset**2)

        if offset >= 5:
            print(f"[{datetime.datetime.now()}] Обнаружено смещение камеры")

        cv.imshow('Camera', next_frame)
        if cv.waitKey(1) == ESC_KEY_CODE:
            cap.release()
            cv.destroyAllWindows()

        previous_frame = next_frame
        time.sleep(delay)


if __name__ == '__main__':
    detect_offset(0.5)
