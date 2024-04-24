import ssl
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
import queue
from bs4 import BeautifulSoup
from pymongo import MongoClient
from connection import connectDataBase, createPage
from parser import connect_to_mongodb, parse


def crawlerThread(frontier):
    # keeps track of all visited URLs
    visited = []
    count = 0

    # while there are still URLs in the frontier
    while frontier:

        # gets the first element of the queue
        url = frontier[count]

        # checks if url is in the visited array
        if url not in visited:
            visited.append(url)

        # Gets the html text of the current url
        the_html = retrieveHTML(url)

        #stores URL and html in mongo db
        createPage(pages, url, the_html)

        # checks if the html contains the "Permanent Faculty" heading
        if the_html.find('h1', string="Permanent Faculty"):
            print("permanent page found")
            frontier = []
            return url
        else:
            # gets all links in the html
            parsed = the_html.find_all('a')

            for link in parsed:
                # gets the actual link of <a>
                just_link = link.get('href')

                # checks if link is without domain and adds it if its missing
                if just_link.startswith('/sci/computer-science/'):
                    just_link = "https://www.cpp.edu" + just_link

                    # adds link if not visited and not in frontier
                    if just_link not in visited and just_link not in frontier:
                        frontier.append(just_link)

        count = count + 1

# function that uses beautiful soup to get the html of the link
def retrieveHTML(url):
    context = ssl._create_unverified_context()

    html = urlopen(url, context=context).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#seed URL
seed = "https://www.cpp.edu/sci/computer-science/"
frontier = [seed]
db = connectDataBase()
pages = db.pages

# calls crawler method
url = crawlerThread(frontier)

# connects database for parser
db2 = connect_to_mongodb()
professors = db2.professors
parse(professors, url)
