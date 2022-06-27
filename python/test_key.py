import cv2
import numpy as np

#frame = np.full((360, 480, 3), 0, dtype=int)
frame = cv2.imread("/home/pi/Pictures/2020-07-20_1439.jpg")
cv2.imshow("Frame", frame)

while True:
    key = cv2.waitKey(1)
    if key != -1:
        print("Key", key)
    if key == ord("q"):  # up key
        break

