import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread


# Parameter = 0 - uses main camera, Parameter = 1 - uses secondary camera attached
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

first_frame = None
time.sleep(1)

# Initialize the background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

status_list = [0]
count = 1


def clean_folder():
    print("clean")
    images = glob.glob("images/*.png")
    print(images)
    print(len(images))
    for image in images:
        os.remove(image)
    print("clean finish")


while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Apply the background subtractor to get the foreground mask
    fgmask = fgbg.apply(gray_frame_gau)
    thresh_frame = cv2.threshold(fgmask, 45, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
clean_thread.start()

