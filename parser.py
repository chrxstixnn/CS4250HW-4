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


def parse(col, url):
    context = ssl._create_unverified_context()
    html = urlopen(url, context=context).read()
    soup = BeautifulSoup(html, 'html.parser')

    professors = soup.find_all('div', class_='clearfix')

    for professor in professors:
        name = professor.find('h2')
        title = professor.find('strong', string=re.compile("Title"))
        office = professor.find('strong', string=re.compile("Office"))
        phone = professor.find('strong', string=re.compile("Phone"))
        email = professor.find('a')
        website = professor.find('a', href=re.compile("http://"))

        if name and name is not None:
            name = name.text
            print(name)
        if title and title is not None:
            title = title.next_sibling.text
            print(title)
        if office and office is not None:
            office = office.next_sibling.text
            print(office)
        if phone and phone is not None:
            phone = phone.next_sibling.text
            print(phone)
        if email and email is not None:
            email = email.text
            print(email)
        if website and website is not None:
            website = website.text
            print(website)

        if name is not None:
            col.insert_one({
                "name": name,
                "office": office,
                "phone": phone,
                "email": email,
                "website": website
            })

        print()
