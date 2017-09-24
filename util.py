import settings
import math
from email.mime.text import MIMEText

def post_listing_to_slack(sc, listing):
    """
    Posts the listing to slack.
    :param sc: A slack client.
    :param listing: A record of the listing.
    """
    desc = "{0} | {1} | <{2}>".format( listing["price"], listing["name"], listing["url"])
    sc.api_call(
        "chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
        username='pybot', icon_emoji=':robot_face:'
    )

def send_listing_email(mail, listing):
    """
    Send the listing via email
    :param mail: A mail client.
    :param listing: A record of the listing.
    """

    email_from = "Craigslist Checker Bot"
    email_space = ", "

    message = "%s \n\n" % (listing["name"])
    message += "%s \n\n" % (listing["price"])
    message += "%s \n\n" % (listing["url"])

    msg = MIMEText(message)
    msg['Subject'] = listing["name"]
    msg['From'] = email_from

    emails = settings.EMAIL_RECIPIENTS
    msg['To'] = emails[0]
    mail.sendmail(email_from, emails, msg.as_string())




