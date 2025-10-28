import json
import ssl
import re
import sys
from urllib.request import urlopen, Request
import tkinter as tk

def getWikiData(title):
    title = re.sub(r'[^a-zA-Z0-9,]+', '_', title)
    title = title.strip('_')
    
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={title}&rvprop=timestamp|user&rvlimit=30&redirects'
    
    try:
        request = Request(url, headers={'User-Agent': 'CS222Project/1.0'})
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
        data = json.loads(response.read())
        
        redirect = ""
        if 'redirects' in data.get('query', {}):
            redirect = f"Redirected to {data['query']['redirects'][0]['to']}"
        
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        page = pages[page_id]
        
        if 'missing' in page:
            return None, "No page found", []
        
        return redirect, "success", page['revisions']
    
    except Exception as e:
        return None, "Network error", []

def commandLine():
    title = input("Enter Wikipedia Article Title:\n")
    
    redirect, status, revisions = getWikiData(title)
    
    if status == "No page found":
        print("No Wikipedia page found for the provided name")
        sys.exit(2)
    elif status == "Network error":
        print("Network error occurred")
        sys.exit(3)
    
    if redirect:
        print(redirect)
    
    for revision in revisions:
        print(f"{revision['timestamp']} {revision['user']}")

def searchWiki():
    title = entry.get()
    text_area.delete(1.0, tk.END)
    
    if not title:
        text_area.insert(tk.END, "Please enter a title")
        return
    
    text_area.insert(tk.END, "Loading...\n")
    root.update()
    
    redirect, status, revisions = getWikiData(title)
    text_area.delete(1.0, tk.END)
    
    if status == "No page found":
        text_area.insert(tk.END, f"No page found for '{title}'")
        return
    elif status == "Network error":
        text_area.insert(tk.END, "Network error occurred")
        return
    
    if redirect:
        text_area.insert(tk.END, f"{redirect}\n\n")
    
    for revision in revisions:
        text_area.insert(tk.END, f"{revision['timestamp']} {revision['user']}\n")

def createGUI():
    global root, entry, text_area
    
    root = tk.Tk()
    root.title("Wikipedia Revisions")
    root.geometry("600x400")
    tk.Label(root, text="Enter Wikipedia Article Title:").pack(pady=5)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    entry.bind('<Return>', lambda e: searchWiki())
    tk.Button(root, text="Search", command=searchWiki).pack(pady=10)
    
    text_area = tk.Text(root, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    root.mainloop()
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        createGUI()
    else:
        commandLine()

