import cv2
import numpy as np

def noting(x):
    pass

cv2.namedWindow("frame")
cv2.createTrackbar("H","frame",0,179,noting)
cv2.createTrackbar("s","frame",255,255,noting)
cv2.createTrackbar("v","frame",255,255,noting)

img_hsv = np.zeros((250,500,3),np.uint8)

while True:
    h = cv2.getTrackbarPos("H","frame")

    s = cv2.getTrackbarPos("S","frame")
    v = cv2.getTrackbarPos("V","frame")

    img_hsv[:] = (h,s,v)
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow("Frame",img_bgr)
    key =  cv2.waitKey(1)
    if key ==ord('q'):
            break

cv2.destroyAllWindows()
