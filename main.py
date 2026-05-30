
import cv2
import cvzone
import numpy as np
import psycopg2
import pickle
from datetime import datetime


conn = psycopg2.connect(
    dbname="parking_db",
    user="postgres",
    password="sql",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

width, height = 107, 48

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

def vehicle_enters(vehicle_id, entry_time):
    
    cursor.execute("INSERT INTO parked_vehicles (vehicle_id, entry_time) VALUES (%s, %s)", (vehicle_id, entry_time))
    conn.commit()
    print("Vehicle entered. Entry time recorded.")

def vehicle_exits(vehicle_id, entry_time):
    
    exit_time = datetime.now()
    cursor.execute("UPDATE parked_vehicles SET exit_time = %s, parking_duration = %s WHERE vehicle_id = %s AND exit_time IS NULL", (exit_time, exit_time - entry_time, vehicle_id))
    conn.commit()
    print("Vehicle exited. Exit time recorded.")

cap = cv2.VideoCapture('carPark.mp4')

prev_spaceCounter = 0

while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    spaceCounter = 0
    for pos in posList:
        imgCrop = imgThreshold[pos[1]:pos[1] + height, pos[0]:pos[0] + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Free: {(spaceCounter)}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    
    
    key = cv2.waitKey(10)
    if key == ord('q'):  # Press 'q' to quit
        break

    
    if spaceCounter != prev_spaceCounter:
        if spaceCounter < prev_spaceCounter:  # Vehicle exited
            vehicle_exits("ABC123", datetime.now())
        else:  # Vehicle entered
            vehicle_enters("ABC123", datetime.now())
    
    prev_spaceCounter = spaceCounter


cursor.close()
conn.close()
cap.release()
cv2.destroyAllWindows()



