import sqlite3
import cv2
import numpy as np
from recognizer import FaceRecognizer
import database as db

THRESHOLD = 0.7 

def _open_camera() -> cv2.VideoCapture | None:
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: cannot open camera.")
        return None
    return cam

def register_user(model: FaceRecognizer):
    name = input("\nNew user name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    cam = _open_camera()
    if cam is None: return

    POSES = ["Look straight", "Look left", "Look right", "Look up", "Look down"]
    SHOTS = 64
    
    print(f"\nRegistering: {name}")
    print("Follow instructions. Press Q to cancel.\n")

    conn = sqlite3.connect(db.DB_PATH)
    user_id = db.create_user(name, conn)
    
    for pose in POSES:
        print(f"  {pose}...")
        valid_shots = 0
        while valid_shots < SHOTS:
            ret, frame = cam.read()
            if not ret: break

            cv2.putText(frame, f"{pose} ({valid_shots + 1}/{SHOTS})", (30, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Registration", frame)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = model.detect(rgb_frame)
            
            if boxes is not None and len(boxes) > 0:
                face_img = model.crop_face(rgb_frame, boxes[0])
                if face_img:
                    embedding = model.embed(face_img)
                    db.save_face(user_id, face_img, embedding, conn)
                    valid_shots += 1
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        if cv2.waitKey(1) & 0xFF == ord("q"): break

    conn.commit()
    conn.close()
    cam.release()
    cv2.destroyAllWindows()
    print(f"User '{name}' registration finished.")

def run_recognition(model: FaceRecognizer):
    encodings = db.load_all_embeddings()
    if not encodings:
        print("\nBaza je prazna.")
        return

    cap = _open_camera()
    if cap is None: return
    
    print("\nRecognition running. Press Q to stop.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = model.detect(img_rgb)

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                face_img = model.crop_face(img_rgb, box)
                if face_img is None: continue

                embedding = model.embed(face_img)

                # Usporedba pomoću skalarnog produkta (dot product)
                best_match, best_score = "Unknown", THRESHOLD
                for person, person_encoding in encodings.items():
                    score = np.dot(embedding, person_encoding)
                    if score > best_score:
                        best_match = person
                        best_score = score

                # Crtanje rezultata
                label = f"{best_match} ({round(best_score * 100, 2)}%)"
                color = (0, 255, 0) if best_match != "Unknown" else (0, 0, 255)
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        else:
            cv2.putText(frame, "No face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def delete_user():
    name = input("\nUser name to delete: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
        
    if db.delete_user(name):
        print(f"User '{name}' deleted.")
    else:
        print(f"User '{name}' not found.")