from Tkinter import *

class App:

    def __init__(self,master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.title = Label(master, text="Hello World!")
        self.title.pack()

    def say_hi(self):
        print "hi there, everyone!"

# make window, app
window = Tk()
poll = App(window)

# end
window.mainloop()
window.destroy()
