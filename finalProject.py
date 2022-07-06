from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog
import datetime


class MainGUI:
    def __init__(self, root) -> None:
        # BUTTON ON/OFF STATES
        self.isDetectEyes = False
        self.isDetectFace = False
        self.isDetectSmile = False
        self.isDetectCat = False
        self.isUsingWebCam = False
        self.isPlayingVideo = False
        self.isImageSelected = False

        # DEFAULT IMAGE WHEN NO IMAGE/VIDEO SOURCE IS USED
        self.defaultFrameImage = PhotoImage(file=r"./icons/need_image.png")

        # RESIZING ICONS TO A SMALLER SIZE
        iconWidth = 1  # Icons will resize 1/n of the original Icon Image
        iconHeight = 1
        eyeIcon = PhotoImage(
            file=r"./icons/eye.png").subsample(iconWidth, iconHeight)
        faceIcon = PhotoImage(
            file=r"./icons/face-detection.png").subsample(iconWidth, iconHeight)
        smileIcon = PhotoImage(
            file=r"./icons/smile.png").subsample(iconWidth, iconHeight)
        catIcon = PhotoImage(
            file=r"./icons/cat.png").subsample(iconWidth, iconHeight)
        webCamIcon = PhotoImage(
            file=r"./icons/webcam.png").subsample(iconWidth, iconHeight)
        videoIcon = PhotoImage(
            file=r"./icons/video.png").subsample(iconWidth, iconHeight)
        imageIcon = PhotoImage(
            file=r"./icons/image.png").subsample(iconWidth, iconHeight)
        stopIcon = PhotoImage(
            file=r"./icons/stop-button.png").subsample(iconWidth, iconHeight)
        captureIcon = PhotoImage(
            file=r"./icons/photo-capture.png").subsample(iconWidth, iconHeight)

        # MAIN WINDOW
        self.root = root
        self.root.title("Final Project")
        self.root.configure(bg="#4DBF85")
        self.root.option_add("*font", "Arial 12")
        self.root.resizable(False, False)

        # IMAGE/VIDEO CANVAS
        imageFrame = Frame(self.root)
        imageFrame.grid(row=0, column=0, padx=10, pady=10)
        self.labelImage = Label(imageFrame)
        self.labelImage.grid(row=0, column=0, padx=5, pady=5)

        # INDIVIDUAL FRAMES FOR GROUPED BUTTONS FOR BETTER LAYOUT
        buttonsFrame = Frame(self.root, width=650, height=400)
        buttonsFrame.grid(row=0, column=1, padx=10, pady=5)

        sourcesButtonsFrame = Frame(buttonsFrame)
        detectButtonsFrame = Frame(buttonsFrame)
        snapshotButtonsFrame = Frame(buttonsFrame)

        sourcesButtonsFrame.grid(row=1, column=0)
        detectButtonsFrame.grid(row=3, column=0)
        snapshotButtonsFrame.grid(row=5, column=0)

        # BUTTONS
        # SOURCE BUTTONS
        self.buttonUseWebCam = Button(
            sourcesButtonsFrame, width=80, text="Webcam", image=webCamIcon,
            compound=TOP, command=self.start_webcam)
        self.buttonUploadVideo = Button(
            sourcesButtonsFrame, width=80, text="Video", image=videoIcon,
            compound=TOP, command=self.upload_video)
        self.buttonUploadImage = Button(
            sourcesButtonsFrame, width=80, text="Image", image=imageIcon,
            compound=TOP, command=self.upload_image)

        # DETECTION BUTTONS
        self.buttonEyes = Button(
            detectButtonsFrame, text="Eyes", image=eyeIcon, width=120,
            compound=LEFT, command=lambda: self.detect_button_click(self.isDetectEyes, 'isDetectEyes', self.buttonEyes))
        self.buttonFace = Button(
            detectButtonsFrame, text="Face", image=faceIcon, width=120,
            compound=LEFT, command=lambda: self.detect_button_click(self.isDetectFace, 'isDetectFace', self.buttonFace))
        self.buttonSmile = Button(
            detectButtonsFrame, text="Smile", image=smileIcon, width=120,
            compound=LEFT, command=lambda: self.detect_button_click(self.isDetectSmile, 'isDetectSmile', self.buttonSmile))
        self.buttonCat = Button(
            detectButtonsFrame, text="Cats", image=catIcon, width=120,
            compound=LEFT, command=lambda: self.detect_button_click(self.isDetectCat, 'isDetectCat', self.buttonCat))

        # MISC BUTTONS
        self.buttonSnapShot = Button(
            snapshotButtonsFrame, text="SnapShot", image=captureIcon, width=140, state=DISABLED,
            compound=LEFT, command=lambda: SaveSnapShotWindow(self.root, self.filteredFrame))
        self.buttonStop = Button(
            snapshotButtonsFrame, text="Stop", image=stopIcon, width=140,
            compound=LEFT, command=self.stop_playing)

        # BUTTON LAYOUT
        Label(buttonsFrame, text="Pick a Source").grid(
            row=0, column=0, pady=10)
        self.buttonUseWebCam.grid(row=1, column=0, padx=5, pady=5)
        self.buttonUploadVideo.grid(row=1, column=1, padx=5, pady=5)
        self.buttonUploadImage.grid(row=1, column=2, padx=5, pady=5)

        Label(buttonsFrame, text="Pick a Detection").grid(
            row=2, column=0, pady=10)
        self.buttonEyes.grid(row=0, column=0, padx=5, pady=5)
        self.buttonFace.grid(row=1, column=0, padx=5, pady=5)
        self.buttonSmile.grid(row=0, column=1, padx=5, pady=5)
        self.buttonCat.grid(row=1, column=1, padx=5, pady=5)

        Label(buttonsFrame, text="Misc").grid(
            row=4, column=0, pady=10)
        self.buttonSnapShot.grid(row=0, column=0, padx=5, pady=5)
        self.buttonStop.grid(row=0, column=1, padx=5, pady=5)

        # DISPLAY DEFAULT IMAGE UPON LAUNCH OR WHEN STOP BUTTON IS PRESSED
        self.labelImage.configure(image=self.defaultFrameImage)

        # CUSTOMIZE THE "X" BUTTON OF A WINDOW TO CLOSE IT WITHOUT ERROR
        # When the user pressed the X button on a window, this function will suspend all running functions before closing/destroying the window
        self.root.protocol("WM_DELETE_WINDOW", lambda: (
            self.stop_playing(), self.root.destroy()))

        self.root.mainloop()

    def start_webcam(self):
        # Stop Everything if there is any
        self.stop_playing()

        # State that the program is using the Web Cam as source
        self.isUsingWebCam = True
        self.isPlayingVideo = False
        self.isImageSelected = False
        self.buttonUseWebCam.configure(state=DISABLED)
        self.buttonSnapShot.configure(state=NORMAL)

        # Opens the Web cam
        self.webCamCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.cycle_frames()

    def upload_image(self):
        # Stop Everything if there is any
        self.stop_playing()

        # Spawns a window to choose a file, if a file was not selected the function will stop
        filePath = filedialog.askopenfilename(title="Select image file", filetypes=(
            ("jpg files", "*.jpg"), ("all files", "*.*")))
        if filePath == "":
            return
        # Convert / path to \\ for Windows to be able to read
        self.convertedFilePath = filePath.replace('/', "\\\\")

        # State that the program is using an Image as source
        self.isImageSelected = True
        self.isUsingWebCam = False
        self.isPlayingVideo = False
        self.buttonSnapShot.configure(state=NORMAL)

        self.cycle_frames()

    def upload_video(self):
        # Stop Everything if there is any
        self.stop_playing()

        # Spawns a window to choose a file, if a file was not selected the function will stop
        filePath = filedialog.askopenfilename(title="Select video file", filetypes=(
            ("mp4 files", "*.mp4"), ("all files", "*.*")))
        if filePath == "":
            return

        # Convert / path to \\ for Windows to be able to read
        convertedFilePath = filePath.replace('/', "\\\\")

        self.video = cv2.VideoCapture(convertedFilePath)

        # State that the program is using a Video as source
        self.isUsingWebCam = False
        self.isPlayingVideo = True
        self.isImageSelected = False
        self.buttonSnapShot.configure(state=NORMAL)

        self.cycle_frames()

    def detect_button_click(self, buttonState, instanceName, button):
        if buttonState:
            # Sets the button to be Unpressed
            setattr(self, instanceName, False)
            button.config(relief=RAISED)

        else:
            # Sets the button to be Pressed
            setattr(self, instanceName, True)
            button.config(relief=SUNKEN)

        # Conditional statement for when an Image is the source, every click of the button updates the image
        if ((not self.isUsingWebCam) & (not self.isPlayingVideo)):
            if self.isImageSelected:
                self.cycle_frames()

    def cycle_frames(self):
        if self.isPlayingVideo | self.isUsingWebCam:
            while True:
                ret = 0
                if self.isUsingWebCam:
                    ret, frame = self.webCamCapture.read()
                    # Flips the webcam output to act like a mirror
                    frame = cv2.flip(frame, 1)

                if self.isPlayingVideo:
                    ret, frame = self.video.read()

                if not ret:  # Stops the while loop when the video/webcam has no more frames or have been stopped
                    break
                #
                self.show_image_on_label(frame)

        if self.isImageSelected:
            self.image = cv2.imread(self.convertedFilePath)
            self.show_image_on_label(self.image)

    def show_image_on_label(self, frame):
        # Apply the boxes and convert the image from BGR to RGB
        # This is the variable that will be used when clicking the snapshot button
        self.filteredFrame = self.detection_applier(frame)
        cv2image = cv2.cvtColor(self.filteredFrame, cv2.COLOR_BGR2RGB)

        # Converts CV2 image to PIL image that tkinter can read
        img_update = ImageTk.PhotoImage(Image.fromarray(cv2image))

        # Configure the label to show the PIL image in it
        self.labelImage.configure(image=img_update)
        self.labelImage.image = img_update
        self.labelImage.update()

    def detection_applier(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Configs of when drawing a text on the frames/images
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.7
        fontBold = 2

        faceCascade = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")
        eyeCascade = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_eye.xml")
        smileCascade = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_smile.xml")
        catFaceCascade = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_frontalcatface.xml")

        if (self.isDetectFace):
            # WHEN A FACE IS DETECTED, ONLY THE EYES AND SMILE IN THE FACE ROI WILL BE BOXED
            detectedFaces = faceCascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in detectedFaces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face', (x, y), font,
                            fontScale, (0, 255, 0), fontBold)

                # Region of Interest of the Face
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                if self.isDetectEyes:
                    eyes = eyeCascade.detectMultiScale(roi_gray, 1.3, 25)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey),
                                      (ex+ew, ey+eh), (0, 0, 255), 2)
                        cv2.putText(roi_color, 'Eyes', (ex, ey),
                                    font, fontScale, (0, 0, 255), fontBold)

                if self.isDetectSmile:
                    smiles = smileCascade.detectMultiScale(
                        roi_gray, 1.8, 25)
                    for (sx, sy, sw, sh) in smiles:
                        cv2.rectangle(roi_color, (sx, sy),
                                      ((sx + sw), (sy + sh)), (255, 0, 0), 2)
                        cv2.putText(roi_color, 'Smile', (sx, sy),
                                    font, fontScale, (255, 0, 0), fontBold)

        if (self.isDetectEyes & (not self.isDetectFace)):

            detectedEyes = eyeCascade.detectMultiScale(gray, 1.3, 25)
            for (x, y, w, h) in detectedEyes:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, 'Eyes', (x, y),
                            font, fontScale, (0, 0, 255), fontBold)

        if (self.isDetectSmile & (not self.isDetectFace)):

            detectedSmiles = smileCascade.detectMultiScale(gray, 1.8, 20)
            for (x, y, w, h) in detectedSmiles:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (225, 0, 0), 2)
                cv2.putText(frame, 'Smile', (x, y),
                            font, fontScale, (255, 0, 0), fontBold)

        if self.isDetectCat:

            detectedCats = catFaceCascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in detectedCats:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 102, 255), 2)
                cv2.putText(frame, 'Cat', (x, y),
                            font, fontScale, (0, 102, 255), fontBold)

        return frame

    def stop_playing(self):
        # Releases either the webcam of the video source
        if self.isUsingWebCam:
            self.webCamCapture.release()
        if self.isPlayingVideo:
            self.video.release()

        # Set the default image on the image canvas
        self.labelImage.configure(image=self.defaultFrameImage)

        # Change button states accordingly
        self.isUsingWebCam = False
        self.isPlayingVideo = False
        self.isImageSelected = False
        self.buttonSnapShot.configure(state=DISABLED)
        self.buttonUseWebCam.configure(state=NORMAL)


class SaveSnapShotWindow:
    def __init__(self, root, filteredFrame) -> None:
        self.saveWindow = Toplevel(root)
        self.saveWindow.title("Save SnapShot")
        self.saveWindow.resizable(False, False)
        self.saveWindow.option_add("*font", "Arial 12")

        # IMAGE/VIDEO CANVAS
        self.imageFrame = Frame(self.saveWindow)
        self.labelImage = Label(self.imageFrame)
        self.imageFrame.pack()
        self.labelImage.grid(row=0, column=0, padx=10, pady=10)

        # SEPARATE FRAMES FOR THE BUTTONS AND TEXT FIELD
        changeFileNameFrame = Frame(self.saveWindow)
        changeFileNameFrame.pack()
        buttonFrame = Frame(self.saveWindow)
        buttonFrame.pack()

        # TEXTFIELD FOR THE FILE NAME
        self.entryboxSaveAs = Entry(changeFileNameFrame, width=25)
        labelFileExtension = Label(changeFileNameFrame, text=".jpg")

        # SAVE AND CANCEL BUTTONS
        self.buttonSave = Button(
            buttonFrame, text="Save", command=self.save, bg='#4764ff', fg='white', width=15, height=1)
        self.buttonCancel = Button(
            buttonFrame, text="Cancel", command=self.close_window_or_cancel, bg='#3c3c3c', fg='white', width=15, height=1)

        # TEXTFIELD AND BUTTONS LAYOUT
        Label(changeFileNameFrame, text="Set Filename:").grid(row=0, column=0)
        self.entryboxSaveAs.grid(row=1, column=0)
        labelFileExtension.grid(row=1, column=1, sticky=W)
        self.buttonSave.grid(row=0, column=1, padx=20, pady=10)
        self.buttonCancel.grid(row=0, column=0, padx=20, pady=10)
        #
        #
        # SHOW THE IMAGE ON THE IMAGE CANVAS
        self.snapShotImage = filteredFrame
        self.show_image_on_label(self.snapShotImage)

        # GETS THE CURRENT TIME AND PLACE IT IN THE TEXTFIELD AS A DEFAULT FILE NAME
        self.timeString = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.entryboxSaveAs.insert(INSERT, self.timeString)

        # GRABS THE FOCUS ON THIS WINDOW SO THAT THE MAIN WINDOW CANNOT BE PRESSED UNTIL THIS WINDOW IS CLOSED
        self.saveWindow.grab_set()

        # MODIFIED THE X BUTTON FOR A SAFE CLOSE
        self.saveWindow.protocol(
            "WM_DELETE_WINDOW", self.close_window_or_cancel)

    def save(self):
        # Gets the file name from the textbox
        saveAsFileName = self.entryboxSaveAs.get()

        # If the user did not type any name, it will default to the current time
        if saveAsFileName == "":
            saveAsFileName = self.timeString

        # Writes/Saves the image that was passed through the class not the downscale thumbnail/image
        cv2.imwrite(f'./snapshots/{saveAsFileName}.jpg', self.snapShotImage)

        self.close_window_or_cancel()

    def close_window_or_cancel(self):
        self.saveWindow.grab_release()
        # Safely destroy the toplevel without affecting the root window
        self.saveWindow.destroy()

    def show_image_on_label(self, frame):
        # Apply the boxes and convert the image from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2image = self.downscale_image(cv2image)

        # Converts CV2 image to PIL image that tkinter can read
        img_update = ImageTk.PhotoImage(Image.fromarray(cv2image))

        # Configure the label to show the PIL image in it
        self.labelImage.configure(image=img_update)
        self.labelImage.image = img_update
        self.labelImage.update()

    def downscale_image(self, image):
        scale_percent = 70  # Resize the image to n%
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # Return the resized image
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


root = tk.Tk()
MainGUI(root)
