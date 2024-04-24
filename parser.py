import ssl
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

DB_NAME = "Homework4"
DB_HOST = "localhost"
DB_PORT = 27017

#connect database
def connect_to_mongodb():
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db

    except:
        print("Database not connected successfully")

# method to parse through the permanent faculty page
def parse(col, url):

    # gets the html of the website
    context = ssl._create_unverified_context()
    html = urlopen(url, context=context).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Gets the html of each professor
    professors = soup.find_all('div', class_='clearfix')

    # parses through each professor and finds all the information
    for professor in professors:
        name = professor.find('h2')
        title = professor.find('strong', string=re.compile("Title"))
        office = professor.find('strong', string=re.compile("Office"))
        phone = professor.find('strong', string=re.compile("Phone"))
        email = professor.find('a')
        website = professor.find('a', href=re.compile("http://"))

        # Checks if each field has a value and then converts
        # the value to text
        if name and name is not None:
            name = name.text

        # checks if title has value
        if title and title is not None:
            title = title.next_sibling.text

        # checks if office has a value
        if office and office is not None:
            office = office.next_sibling.text

        # checks if phone has a value
        if phone and phone is not None:
            phone = phone.next_sibling.text

        # checks if email has a value
        if email and email is not None:
            email = email.text

        # checks if website has a value
        if website and website is not None:
            website = website.text

        # inserts each of those fields into MongoDB
        if name is not None:
            col.insert_one({
                "name": name,
                "office": office,
                "phone": phone,
                "email": email,
                "website": website
            })
