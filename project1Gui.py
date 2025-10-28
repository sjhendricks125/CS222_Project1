import tkinter as tk
import json
import ssl
import re
import sys
from urllib.request import urlopen, Request

def get_wikipedia_revisions(title):
    try:
        clean_title = re.sub(r'[^a-zA-Z0-9,]+', '_', title)
        clean_title = clean_title.strip('_')
        
        url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={clean_title}&rvprop=timestamp|user&rvlimit=30&redirects'
        
        request = Request(url, headers={'User-Agent': 'CS222Project/1.0'})
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
        wikiData = json.loads(response.read())
        
        redirect_message = ""
        if 'redirects' in wikiData.get('query', {}):
            redirect_name = wikiData['query']['redirects'][0]['to']
            redirect_message = f"Redirected to '{redirect_name}'"
        
        pages = wikiData['query']['pages']
        page_id = list(pages.keys())[0]
        page = pages[page_id]
        
        if 'missing' in page:
            return False, "No page was found for the provided name", []
        
        revisions = page['revisions']
        return True, redirect_message, revisions
        
    except Exception as e:
        return False, "Network error occurred", []

def query_article():
    title = title_entry.get()
    revisions_text.delete(1.0, tk.END) 

    if not title:
        revisions_text.insert(tk.END, "Please enter the article title")
        return
    
    print(f"Starting query for article: {title}")
    revisions_text.insert(tk.END, "Gathering the revisions now-\n")
    window.update()
    success, message, revisions = get_wikipedia_revisions(title)
    revisions_text.delete(1.0, tk.END)
    
    if not success:
        if "No page" in message:
            revisions_text.insert(tk.END, f"No Wikipedia article found for '{title}'. Please check the spelling and try again.")
        elif "Network error" in message:
            revisions_text.insert(tk.END, "Network error occurred. Please check your internet connection and try again.")
        else:
            revisions_text.insert(tk.END, f"Error: {message}")
        return
    if message: 
        revisions_text.insert(tk.END, message)
    
    print("Displaying revisions:")
    for revision in revisions:
        timestamp = revision['timestamp']
        user = revision['user']
        print(f"{timestamp} {user}")
        revisions_text.insert(tk.END, f"{timestamp} {user}\n")

# Command line 
def run_command_line():
    title = input("Enter Wikipedia Article Title:\n")
    success, message, revisions = get_wikipedia_revisions(title)
    
    if not success:
        print(message)
        if "No page" in message:
            sys.exit(2)
        else:
            sys.exit(3)
    
    if message:  
        print(message)
    for revision in revisions:
        timestamp = revision['timestamp']
        user = revision['user']
        print(f"{timestamp} {user}")

# GUI version
def run_gui():
    global window, title_entry, revisions_text
    
    window = tk.Tk()
    window.title("Wikipedia Article Revisions")
    window.geometry("600x400")


    title_label = tk.Label(window, text="Enter Wikipedia Article Title:")
    title_label.pack()

    title_entry = tk.Entry(window, width=50)
    title_entry.pack()
    title_entry.bind('<Return>', lambda event: query_article())  

    query_button = tk.Button(window, text="Get Revisions", command=query_article)
    query_button.pack(pady=10)

    revisions_text = tk.Text(window, wrap=tk.WORD)
    revisions_text.pack(expand=True, fill=tk.BOTH)

    window.mainloop()
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cmd":
        run_command_line()
    else:
        run_gui()
