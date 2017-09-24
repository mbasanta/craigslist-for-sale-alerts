from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import post_listing_to_slack, send_listing_email
from slackclient import SlackClient
from urlparse import urlparse
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

import time
import settings
import requests
import sys
import json
import smtplib

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    name = Column(String)
    price = Column(Float)
    cl_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_postings_from_urls():
    """
    Scrapes Craigslist for a certain geographic area, and finds the latest listings.
    :return: A list of actually new results.
    """
    results = []

    for url in settings.LISTING_URLS:
        r = requests.get(url)
        response = r.text
        soup = BeautifulSoup(response, "html.parser")
        links = soup.find_all('p', {'class':'result-info'})

        for link in links:
            title = link.find('a', {'class':'result-title'})
            meta = link.find('span', {'class':'result-meta'})
            price = meta.find('span', {'class':'result-price'})
            date = link.find('time', {'class':'result-date'})

            result = {}
            result['name'] = title.text
            result['id'] = title['data-id']

            result['url'] = title['href']
            result['datetime'] = date['datetime']

            if price is not None:
                result['price'] = price.text
            else:
                result['price'] = ''

            results.append(result)

    return results


def scrape():
    """
    Scrapes Craigslist for a certain geographic area, and finds the latest listings.
    :return: A list of actually new results.
    """
    possible_results = get_postings_from_urls()
    new_results = []

    for result in possible_results:

        # For Debugging, print the craigslist ID
        #print result["id"]

        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                name=result["name"],
                price=price,
                cl_id=result["id"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()
            new_results.append(result)

    return new_results

def do_scrape():
    """
    Runs the Craigslist scraper, and posts data to slack/sends email. Optionally checks in with Dead Man's Snitch for monitoring.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Create a mail client and log in
    mail = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    mail.ehlo()
    mail.starttls()
    mail.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

    try:
        r = requests.get(settings.LISTING_URLS_JSON)
        json_data = json.loads(r.text)
        settings.LISTING_URLS = json_data['listing_urls']
        settings.EMAILS = json_data['emails']
    except Exception:
        print "Could not fetch listings from remote URL"
        pass

    # Get all the results from craigslist.
    all_results = scrape();

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to slack and email
    for result in all_results:
        post_listing_to_slack(sc, result)
        send_listing_email(mail, result)

    # Quit mail
    mail.quit()

    # Notify Dead Man's Snitch, if configured
    try:
        dms_msg = "Found %s results" % ( len(all_results) )
        dms = requests.post(settings.DMS_URL, data = { "m" : dms_msg })
    except Exception:
        pass

if __name__ == '__main__':
    do_scrape()

