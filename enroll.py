"""
Run this once to enroll the administrator's face for BankGuard AI.

Usage:
    python enroll.py
"""

from security.face_auth import enroll_admin_face


def main() -> None:
    print("BankGuard AI - Administrator Face Enrollment")
    print("A camera window will open. Look at the camera and stay still.")
    print("Press ESC to cancel early.\n")

    success, message = enroll_admin_face(
        camera_index=0,
        capture_seconds=10,
    )

    if success:
        print(f"\n[OK] {message}")
    else:
        print(f"\n[FAILED] {message}")


if __name__ == "__main__":
    main()
