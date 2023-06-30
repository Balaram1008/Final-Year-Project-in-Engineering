import os
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Set the key length
key_length = 256

# Generate a secret key
secret_key = get_random_bytes(key_length // 8)

# Initialize the AES cipher in CBC mode
cipher = AES.new(secret_key, AES.MODE_CBC)

# Read the input video file
input_file = "input_video.mp4"
cap = cv2.VideoCapture(input_file)

# Initialize variables for motion vector computation
prev_frame = None
motion_vectors = []

# Process each frame of the video
while True:
    # Read the next frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Encrypt the frame using the secret key
    encrypted_frame = cipher.encrypt(gray_frame.tobytes())

    # Embed the message in the encrypted frame using LSB embedding
    message = "This is a secret message."
    message_bits = "".join(format(ord(c), "08b") for c in message)
    for j, bit in enumerate(message_bits):
        if j >= len(encrypted_frame) * 8:
            break
        byte_idx = j // 8
        bit_idx = j % 8
        mask = ~(1 << bit_idx)
        new_byte = (encrypted_frame[byte_idx] & mask) | (int(bit) << bit_idx)
        encrypted_frame = encrypted_frame[:byte_idx] + bytes([new_byte]) + encrypted_frame[byte_idx + 1:]

    # Compute the motion vector between this frame and the previous frame
    if prev_frame is not None:
        flow = cv2.calcOpticalFlowFarneback(prev_frame, gray_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        dx = flow[..., 0].mean()
        dy = flow[..., 1].mean()
        motion_vectors.append((dx, dy))

    # Update the previous frame
    prev_frame = gray_frame

    # Write the encrypted and embedded frame to a file
    with open("encrypted_video.bin", "ab") as f:
        f.write(encrypted_frame)

# Encrypt the motion vectors using the secret key
encrypted_motion_vectors = cipher.encrypt(str(motion_vectors).encode())

# Write the encrypted motion vectors to a file
with open("encrypted_motion_vectors.bin", "wb") as f:
    f.write(encrypted_motion_vectors)

# Decrypt and display the first frame of the encrypted video

# Read the first encrypted and embedded frame from the file
with open("encrypted_video.bin", "rb") as f:
    encrypted_frame = f.read(gray_frame.size)

# Decrypt the encrypted and embedded frame using the secret key
decrypted_frame = cipher.decrypt(encrypted_frame)

# Extract the embedded message from the decrypted frame using LSB extraction
extracted_bits = "".join(format(byte, "08b")[-1] for byte in decrypted_frame)
extracted_message = "".join(chr(int(extracted_bits[i:i + 8], 2)) for i in range(0, len(extracted_bits), 8))
print("Extracted message:", extracted_message)

# Convert the decrypted frame back to a grayscale image
decrypted_image = np.frombuffer(decrypted_frame, dtype=np.uint8).reshape(gray_frame.shape)

# Display the decrypted image
cv2.imshow("Decrypted Image", decrypted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
