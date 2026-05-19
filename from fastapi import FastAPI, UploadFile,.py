from fastapi import FastAPI, UploadFile, File
import uvicorn
import face_recognition
import numpy as np
import cv2

app = FastAPI()

# ==========================================================
# FACE VERIFICATION API
# ==========================================================

@app.post("/verify-face/")
async def verify_face(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    # ================= READ IMAGE 1 =================
    image1_bytes = await image1.read()

    nparr1 = np.frombuffer(image1_bytes, np.uint8)

    img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)

    rgb1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    # ================= READ IMAGE 2 =================
    image2_bytes = await image2.read()

    nparr2 = np.frombuffer(image2_bytes, np.uint8)

    img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

    rgb2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # ================= DETECT FACES =================
    face_locations1 = face_recognition.face_locations(rgb1)

    face_locations2 = face_recognition.face_locations(rgb2)

    # ================= CHECK FACE EXISTS =================
    if len(face_locations1) == 0:
        return {"error": "No face found in image1"}

    if len(face_locations2) == 0:
        return {"error": "No face found in image2"}

    # ================= FACE ENCODINGS =================
    encoding1 = face_recognition.face_encodings(
        rgb1,
        face_locations1
    )[0]

    encoding2 = face_recognition.face_encodings(
        rgb2,
        face_locations2
    )[0]

    # ================= COMPARE FACES =================
    result = face_recognition.compare_faces(
        [encoding1],
        encoding2
    )

    # ================= DISTANCE =================
    face_distance = face_recognition.face_distance(
        [encoding1],
        encoding2
    )

    similarity_score = round((1 - face_distance[0]) * 100, 2)

    verification = (
        "same person"
        if result[0]
        else "different person"
    )

    # ================= RETURN RESPONSE =================
    return {
        "verification_result": verification,
        "similarity_score": f"{similarity_score}%",
        "image1_face_locations": face_locations1,
        "image2_face_locations": face_locations2
    }


# ==========================================================
# RUN FASTAPI SERVER
# ==========================================================

if _name_ == "_main_":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
