from Tkinter import *

main = Tk()
main.title("Multiple Choice Listbox")
main.geometry("+50+150")
frame = Frame(main)
frame.grid(column=0, row=0, sticky=(N, S, E, W))

valores = StringVar()
valores.set("Carro Coche Moto Bici Triciclo Patineta Patin Patines Lancha Patrullas")

lstbox = Listbox(frame, listvariable=valores, selectmode=MULTIPLE, width=20, height=10)
lstbox.grid(column=0, row=0, columnspan=2)

def select():
    reslist = list()
    seleccion = lstbox.curselection()
    for i in seleccion:
        entrada = lstbox.get(i)
        reslist.append(entrada)
    for val in reslist:
        print(val)

btn = Button(frame, text="Choices", command=select)
btn.grid(column=1, row=1)

main.mainloop()