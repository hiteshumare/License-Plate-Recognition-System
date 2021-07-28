import tkinter as Tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
import imutils
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# create a tkinter window
root = Tk() 
num = Label(root,bd=10)
sign_image = Label(root,bd=10)
plate_image=Label(root,bd=10)

# Define Upload Image Function
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((root.winfo_width()/2.25),(root.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        
        show_classify_button(file_path)
        #label.configure(text='')
    except:
        pass

# Define Classify Function  
def classify(file_path):
    res_text=[0]
    res_img=[0]
    img = cv2.imread(file_path,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (300,200) )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edged = cv2.Canny(gray, 30, 200)
    edged = cv2.Canny(gray, 30, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print ("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv2.bitwise_and(img,img,mask=mask)
    res_img[0]=new_image
    cv2.imwrite("C:/Users/Hitesh U/Desktop/Desktop Folder/MINI_PROJECT_TEST/New folder/LicensePlateRecognition/result.png",new_image)
    uploaded=Image.open("C:/Users/Hitesh U/Desktop/Desktop Folder/MINI_PROJECT_TEST/New folder/LicensePlateRecognition/result.png")
    im=ImageTk.PhotoImage(uploaded)
    plate_image.configure(image=im)
    plate_image.image=im
    #cv2.imshow('Gray image', new_image)
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    print("programming_fever's License Plate Recognition\n")
    print("Detected license plate Number is:",text)
    num.configure(text='text')
    img = cv2.resize(img,(500,300))
    Cropped = cv2.resize(Cropped,(400,200))
    #cv2.imshow('car',img)
    #cv2.imshow('Cropped',Cropped)
    #plate_image.image=new_image    
    #plate_image.configure(image=new_image)
    #plate_image.image=new_image
    
# Open window having dimension 800x600
root.geometry('800x600')
root.title("License Plate Recognition")
# Create a Upload Button
upload=Button(root,text="Upload an image",command=upload_image)
upload.configure(background='#364156', foreground='white',font=('arial',15,'bold'))
upload.pack()
upload.place(x=100,y=500)

sign_image.pack()
sign_image.place(x=100,y=200)

plate_image.pack()
plate_image.place(x=450,y=200)

# Create a Classify Button
def show_classify_button(file_path):
    classify_b=Button(root,text="Classify Image",command=lambda: classify(file_path))
    classify_b.configure(background='#364156', foreground='white',font=('arial',15,'bold'))
    classify_b.place(x=450,y=500)
    
root.mainloop()