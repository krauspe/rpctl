#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename,askopenfile
import tkFont
import os,time
from collections import defaultdict
import pprint
from MyPILTools import LabelAnimated


# Titles
main_window_title = """ 2Step Remote Pilot Control License Check """

pydir =  os.path.dirname(os.path.abspath(__file__))
basedir = os.path.dirname(pydir)
imagedir = os.path.join(basedir, "images")
animdir = os.path.join(imagedir, "animated_gifs")
logo_filename = 'dfs.gif'
default_animated_gif_filename = 'airplane13.gif'
duration = 1
logo_file = os.path.join(imagedir, logo_filename)
default_animated_gif_file = os.path.join(imagedir, default_animated_gif_filename)


def Quit():
        print "Quit"
        root.quit()


class MainApp(Frame):

    #def __init__(self, root, *args, **kwargs):
    def __init__(self, root=None ):
        """http://stackoverflow.com/questions/6129899/python-multiple-frames-with-grid-manager"""
        self.r1 = 0

        Frame.__init__(self, root)


        self.frame = Frame(root)
        self.frame.grid(row=0,column=1)

        self.logo = PhotoImage(file=logo_file)
        Label(self.frame, image=self.logo).grid(row=0,column=0,sticky="E")


        self.anim = self.showAnimatedGif(default_animated_gif_file, 1, "forever", 2, 0, 2)

        self.lFont = tkFont.Font(family="Arial Black", size="12")
        Label(self.frame,  text="Evaluation period expired !",font=self.lFont, width=30,fg="black", bg="red").grid(row=0, column=1, sticky=W+E)
        #Button(self.frame, text="Update Remote Pilot Status", command=self.updateStatus).grid(row=3, column=1, sticky=W+E)
        Button(self.frame, text="Buy license", fg="black", command=self.showGif1).grid(row=2, column=0,sticky=W + E)
        Button(self.frame, text="Ignore", fg="black", command=self.showGif1).grid(row=2, column=1,sticky=W + E)
        Button(self.frame, text="Enter License Key", fg="black", command=self.inputRegistrationKey).grid(row=2, column=2, sticky=W + E)
        Button(self.frame, text="QUIT", fg="black", command=self.frame.quit).grid(row=2, column=3, sticky=W + E)


# self.bt_Start_Reconfiguration = Button(self.con_and_button_frame, text="Start Reconfiguration", command=self.startReconfiguration, state=DISABLED, activebackground="red")
        # self.bt_Start_Reconfiguration.grid(row=11, column=1, sticky=W+E)
        #
        # Label(self.con_and_button_frame,  text="").grid(row=12, column=1, sticky=W+E)
        # Button(self.con_and_button_frame,text="QUIT", fg="red",command=self.frame.quit).grid(row=13,column=1, sticky=W+E)

    def showGif1(self):
        self.stopAnimation()
        animated_gif_subdir = "others"
        animated_gif_filename = "Gravity-balls-ear-to-ear-crazy-animation.gif"
        animated_gif_file = os.path.join(animdir,animated_gif_subdir, animated_gif_filename)
        self.anim = self.showAnimatedGif(animated_gif_file, 1, "forever", 2, 0, 2)


    def showAnimatedGif(self,file,duration,mode,method,row,column):
        #if self.anim:
        #    self.stopAnimation()
        self.anim = LabelAnimated(self.frame, file, duration, mode, method)
        self.anim.grid(row=row,column=column)
        return self.anim


    def stopAnimation(self):
        self.anim.after_cancel(self.anim.cancel)
        self.anim.destroy()

    def inputRegistrationKey(self):
        '''inputRegistrationKey'''
        self.font_label_regkey = tkFont.Font(family="Arial Black", size="10")
        self.reg_window = Toplevel(self)
        self.reg_window.wm_title("Register")
        l = Label(self.reg_window, text="Type in your registration key").pack()


        self.entrytext = StringVar()
        Entry(self.reg_window, textvariable=self.entrytext).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Check")
        Button(self.reg_window, textvariable=self.buttontext, command=self.clicked1).pack()

        self.label_regkey = Label(self.reg_window, text="", font=self.font_label_regkey)
        self.label_regkey.pack()


    def clicked1(self):
        self.input = self.entrytext.get()
        self.label_regkey_text = ""
        if self.input == "1.4.2016":
            self.label_regkey_text = "registration complete"
        else:
            self.label_regkey_text = "license key not valid !!"

        self.label_regkey.configure(text=self.label_regkey_text)
        time.sleep(3)
        self.reg_window.quit()




if __name__ == "__main__":
    root = Tk()
    #root.geometry("800x600")  # mal testen !!
    root.title(main_window_title)
    main = MainApp(root)
    #main.grid(row=0,column=0)
    main.grid()
    root.mainloop()
    root.destroy()

