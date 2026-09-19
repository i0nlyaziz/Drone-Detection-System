import cv2
from ultralytics import YOLO
import sqlite3
import datetime
import time


conn = sqlite3.connect("DataBase.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS info (Id integer primary key , Drone text , Confidence real , Screenshot text , Date text)""")
conn.commit()

state = {}
timer = {}

model = YOLO('best.pt',task='detect')

cam = cv2.VideoCapture(0)

while True:
    ret , frame = cam.read()
    if not ret:
        break
    results = model.track(frame,persist=True,tracker='bytetrack.yaml',verbose=False)
    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf = float(box.conf[0])
            class_id = int(box.cls[0])

            if conf < 0.65:
                continue

            if box.id is None:
                continue

            track_id = int(box.id)

            if track_id not in state:
                state[track_id] = {"Date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   "Drone":"No",
                                   "Screenshot":"No"}

            if class_id == 0:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),1)
                if track_id not in timer:
                    timer[track_id] = time.time()
                duration = time.time() - timer[track_id]
                print(duration)

                if duration >= 3 and state[track_id]['Screenshot'] == "No":
                    crop = frame[y1:y2,x1:x2]
                    cv2.imwrite(f"Warning_Crop_{track_id}.jpg",crop)
                    cv2.imwrite(f"Warning_Full_{track_id}.jpg",frame)
                    state[track_id]['Drone'] = "Yes"
                    state[track_id]['Screenshot'] = "Yes"

                    cursor.execute("""insert into info(Drone,Confidence,Screenshot,Date) values(?,?,?,?)""",(state[track_id]['Drone'],conf,state[track_id]['Screenshot'],state[track_id]['Date']))
                    conn.commit()
            else:
                state[track_id]['Drone'] = 'No'
                state[track_id]['Screenshot'] = "No"
                timer.pop(track_id,None)

    cv2.imshow("webcam",frame)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
        
conn.close()
cam.release()
cv2.destroyAllWindows()