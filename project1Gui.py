import tkinter as tk

def query_article():
    title = title_entry.get()
    revisions_text.delete(1.0, tk.END)  # Clear previous results

    if not title:
        revisions_text.insert(tk.END, "Please enter the article title")
        return
    
    revisions_text.insert(tk.END, "Gathering the revisions now-\n")
    window.update()
    success, message, revisions = get_wikipedia_revisions(title)
    revisions_text.delete(1.0, tk.END)
    
    if not success:
        revisions_text.insert(tk.END, f"Error: {message}")
        return

    for revision in revisions:
        revisions_text.insert(tk.END, f"{revision['timestamp']} {revision['user']}\n")

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
