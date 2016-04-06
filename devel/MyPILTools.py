from Tkinter import *
from PIL import Image, ImageTk
from math import fabs
## pip install Pillow # yields PIL package

# TODO : for recursive functions look at
# TODO : http://stackoverflow.com/questions/33923/what-is-tail-recursion

class LabelAnimated(Label):
    def __init__(self, master, filename,duration_factor,mode,method):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = duration_factor * im.info['duration']
        except KeyError:
            self.delay = 100

        print "LabelAnimated uses mode: ", mode, "\nduration: ", duration_factor, "delay: ", self.delay

        if method == 2:
            self.frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in seq]
            Label.__init__(self, master, image=self.frames[0])
        else:
            first = seq[0].convert('RGBA')
            self.frames = [ImageTk.PhotoImage(first)]
            Label.__init__(self, master, image=self.frames[0])
            temp = seq[0]
            for image in seq[1:]:
                temp.paste(image)
                frame = temp.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        # set negative duration factor to play animated gif only once

        if mode == "once":
            print "using play_once."
            self.cancel = self.after(self.delay, self.play_once())
        else:
            self.cancel = self.after(self.delay, self.play())



    def play(self):
        #print "idx = %s" % self.idx
        self.config(image=self.frames[self.idx])
        self.update_idletasks()
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)

    def play_once(self):
        if self.idx < len(self.frames):
            self.config(image=self.frames[self.idx])
            self.update_idletasks()
            self.idx += 1
            self.cancel = self.after(self.delay, self.play_once)


##root = Tk()


#anim = LabelAnimated(root, '../images/animated_gifs/kamikaze-cat6.gif')
#anim.pack()

#def stopAnimation():
#    anim.after_cancel(anim.cancel)

#Button(root, text='stop', command=stopAnimation).pack()

##root.mainloop()