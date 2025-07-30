import os
import time
import datetime
import re
import cv2
import keyboard
import psutil
import IPython
import pylab
from pingpong.ai.aiutils import AiUtils

class GetWebcam():
    frame = None
    def __init__(self) -> None:
        self._webcam_cap = None
        if self._is_jupyter_notebook():
            self._is_jupyter_notebook_bool = True
        else:
            self._is_jupyter_notebook_bool = False
    
    # Maybe does not work on other OSes. (Python 3.6.6 with Windows 10, Ubuntu 20.04 checked. MacOS unchecked.)
    # VSCode jupyter notebook extension does not returns True.
    # Renaming exe files of python & jupyter-notebook, and kernel of jupyter-notebook is not supported.
    def _is_jupyter_notebook(self):
        pid = os.getpid()
        p = psutil.Process(pid)
        cmdlines = p.cmdline()
        try:
            if "python" in os.path.split(cmdlines[0])[1] and "kernel" in os.path.split(cmdlines[-1])[1]:
                while True:
                    p = psutil.Process(pid)
                    cmdlines = p.cmdline()
                    if "python" in os.path.split(cmdlines[0])[1] and "jupyter-notebook" in os.path.split(cmdlines[1])[1]:
                        return True
                    pid = p.ppid()
            else:
                return False
        except psutil.NoSuchProcess:
            return False
        except Exception as error:
            raise error

    def webcam_open(self, camera_number=0):
        self._webcam_cap = cv2.VideoCapture(camera_number)
        if self._webcam_cap.isOpened() == False:
            print("Failed to open camera.")
    
    def webcam_close(self):
        try:
            self._webcam_cap.release()
        except:
            pass
    
    def webcam_take_snapshots(self, save_path, delay=0.5):
        global frame
        if self._webcam_cap == None or self._webcam_cap.isOpened() == False:
            raise Exception("Camera is not opened. Cannot execute operation.")
        save_path = AiUtils.validate_folder_path(save_path, True)
        if not self._is_jupyter_notebook_bool:
            print("Save images to", save_path)
            print("Press S to take a snapshot, or press Q to quit.")
            photo_number = 0
            while True:
                ret, frame123 = self._webcam_cap.read()
                if ret == True: 
                    frame = frame123
                    cv2.imshow("Taking_snapshots", frame123)
                    k = cv2.waitKey(1)
                    if keyboard.is_pressed('q'):
                        print("Q hit, closing...")
                        break
                    elif keyboard.is_pressed('s'):
                        img_name = AiUtils.validate_file_path(save_path, 'png', 'snapshot')
                        cv2.imwrite(img_name, frame)
                        print(img_name, "saved.")
                        photo_number += 1
                        time.sleep(delay)
                    print(photo_number, "photos taken.")
                else:
                    break
            self.destroy_webcam_window("Taking_snapshots")
        else:
            photo_number = 0
            is_photo_taken_frame = False
            img_name = ""
            while True:
                ret, frame123 = self._webcam_cap.read()
                if ret == True:
                    frame = frame123
                    converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pylab.axis('off')
                    pylab.title(f"Taking_snapshots\nSave images to \"{save_path}\".\nPress S to take a snapshot, or press Q to quit.")
                    pylab.imshow(converted_frame)
                    pylab.show()
                    if keyboard.is_pressed('q'):
                        print("Q hit, closing...")
                        break
                    elif keyboard.is_pressed('s'):
                        img_name = AiUtils.validate_file_path(save_path, 'png', 'snapshot')
                        cv2.imwrite(img_name, frame)
                        photo_number += 1
                        is_photo_taken_frame = True
                    if not img_name == "":
                        print(img_name, "saved.")
                    if is_photo_taken_frame:
                        is_photo_taken_frame = False
                        time.sleep(delay)
                    print(photo_number, "photos taken.")
                    self.clear_output()
                else:
                    break
    
    def webcam_get_frame(self, window="Get_frame"):
        global frame
        if self._webcam_cap == None or self._webcam_cap.isOpened() == False:
            raise Exception("Camera is not opened. Cannot execute operation.")
        # ret, frame = self._webcam_cap.read()
        ret, frame123 = self._webcam_cap.read()
        if not self._is_jupyter_notebook_bool:
            if ret == True: 
                frame = frame123
                cv2.imshow(window, frame)
                k = cv2.waitKey(1)
        else:
            if ret == True: 
                frame = frame123
                converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pylab.axis('off')
                pylab.title(window)
                pylab.imshow(converted_frame)
                pylab.show()
            else:
                print("Frame is False")
        return frame
    
    def getwebcam(self):
        if self._webcam_cap == None or self._webcam_cap.isOpened() == False:
            raise Exception("Camera is not opened. Cannot execute operation.")
        while True:
            ret, frame123 = self._webcam_cap.read()
            if ret == True:
                frame = frame123
                converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pylab.axis('off')
                pylab.title("Taking_snapshots")
                pylab.imshow(converted_frame)
                pylab.show()
                self.clear_output()
            else:
                self.clear_output()
                print("getwebcam")
        # ret, frame123 = self._webcam_cap.read()
        # if ret == True:
        #     frame = frame123
        #     converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     pylab.axis('off')
        #     pylab.title("getwebcame")
        #     pylab.imshow(converted_frame)
        #     pylab.show()
        #     self.clear_output()
        # else:
        #     print("test")
           
    
    def clear_output(self, wait=True):
        IPython.display.clear_output(wait)

    def destroy_webcam_window(self, window):
        cv2.destroyWindow(window)
    
    def __del__(self):
        self.webcam_close()
        cv2.destroyAllWindows()
