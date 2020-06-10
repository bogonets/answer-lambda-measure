import numpy as np
import cv2
import estimator_fps as fps

def main():

    while True:
        empty = np.zeros((500, 500, 3), np.int8)

        empty = cv2.putText(
            empty, str(fps.get_fps()), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("image", empty)
        key = cv2.waitKey(1)

        if key == 27:
            break
        elif key == ord('1'):
            fps.on_run([])


if __name__ == "__main__":
    main()
