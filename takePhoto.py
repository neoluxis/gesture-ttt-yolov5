import cv2


def main():
    total_pics = 1000
    cap = cv2.VideoCapture(0)

    pic_no = 0
    flag_start_capturing = False
    frames = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imwrite("hand_images/" + str(pic_no) + ".jpg", frame)
        cv2.imshow("Capturing gesture", frame)
        cv2.waitKey(10)
        pic_no += 1
        if pic_no == total_pics:
            break


main()