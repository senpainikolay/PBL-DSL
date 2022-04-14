import tkinter as tk  
from TextExtraction import TextSelectorFromImage
  
# Top level window
frame = tk.Tk()
frame.title("Marusea's Office")
frame.geometry('500x700')
# Function for getting Input
# from textbox and printing it 
# at label widget
  
def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    lbl.config(text = inp) 
    print('auf')  
    img_path = 'kek.jpg'
    a = TextSelectorFromImage()
    a.run('kek.jpg')
  
# TextBox Creation
inputtxt = tk.Text(frame,
                   height = 20,
                   width = 50)
  
inputtxt.pack()
  
# Button Creation
printButton = tk.Button(frame, 
                        
                        text = "Run", 
                        command = printInput )
printButton.pack()
  
# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()
frame.mainloop()