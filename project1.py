import json
import ssl
import re
import sys
from urllib.request import urlopen, Request

# getWikiTitle
#Prompts user for title
#Cleans title for url 
#Strips leading/trailing underscores
#Returns clean title string 
def getWikiTitle():
    try:
        title = input("Enter Wikipedia Article Title:\n")
        title = re.sub(r'[^a-zA-Z0-9,]+', '_', title) #replace characters with '_'
        title = title.strip('_') #remove leading/trailing underscores
    except IndexError:
        print("Title input error")
        sys.exit(1)
    return title

# sendRequest 
#Sends request to Wikipedia API
#handles redirects and missing pages
#prints the timestamp and user of last 30 revisions
#Exits with specific codes for different errors
def sendRequest(url):
    try: 
        request = Request(url, headers={'User-Agent': 'CS222Project/1.0'})
        #sends request and parse JSON response
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
        wikiData = json.loads(response.read())

        #Handle redirects

        if 'redirects' in wikiData.get('query', {}):
            redirect_name = wikiData['query']['redirects'][0]['to']
            print(f"Redirected to {redirect_name}")
        #extracts page data
        pages = wikiData['query']['pages']
        page_id = list(pages.keys())[0]
        page = pages[page_id]

        #Handle missing pages
        
        if 'missing' in page:
            print("No Wikipedia page found for the provided name")
            sys.exit(2)
        revisions = page['revisions']
        for revision in revisions:
            timestamp = revision['timestamp']
            user = revision['user']
            print(f"{timestamp} {user}")
        sys.exit(0)
    except Exception as e:
        print("Network error occurred")
        sys.exit(3)

def main():
    wikiTitle = getWikiTitle()
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={wikiTitle}&rvprop=timestamp|user&rvlimit=30&redirects'
    sendRequest(url)
    
main()

