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

## Put Craigslist ID of the Craigslist item to delete here
cl_id_to_delete = 1234567890

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

rows = session.query(Listing).count()
print "%s rows in database" % (rows)

listings = session.query(Listing).order_by(Listing.id.desc())

i = 0
for listing in listings:
    if( i > 15):
        break
    print "%s: %s - %s" % (listing.id,listing.name, listing.cl_id)
    i+=1

session.query(Listing).filter_by(cl_id=cl_id_to_delete).delete()
session.commit()
print
print "Deleted: %s " % (cl_id_to_delete)

rows = session.query(Listing).count()
print "%s rows in database" % (rows)