import os
import time
import cv2
import numpy as np
import logging

# OpenCV may emit non-fatal DNN backend warnings on newer builds.
# Keep the real face-recognition errors visible while suppressing
# noisy OpenCV warning messages.
logging.getLogger("cv2").setLevel(logging.ERROR)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DETECTOR_MODEL = os.path.join(
    BASE_DIR,
    "models",
    "face_detection_yunet_2023mar.onnx",
)

RECOGNIZER_MODEL = os.path.join(
    BASE_DIR,
    "models",
    "face_recognition_sface_2021dec.onnx",
)

FACE_DATA_DIR = os.path.join(BASE_DIR, "data", "face_auth")
FACE_TEMPLATE = os.path.join(FACE_DATA_DIR, "admin_face.npy")

# SFace cosine similarity threshold.
# A higher value is stricter.
FACE_MATCH_THRESHOLD = 0.363


def _load_models():
    if not os.path.exists(DETECTOR_MODEL):
        raise FileNotFoundError(
            f"Face detector model not found: {DETECTOR_MODEL}"
        )

    if not os.path.exists(RECOGNIZER_MODEL):
        raise FileNotFoundError(
            f"Face recognition model not found: {RECOGNIZER_MODEL}"
        )

    detector = cv2.FaceDetectorYN.create(
        DETECTOR_MODEL,
        "",
        (320, 320),
        0.9,
        0.3,
        5000,
    )

    recognizer = cv2.FaceRecognizerSF.create(
        RECOGNIZER_MODEL,
        "",
    )

    return detector, recognizer


def _largest_face(faces):
    if faces is None or len(faces) == 0:
        return None

    faces = np.asarray(faces)

    areas = faces[:, 2] * faces[:, 3]

    return faces[int(np.argmax(areas))]


def _get_face_embedding(frame, detector, recognizer):
    height, width = frame.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(frame)

    face = _largest_face(faces)

    if face is None:
        return None

    aligned_face = recognizer.alignCrop(
        frame,
        face,
    )

    feature = recognizer.feature(
        aligned_face
    )

    return feature


def enroll_admin_face(
    camera_index: int = 0,
    capture_seconds: int = 5,
) -> tuple[bool, str]:

    os.makedirs(FACE_DATA_DIR, exist_ok=True)

    detector, recognizer = _load_models()

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        return False, "Unable to open the camera."

    best_feature = None
    start_time = time.time()

    try:
        while time.time() - start_time < capture_seconds:

            success, frame = camera.read()

            if not success:
                continue

            feature = _get_face_embedding(
                frame,
                detector,
                recognizer,
            )

            if feature is not None:
                best_feature = feature

            cv2.imshow(
                "BankGuard AI - Face Enrollment",
                frame,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    if best_feature is None:
        return False, "No face was detected. Enrollment cancelled."

    np.save(
        FACE_TEMPLATE,
        best_feature,
    )

    return True, "Administrator face enrolled successfully."


def verify_admin_face(
    camera_index: int = 0,
    verification_seconds: int = 8,
) -> tuple[bool, str]:

    if not os.path.exists(FACE_TEMPLATE):
        return False, "No administrator face has been enrolled."

    detector, recognizer = _load_models()

    reference_feature = np.load(
        FACE_TEMPLATE
    )

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        return False, "Unable to open the camera."

    start_time = time.time()
    best_score = -1.0

    try:
        while time.time() - start_time < verification_seconds:

            success, frame = camera.read()

            if not success:
                continue

            feature = _get_face_embedding(
                frame,
                detector,
                recognizer,
            )

            if feature is not None:

                score = recognizer.match(
                    reference_feature,
                    feature,
                    cv2.FaceRecognizerSF_FR_COSINE,
                )

                best_score = max(
                    best_score,
                    float(score),
                )

                if best_score >= FACE_MATCH_THRESHOLD:
                    return True, (
                        "Administrator face verified "
                        f"(score: {best_score:.3f})."
                    )

            cv2.imshow(
                "BankGuard AI - Face Verification",
                frame,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    return False, (
        "Face verification failed "
        f"(best score: {best_score:.3f})."
    )
