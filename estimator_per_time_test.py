import cv2

def main():

    while True:
        empty = np.zeros((500, 500, 3), np.int8)

        fps = get_fps()
        empty = cv2.putText(
            empty, str(fps), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("image", empty)
        key = cv2.waitKey(1)

        if key == 27:
            break
        elif key == ord('1'):
            on_run(['1'])


if __name__ == "__main__":
    main()
