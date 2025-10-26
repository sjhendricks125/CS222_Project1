# CS222_Project1
Savannah Hendricks and Caleb Wilson 

This Python project retrieves and displays data about the last 30 revisions of a specified Wikipedia article. The project provides two different interfaces to access this functionality.

# How to Run
Run python project1.py

# How to run GUI
Run project1Gui.py
This will open a window where you can enter an article title, and then hit the "Get Revisions" for it to work.

# How it works
The code uses the article title to find the URL and redirect the user if the article title was redirected. If the article does not exist, it displays an error message. Otherwise it displays the timestamp and username for each last 30 changes to the page in order. The code uses error handling for input issues and network issues. 
