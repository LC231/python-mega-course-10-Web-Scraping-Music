import requests
import selectorlib
import os
import smtplib, ssl
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '\
    'AppleWebKit/537.36 '\
    '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db", timeout=10)



def scrape(URL):
    """ Scrape the page source from the URL"""
    response = requests.get(URL, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value
    

def send_email(message):
    host = "smtp.gmail.com" 
    port = 465

    username = "231lukecurran@gmail.com"
    password = os.getenv("PASSWORD")
    reciever = "231lukecurran@gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, reciever, message)


def store(extracted):
     row = extracted.split(",")
     row = [item.strip() for item in row]
     cursor = connection.cursor()
     cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
     connection.commit()


def read(extracted):
     row = extracted.split(",")
     row = [item.strip() for item in row]
     band, city, date = row
     cursor = connection.cursor()
     cursor.execute("SELECT * FROM events WHERE band=? \
                    AND city=? AND date=?", (band, city, date))
     rows = cursor.fetchall()
     print(rows)
     return rows



if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
    
        
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey, new event was found!")
        time.sleep(2)