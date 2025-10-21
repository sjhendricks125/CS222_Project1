# CS222_Project1
Savannah Hendricks and Caleb Wilson 

This Python project retreieves and displays data about the last 30 revisions of a specified Wikipedia article. It begins by prompting the user to enter an article title, which is then cleaned to fit the url format. Using the cleaned title a url is constructed to query the Wikipedia API for revision data. It send the request and handles potential redirects by notifying the user if the article title was redirected. If the article does not exist, it exits with an error message. Otherwise it parses the JSON response and prints the timestamp and username for each of the last 30 revisions in reverse chronological order. The script includes error handling for input issues, missing pages, and network failures. 
