import tkinter as tk
import json
import ssl
import re
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
            redirect_message = f"Redirected to '{redirect_name}'\n\n"
        
        pages = wikiData['query']['pages']
        page_id = list(pages.keys())[0]
        page = pages[page_id]
        
        if 'missing' in page:
            return False, "No Wikipedia page found for the provided name", []
        
        revisions = page['revisions']
        for revision in revisions:
            timestamp = revision['timestamp']
            user = revision['user']
            print(f"{timestamp} {user}")
        return True, redirect_message, revisions
        
    except Exception as e:
        return False, "Network error occurred", []

def query_article():
    title = title_entry.get()
    revisions_text.delete(1.0, tk.END) 

    if not title:
        revisions_text.insert(tk.END, "Please enter the article title")
        return
    
    revisions_text.insert(tk.END, "Gathering the revisions now-\n")
    window.update()
    
    from project1 import sendRequest

    clean_title = re.sub(r'[^a-zA-Z0-9,]+', '_', title).strip('_')
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={clean_title}&rvprop=timestamp|user&rvlimit=30&redirects'

    try:
        sendRequest(url)
    except SystemExit:
        pass # Prevent closing the GUI
    success, message, revisions = get_wikipedia_revisions(title)

    revisions_text.delete(1.0, tk.END)
    
    if not success:
        revisions_text.insert(tk.END, f"Error: {message}")
        return
    if message:
        revisions_text.insert(tk.END, message)
    
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

#Query button
query_button = tk.Button(window, text="Get Revisions", command=query_article)
query_button.pack(pady=10)

#Text area for displaying revisions
revisions_text = tk.Text(window, wrap=tk.WORD)
revisions_text.pack(expand=True, fill=tk.BOTH)

#Start the GUI event loop
window.mainloop()
