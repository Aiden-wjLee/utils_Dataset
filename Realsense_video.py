import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
import datetime
import sys
import os
import pyrealsense2 as rs

class PlotCanvas:
    def __init__(self, root, figsize=(10, 10)):
        self.ax = plt.gca()
        self.fig = plt.figure(figsize=figsize)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.frame=None
        self.video_save_TF=False
        self.save_path=None
        self.save_folder=None
        self.count=0
        
    def get_canvas(self):
        return self.canvas

    def get_figure(self):
        return self.fig
    
def Start_video(plotcanvas,pipeline):
    #ret, img = cap.read()
    print("start: 공사중")
    plotcanvas.video_save_TF=True

def Pause_video(plotcanvas):
    plotcanvas.video_save_TF=False
    
def View_video(plotcanvas, pipeline):
    realframes = pipeline.wait_for_frames()
    
    img_color = realframes.get_color_frame()

    img_color = np.asanyarray(img_color.get_data())
    img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RGB
    
    #img_color = cv2.   resize(img_color, (2400, 1800), interpolation=cv2.INTER_CUBIC)
    #img_color = cv2.GaussianBlur(img_color, (5, 5), 0)
    #img_color = cv2.Canny(img_color, 50, 150)
    #img_color = cv2.equalizeHist(img_color)
    
    x=3
    #kernel = np.array([[-x, -x, -x], [-x, 8*x+1, -x], [-x, -x, -x]])
    #kernel = np.array([[0, -x, 0], [-x, 4*x+1, -x], [0, -x, 0]])
    #img_color = cv2.filter2D(img_color, -1, kernel)

    plotcanvas.frame.set_data(img_color)
    plotcanvas.canvas.draw()
    
    if plotcanvas.video_save_TF==True:
        if not os.path.exists(plotcanvas.save_path+plotcanvas.save_folder):
            os.makedirs(plotcanvas.save_path+plotcanvas.save_folder)
        img_color=cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR)
        saved=cv2.imwrite(f'{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg', img_color)
        if saved==False:
            print("save error")
        else:
            print(f"{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg")
        print(f"{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg")
        plotcanvas.count+=1
    
    root.after(40, View_video, plotcanvas, pipeline)

def Save_video(plotcanvas):
    plotcanvas.save_path = 'D:/Dataset/prior/'
    plotcanvas.save_folder = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'/'
    plotcanvas.count=0
    plotcanvas.video_save_TF=False

def main(plotcanvas,pipeline):
    # 버튼 생성 및 클릭 이벤트 바인딩
    button_frame1 = tk.Frame(root, bg='lightblue', highlightbackground='darkblue', highlightthickness=1, relief='groove')
    button_frame1.pack(side='top', pady=5)
    Make_box_button = ttk.Button(button_frame1, text="Start Video", command=lambda: Start_video(plotcanvas, pipeline))
    Make_box_button.pack(side='left',pady=5, padx=10)
    Pause_video_button = ttk.Button(button_frame1, text="Pause Video", command=lambda: Pause_video(plotcanvas))
    Pause_video_button.pack(side='left',pady=5, padx=10)
    
    Save_video_button = ttk.Button(button_frame1, text="Save Video", command=lambda: Save_video(plotcanvas))
    Save_video_button.pack(side='left',pady=5, padx=10)
    
    

    View_video(plotcanvas, pipeline)
    # 그림을 캔버스에 삽입하고 Tkinter 창에 표시
    plotcanvas.canvas.draw()
    plotcanvas.canvas.get_tk_widget().pack()
    
    root.mainloop()

if __name__=="__main__":
    # Tkinter 창 설정
    root = tk.Tk()
    root.configure(background='black')
    plotcanvas=PlotCanvas(root,figsize=(10, 10))
    
    #ax,fig 설정
    ax=plotcanvas.ax
    fig=plotcanvas.fig
    canvas=plotcanvas.canvas
    
    #web cam load 
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    # Start streaming
    profile=pipeline.start(config)
    #sensor_color = profile.get_device().first_color_sensor()
    #sensor_color.set_option(rs.option.enable_auto_white_balance, 0)
    
    realframes = pipeline.wait_for_frames()
    
    img_color = realframes.get_color_frame()
    img_color = np.asanyarray(img_color.get_data())
    
    #set plotcanvas.frame , ax
    #img_color = cv2.resize(img_color, (2400, 1800), interpolation=cv2.INTER_CUBIC)
    frame = plt.imshow(img_color) #, cmap='gray'
    plotcanvas.frame=frame
    plotcanvas.ax.set_title("asdf")
    
    now=datetime.datetime.now()
    #save_path='D:/OneDrive - Sogang/문서/카카오톡 받은 파일/Realsense_video/'
    save_path='D:/Dataset/prior/'
    save_folder=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'/'#f'{now.hour}_{now.minute}_{now.second}/'
    
    plotcanvas.save_path=save_path
    plotcanvas.save_folder=save_folder
    
    main(plotcanvas, pipeline)
    
    pipeline.stop()
    cv2.destroyAllWindows()