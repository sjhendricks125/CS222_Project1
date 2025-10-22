import tkinter as tk

def query_article():
    title = title_entry.get()
    revisions_text.delete(1.0, tk.END)  # Clear previous results


#Gui setup
window = tk.Tk()
window.title("Wikipedia Article Revisions")
window.geometry("600x400")

#Input field for article title
title_label = tk.Label(window, text="Enter Wikipedia Article Title:")
title_label.pack()

title_entry = tk.Entry(window, width=50)
title_entry.pack()

#Text area for displaying revisions
revisions_text = tk.Text(window, wrap=tk.WORD)
revisions_text.pack(expand=True, fill=tk.BOTH)

#Start the GUI event loop
window.mainloop()