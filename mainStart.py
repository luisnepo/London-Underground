import tkinter as tk 
from Window_starter import startFrame, nextFrame 

#initializes the Windows
class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Travel Checker")
        self.geometry("500x500")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        all_frames = (startFrame, nextFrame)

        for F in all_frames:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("startFrame")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        
#initializes the program       
if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()