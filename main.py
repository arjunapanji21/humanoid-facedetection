import cv2
from time import sleep

# SERVO
from ax12 import Ax12

Ax12.open_port()
Ax12.set_baudrate()

SERV1 = Ax12(1)
SERV2 = Ax12(2)
SERV3 = Ax12(3) # kepala
SERV4 = Ax12(4)
SERV5 = Ax12(5)
SERV6 = Ax12(6)

# initial value
cap = cv2.VideoCapture(2)
cascPath = "wajah.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

def posisi_siap():
    SERV1.set_position(830)
    SERV2.set_position(512)
    SERV3.set_position(512)
    SERV4.set_position(512)
    SERV5.set_position(215)
    SERV6.set_position(215)

def turun_tangan():
    SERV1.set_position(830)
    SERV2.set_position(512)
    SERV4.set_position(512)
    SERV5.set_position(215)
    SERV6.set_position(215)

def angkat_tangan():
    SERV1.set_position(830)
    SERV2.set_position(512)
    SERV4.set_position(512)
    SERV5.set_position(715)
    SERV6.set_position(415)

count = 0

while True:
    # Read the image
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect object in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around object
    for (x, y, w, h) in faces:
        count = 20
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cenX = int((x+x+w)/2)
        cenY = int((y+y+h)/2)
        print(cenX)
        # cv2.circle(frame, (cenX, cenY), 10, (0, 255, 0), 2)
        angkat_tangan()

        if(cenX > 320+50):
            pos = SERV3.get_position()
            if(pos > 200):
                SERV3.set_position(pos-5)
        elif(cenX < 320-50):
            pos = SERV3.get_position()
            if(pos < 800):
                SERV3.set_position(pos+5)
        # else:
        #     SERV3.set_position(512)
        break


    if (count > 0):
        count -= 1
        if (count <= 0):
            posisi_siap()

    cv2.imshow("Deteksi", frame)

    # press q to quit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break