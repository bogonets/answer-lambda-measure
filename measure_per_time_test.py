import numpy as np
import cv2
import measure_per_time as mpt


def main():

    mpt.on_set(mpt.PROPS_NAME_SECONDS, "5")
    mpt.on_set(mpt.PROPS_NAME_LABELS, "No Helmet!")
    mpt.on_set(mpt.PROPS_NAME_MEASURE_COUNT, "5")
    mpt.on_set(mpt.PROPS_NAME_ALARM_INTERVAL_SECONDS, "3")

    if not mpt.on_init():
        print("Initialize Fail!")
        return

    while True:
        empty = np.zeros((500, 500, 3), np.int8)

        empty = cv2.putText(
            empty, str(mpt.states), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        empty = cv2.putText(
            empty, str(mpt.next_alarm_times), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        empty = cv2.putText(
            empty, str(mpt.cache_input), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("image", empty)
        key = cv2.waitKey(1)

        if key == 27:
            break
        elif key == ord('1'):
            mpt.on_run(np.array([1]))
        elif key == ord('2'):
            mpt.on_run(np.array([2]))
        elif key == ord('3'):
            mpt.on_run(np.array([3]))
        elif key == ord('4'):
            mpt.on_run(np.array([4]))
        else:
            mpt.on_run(np.array([]))


if __name__ == "__main__":
    main()
