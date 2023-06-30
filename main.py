# Video Encryption Decryption

# imported necessary library
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
import random
import os
from cv2 import *
from moviepy.editor import *


# Main Window & Configuration
window = tk.Tk() # created a tkinter gui window frame
window.title("Video Encryption Decryption") # title given is "DICTIONARY"
window.geometry('1000x700')

# top label
start1 = tk.Label(text = "VIDEO  ENCRYPTION WITH MESSAGE \nEMBEDDING AND MOTION VECTOR", font=("Arial", 35,"underline"), fg="black") # same way bg
start1.place(x = 120, y = 10)

def start_fun():
    window.destroy()

# start button created
startb = Button(window, text="START",command=start_fun,font=("Arial", 25), bg = "orange", fg = "blue", borderwidth=3, relief="raised")
startb.place(x =150 , y =580 )

# image on the main window
path = "Images/front.jpg"
# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img1 = ImageTk.PhotoImage(Image.open(path))
# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img1)
panel.place(x = 130, y = 230)

# function created for exiting
def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# exit button created
exitb = Button(window, text="EXIT",command=exit_win,font=("Arial", 25), bg = "red", fg = "blue", borderwidth=3, relief="raised")
exitb.place(x =730 , y = 580 )
window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

# Main Window & Configuration
window1 = tk.Tk() # created a tkinter gui window frame
window1.title("Video Encryption Decryption") # title given is "DICTIONARY"
window1.geometry('1000x700')

# function to select file
def open_file():
    global filename
    filename = filedialog.askopenfilename(title="Select file")
    # print(filename)
    path_text.delete("1.0", "end")
    path_text.insert(END, filename)

# function to encrypt video and show encrypted video
def encrypt_fun():
    global filename
    global key_entry
    path_list = []
    message= 'secret key'
    key_length=80
    key = int(key_entry.get())

    cap = cv2.VideoCapture(filename)

    # Initialize variables for motion vectors and frames
    _, frame1 = cap.read()
    prev_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    motion_vectors = []

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_pixels = width * height
    scrambled_indices = np.random.permutation(num_pixels)

    # Extract motion vectors between frames
    while (cap.isOpened()):
        ret, frame2 = cap.read()
        if ret == True:
            curr_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev_frame, curr_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            motion_vectors.append(flow)
            prev_frame = curr_frame
        else:
            break

    # Convert the message to binary
    message_bin = ''.join(format(ord(i), '08b') for i in message)

    # Generate a random permutation of the motion vector indices
    np.random.seed(key)
    perm = np.random.permutation(len(motion_vectors))

    # Embed the message bits into the motion vector bits
    for i in range(len(message_bin)):
        mv_index = perm[i % len(perm)]
        mv = motion_vectors[mv_index]
        mv = mv.astype(np.int32)  # convert mv to np.int32
        x = np.random.randint(0, mv.shape[1])
        y = np.random.randint(0, mv.shape[0])
        bit = int(message_bin[i])
        mv[y][x][0] = (mv[y][x][0] & ~1) | bit
        motion_vectors[mv_index] = mv

    # Save the encrypted video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    out = cv2.VideoWriter('encrypted_video6.mp4', cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),
                          (frame1.shape[1], frame1.shape[0]))
    _, frame = cap.read()
    while _:
        # Scramble the pixel indices of the frame
        b, g, r = cv2.split(frame)
        b = np.reshape(b, (num_pixels,))
        g = np.reshape(g, (num_pixels,))
        r = np.reshape(r, (num_pixels,))
        b = b[scrambled_indices]
        g = g[scrambled_indices]
        r = r[scrambled_indices]
        b = np.reshape(b, (height, width))
        g = np.reshape(g, (height, width))
        r = np.reshape(r, (height, width))
        scrambled_frame = cv2.merge((b, g, r))
        scrambled_frame = cv2.merge((b, g, r))

        out.write(scrambled_frame)
        _, frame = cap.read()
    out.release()
    cap.release()

    print("Video encrypted successfully!")

def get_key():
    global key_entry
    key_entry = Entry(window1, width=20, font=("Arial", 20), show='*')
    key_entry.place(x=600, y=200)



# function to decrypt video and show decrypted video
import cv2
import numpy as np

def decrypt_fun():
    global filename
    global key_entry
    path_list = []
    message = ''
    key = int(key_entry.get())

    cap = cv2.VideoCapture(filename)

    # Initialize variables for motion vectors and frames
    _, frame1 = cap.read()
    prev_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    motion_vectors = []

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_pixels = width * height
    scrambled_indices = np.random.permutation(num_pixels)

    # Extract motion vectors between frames
    while (cap.isOpened()):
        ret, frame2 = cap.read()
        if ret == True:
            curr_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev_frame, curr_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            motion_vectors.append(flow)
            prev_frame = curr_frame
        else:
            break

    # Extract the embedded message from the motion vectors
    np.random.seed(key)
    perm = np.random.permutation(len(motion_vectors))
    message_bin = ''
    for i in range(len(message)):
        mv_index = perm[i % len(perm)]
        mv = motion_vectors[mv_index]
        mv = mv.astype(np.int32)  # convert mv to np.int32
        x = np.random.randint(0, mv.shape[1])
        y = np.random.randint(0, mv.shape[0])
        bit = (mv[y][x][0] & 1)
        message_bin += str(bit)



    # Write the decrypted video to file
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    out = cv2.VideoWriter('decrypted_video6.mp4', cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),
                          (frame1.shape[1], frame1.shape[0]))
    _, frame = cap.read()
    while _:
        # Unscramble the pixel indices of the frame
        b, g, r = cv2.split(frame)
        b = np.reshape(b, (num_pixels,))
        g = np.reshape(g, (num_pixels,))
        r = np.reshape(r, (num_pixels,))
        b[scrambled_indices] = b
        g[scrambled_indices] = g
        r[scrambled_indices] = r
        b = np.reshape(b, (height, width))
        g = np.reshape(g, (height, width))
        r = np.reshape(r, (height, width))
        unscrambled_frame = cv2.merge((b, g, r))
        unscrambled_frame = cv2.merge((b, g, r))

        out.write(unscrambled_frame)
        _, frame = cap.read()
    out.release()
    cap.release()

    print("Video decrypted successfully!")




# function to reset the video to original video and show preview of that
def reset_fun():
    global filename

    source3 = cv2.VideoCapture(filename)
    # running the loop
    while True:
        # extracting the frames
        ret3, img3 = source3.read()
        # displaying the video
        cv2.imshow("Original Video", img3)
        # exiting the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break



# top label
start1 = tk.Label(text = "VIDEO  ENCRYPTION WITH MESSAGE \nEMBEDDING AND MOTION VECTOR", font=("Arial", 30, "underline"), fg="black") # same way bg
start1.place(x = 120, y = 10)

# lbl1 = tk.Label(text="Select any video, dimension & crop it...", font=("Arial", 40),fg="green")  # same way bg
# lbl1.place(x=50, y=100)

lbl2 = tk.Label(text="Selected Video", font=("Arial", 30),fg="brown")  # same way bg
lbl2.place(x=80, y=220)

path_text = tk.Text(window1, height=3, width=37, font=("Arial", 30), bg="light yellow", fg="orange",borderwidth=2, relief="solid")
path_text.place(x=80, y = 270)

# Select Button
selectb=Button(window1, text="ENCRYPT VIDEO",command=encrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 120, y = 450)

# Select Button
selectb=Button(window1, text="DECRYPT VIDEO",command=decrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 550, y = 450)

# Select Button
selectb=Button(window1, text="SELECT",command=open_file,  font=("Arial", 25), bg = "light green", fg = "blue")
selectb.place(x = 80, y = 580)

# Get Images Button
getb=Button(window1, text="RESET",command=reset_fun,  font=("Arial", 25), bg = "yellow", fg = "blue")
getb.place(x = 420, y = 580)

key_button = Button(window1, text="Enter Key", command=get_key, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
key_button.place(x=450, y=200)



def exit_win1():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window1.destroy()

# Get Images Button
getb=Button(window1, text="EXIT",command=exit_win1,  font=("Arial", 25), bg = "red", fg = "blue")
getb.place(x = 780, y = 580)

window1.protocol("WM_DELETE_WINDOW", exit_win1)
window1.mainloop()
