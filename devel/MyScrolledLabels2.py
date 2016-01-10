# http://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-grid-of-widgets-in-tkinter

from Tkinter import *

class MainApp(Frame):
    def __init__(self, root=None):

        Frame.__init__(self, root)
        #self.frame = Frame(root, bg="lightblue")
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#000000")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
#        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                  tags="self.frame")
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        '''Put in some fake data'''
        options = [ "1","2","3","4","5","6" ]
        for row in range(100):
            OptionMenu(self.frame, *options).grid(row=row, column=0)
            #Label(self.frame, text="%s" % row, width=3, borderwidth="1",
            #         relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            Label(self.frame, text=t).grid(row=row, column=1)
            Label(self.frame, text=t).grid(row=row, column=2)
            Label(self.frame, text=t).grid(row=row, column=3)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=700,height=200)

if __name__ == "__main__":
    root=Tk()
    root.title('Scrolled Labels Test')
    main = MainApp(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
