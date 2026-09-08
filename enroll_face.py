from security.face_auth import enroll_admin_face

print("Starting BankGuard AI face enrollment...")
print("Look directly at the camera.")
print("Press ESC to cancel.")

success, message = enroll_admin_face()

print(message)
