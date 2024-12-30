import cv2
import numpy as np
import dlib
from colorsys import rgb_to_hsv
from math import sqrt
import os

def click_data(event, x, y, flags, param):
    #print(hsv[y, x, 2])
    pass

def plen(p1, p2):
    x1 = point[p1][0]
    y1 = point[p1][1]
    x2 = point[p2][0]
    y2 = point[p2][1]

    return sqrt((x2-x1)**2 + (y2-y1)**2)

def face_shape(imgpath: str, show: bool = True, output_path: str = "user.png"):
    ########################################## FACE ##############################################
    # Load the detector
    detector = dlib.get_frontal_face_detector()

    # Load the predictor
    #predictor = dlib.shape_predictor("opencv/dat_sources/shape_predictor_68_face_landmarks.dat")

    predictor = dlib.shape_predictor("model/shape_predictor_81_face_landmarks.dat")

    # read the image
    global img
    img = cv2.imread(imgpath)
    if img is None:
        return

    # Convert image into grayscale
    global gray
    global hsv
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2HSV)

    # Use detector to find landmarks
    faces = detector(gray)
    face_exists = False
    for face in faces:
        x1 = face.left() # left point
        y1 = face.top() # top point
        x2 = face.right() # right point
        y2 = face.bottom() # bottom point

        # Create landmark object
        landmarks = predictor(image=gray, box=face)
        face_exists = True

    if not face_exists:
        return

    global point
    point = []
    for i in range(81):
        point.append([landmarks.part(i).x, landmarks.part(i).y])

    # skintone
    sx = point[27][0]
    sy = point[27][1]
    skinsum = 0
    for i in range(30):
        skinsum += hsv[sy, sx, 2]
        sy -= 1
    skintone = skinsum/30

    # Image masking
    lowerBound = np.array([0, 0, round(skintone * 0.8)])
    upperBound = np.array([180, 255, 255])
    global mask
    mask = cv2.inRange(hsv, lowerBound, upperBound)

    # cari forehead
    forehead = [76, 68, 69, 70, 71, 80, 72, 73, 79]
    
    # 68 - 81
    for n in forehead:
        x = point[n][0]
        y = point[n][1]

        while mask[y, x] == 255:
            y -= 1
            point[n][1] -= 1


    for i in range(81):
        x = point[i][0]
        y = point[i][1]

        cv2.circle(img=img, center=(x, y), radius=4, color=(0, 255, 0), thickness=-1)
        # cv2.putText(img=img, text= str(i), org=(x, y), fontFace= cv2.FONT_HERSHEY_SIMPLEX, color= (0, 0, 255), fontScale=0.7, thickness= 2)


    lines = []
    lengths = [
        plen(6, 10),
        plen(4, 12),
        plen(2, 14),
        plen(0, 16),
        plen(8, 22),
        plen(22, 71),
        (plen(70, 7) +
        plen(80, 9) +
        plen(68, 5) +
        plen(73, 11)) / 4
    ]
    jumlah = sum(lengths)
    for i in lengths:
        lines.append(round(i/jumlah, 4) * 100)

    if show:
        ratio = 2

        cv2.namedWindow("Face", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Face", 600, 600)

        # show the image
        cv2.imshow(winname="Face", mat=img)

        #cv2.setMouseCallback('Face',click_data)

        # Delay between every fram
        cv2.waitKey(delay=0)

        # Close all windows
        cv2.destroyAllWindows()


    # Save PNG
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 50]  

    cv2.imwrite(output_path, img, compression_params)
    

    # 11 elements, [0..10]
    return lines