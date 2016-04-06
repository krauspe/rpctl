# http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-grid-of-widgets-in-tkinter

from Tkinter import *

class Example(Frame):
    def __init__(self, root):

        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        #self.frame.bind("<Configure>", self.onFrameConfigure)

        # options = [ "1","2","3","4","5","6" ]
        # for row in range(100):
        #     OptionMenu(self.frame, *options).grid(row=row, column=0)
        #     #Label(self.frame, text="%s" % row, width=3, borderwidth="1",
        #     #         relief="solid").grid(row=row, column=0)
        #     reg_window="this is the second column for row %s" %row
        #     Label(self.frame, text=reg_window).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
