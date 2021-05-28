import tkinter as tk

import os
import cv2
import numpy as np

import time
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)
from keras.models import load_model
#import tensorflow as tf
import CNNModel 


from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")
#print(tf.__version__)
##############################################+=============================================================
image_x, image_y = 64, 64
basepath="E:\Project\pr"

##############################################+=============================================================
root = tk.Tk()
root.configure(background="gray")
root.state('zoomed')
root.title("Sign Recognition System")
##############################################+=============================================================
#####For background Image

lbl = tk.Label(root, text="Sign Language Recognition Using Deep Learning on Custom Processed Gesture Images", font=('times', 25,' bold '),justify=tk.LEFT, wraplength=1300 ,bg="red",fg="black")
lbl.place(x=180, y=5)


frame_CP = tk.LabelFrame(root, text=" Control Panel ", width=200, height=750, bd=5, font=('times', 12, ' bold '),bg="black",fg="white")
frame_CP.grid(row=0, column=0, sticky='s')
frame_CP.place(x=5, y=60)

frame_display = tk.LabelFrame(root, text=" ---WorkSpace--- ", width=1150, height=750, bd=5, font=('times', 12, ' bold '),bg="white",fg="red")
frame_display.grid(row=0, column=0, sticky='s')
frame_display.place(x=210, y=60)

frame_noti = tk.LabelFrame(root, text=" Notification ", width=250, height=750, bd=5, font=('times', 12, ' bold '),bg="black",fg="white")
frame_noti.grid(row=0, column=0, sticky='nw')
frame_noti.place(x=1330, y=60)

ges_name =tk.StringVar()
ges_name="Ges1"
gesEL = tk.Entry(frame_CP, textvariable = ges_name)
gesEL.place(x=25, y=100)
gesEL.insert(0,'G1')

###########################################################################################################
def clear_lbl():
    
    img11 = tk.Label(frame_noti, background='black',width=600,height=850)
    img11.place(x=0, y=0)

def update_label(str_T):
    result_label = tk.Label(frame_noti, text=str_T, font=("italic", 20),justify=tk.LEFT, wraplength=200 ,bg='black',fg='white' )
    result_label.place(x=10, y=0)
#    result_label.after(4000, lambda:result_label.config(text='') )
    
################################################################################################################
def create_folder(folder_name):
    if not os.path.exists(basepath +'/data/training_set/' + folder_name):
        os.mkdir(basepath + '/data/training_set/' + folder_name)
    if not os.path.exists(basepath + '/data/test_set/' + folder_name):
        os.mkdir(basepath + '/data/test_set/' + folder_name)
    
               
def capture_images(ges_name):
    create_folder(str(ges_name))
    
    cam = cv2.VideoCapture(0)

#    cv2.namedWindow("Sign Capture Window")

    img_counter = 0
    t_counter = 1
    training_set_image_name = 1
    test_set_image_name = 1
    listImage = [1,2,3,4,5]


    for loop in listImage:
        while True:

            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)

            l_h = 0
            l_s = 0
            l_v = 0
            u_h = 179 
            u_s = 255
            u_v = 152 
            
            img = cv2.rectangle(frame, (425, 100), (625, 300), (0, 255, 0), thickness=2, lineType=8, shift=0)

            lower_blue = np.array([l_h, l_s, l_v])
            upper_blue = np.array([u_h, u_s, u_v])
            imcrop = img[102:298, 427:623]
            hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

#            result = cv2.bitwise_and(imcrop, imcrop, mask=mask)
            str_T="Please Capture your Sign by pressing << c >> Key" 
            cv2.putText(frame, str(str_T), (10, 30), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,0))
            
            str_T= "Press << esc >> Key to Exit the window"

            cv2.putText(frame, str(str_T), (10, 50), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,0))


            str_T= "Please capture 2000 images for single Gesture "

            cv2.putText(frame, str(str_T), (10, 70), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,255))

            cv2.putText(frame, str(img_counter), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 0, 255))
            cv2.imshow("Sign Capture Window", frame)
            cv2.imshow("Silhouettes Image", mask)
#            cv2.imshow("result", result)

            if cv2.waitKey(1) == ord('c'):

                if t_counter <= 350:
                    img_name = basepath + "/data/training_set/" + str(ges_name) + "/{}.png".format(training_set_image_name)
                    save_img = cv2.resize(mask, (image_x, image_y))
                    cv2.imwrite(img_name, save_img)
                    print("{} written!".format(img_name))
                    training_set_image_name += 1


                if t_counter > 350 and t_counter <= 400:
                    img_name = basepath + "/data/test_set/" + str(ges_name) + "/{}.png".format(test_set_image_name)
                    save_img = cv2.resize(mask, (image_x, image_y))
                    cv2.imwrite(img_name, save_img)
                    print("{} written!".format(img_name))
                    test_set_image_name += 1
                    if test_set_image_name > 250:
                        break


                t_counter += 1
                if t_counter == 401:
                    t_counter = 1
                img_counter += 1


            elif cv2.waitKey(1) == 27:
                cam.release()
                cv2.destroyAllWindows()
                break

        if test_set_image_name > 250:
            break


    cam.release()
    cv2.destroyAllWindows()

###################################################################################################################
def cap_webcam():
    
    update_label("Please Capture your Sign by pressing << c >> Key and Press << esc >> Key to Exit the window")

    if len(gesEL.get()) == 0:
        clear_lbl()
        update_label("Please Enter Gesture Name!!")
        gesEL.focus_set()
    else:
        capture_images(ges_name)

def train_sign():

    clear_lbl()
    
    update_label("Model Training Start...............")
    
    start = time.time()

    X= CNNModel.main()
    
    end = time.time()
        
    ET="Execution Time: {0:.4} seconds \n".format(end-start)
    
    msg="Model Training Completed.."+'\n'+ X + '\n'+ ET

    update_label(msg)

      
#################################################################################################################
#################################################################################################################

def sign_recognize():
    
    clear_lbl()
    
#    update_label("Press << c >> for Gesture Detection with Voice")
    
    
    classifier = load_model(basepath + '/SignR_model.h5')

    def predictor():
        import numpy as np
        from keras.preprocessing import image
        test_image = image.load_img(basepath + '/1.png', target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = classifier.predict(test_image)
   
        if result[0][0] == 1:
            return 'All the best!!'
        elif result[0][1] == 1:
            return 'Very Good!!'
        elif result[0][2] == 1:
            return 'P!!'
        elif result[0][3] == 1:
            return 'A!!'
        elif result[0][4] == 1:
            return 'Z!!'
        
    cam = cv2.VideoCapture(0)
#    update_label("Press << c >> for Gesture Detection with Voice")

    img_text = ''
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame,1)
        update_label("Press << c >> for Gesture Detection with Voice")

        l_h = 0
        l_s = 0
        l_v = 0
        u_h = 179 
        u_s = 255
        u_v = 152 
    
        img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)
    
        lower_blue = np.array([l_h, l_s, l_v])
        upper_blue = np.array([u_h, u_s, u_v])
        imcrop = img[102:298, 427:623]
        hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        cv2.imshow("Sign Capture Window", frame)
        cv2.imshow("Silhouettes Image", mask)
        
        #if cv2.waitKey(1) == ord('c'):
            
        img_name = basepath + "/1.png"
        save_img = cv2.resize(mask, (image_x, image_y))
        cv2.imwrite(img_name, save_img)
    #    print("{} written!".format(img_name))
        img_text = predictor()
#        speak.Speak(img_text)
        
        if cv2.waitKey(1) == ord('c'):
            img_text = predictor()
            speak.Speak(img_text)
            
        if cv2.waitKey(1) == 27:
            cam.release()
            cv2.destroyAllWindows()
            break
            
#################################################################################################################

def window():
    root.destroy()

#################################################################################################################

button1 = tk.Button(frame_CP, text=" Capture Sign Data ", command=cap_webcam,width=19, height=1, font=('times', 12, ' bold '),bg="white",fg="black")
button1.place(x=5, y=50)

button2 = tk.Button(frame_CP, text=" Train Sign Model ", command=train_sign,width=19, height=1, font=('times', 12, ' bold '),bg="white",fg="black")
button2.place(x=5, y=150)
#Analysis data
button3 = tk.Button(frame_CP, text=" Sign Reconition ", command=sign_recognize,width=19, height=1, font=('times', 12, ' bold '),bg="white",fg="black")
button3.place(x=5, y=250)


exit = tk.Button(frame_CP, text="Exit", command=window, width=19, height=1, font=('times', 12, ' bold '),bg="red",fg="white")
exit.place(x=5, y=550)



root.mainloop()