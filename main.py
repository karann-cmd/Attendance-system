import cv2
from deepface import DeepFace
import os
import django
from datetime import datetime

# Django setup — database use karne ke liye
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from dashboard.models import Attendance

def mark_attendance(name):
    today = datetime.now().date()
    time_now = datetime.now().time()
    
    # Check karo — pehle se mark hai ya nahi
    already_marked = Attendance.objects.filter(name=name, date=today).exists()
    
    if not already_marked:
        Attendance.objects.create(
            name=name,
            date=today,
            time=time_now
        )
        print(f"✅ {name} ki attendance mark ho gayi!")
    else:
        print(f"⚠️ {name} pehle se mark hai!")

cap = cv2.VideoCapture(0)
print("System Start hai... Q dabao band karne ke liye")

while True:
    ret, frame = cap.read()
    
    try:
        result = DeepFace.find(
            img_path=frame,
            db_path="C:\\Users\\DELL\\Desktop\\Attendence",
            enforce_detection=False,
            model_name="VGG-Face",
            silent=True
        )
        
        if len(result) > 0 and len(result[0]) > 0:
            identity = result[0].iloc[0]["identity"]
            distance = result[0].iloc[0]["distance"]
            print(f"distance: {distance}")
            
            if distance < 0.4:
                name = os.path.basename(identity).split(".")[0]
                name = name.capitalize()
                mark_attendance(name)
                cv2.putText(frame, f"Present: {name}", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    except Exception as e:
        print(f"Error: {e}")
    
    cv2.imshow("Attendance System", frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()