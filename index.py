import datetime, logging, time
from dotenv import load_dotenv
import os
import resend

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]

logging.basicConfig(filename="apiSender.log", level=logging.INFO)
timeStarted = datetime.datetime.now()
logging.info(
    timeStarted.strftime("%m/%d/%Y, %H:%M:%S")
    + "   SendEmailByApiToKeepAccountActive started."
)

print(
    "SendEmailByApiToKeepAccountActive was started: "
    + timeStarted.strftime("%m/%d/%Y, %H:%M:%S")
)

params = {
    "from": EMAIL_FROM,
    "to": [EMAIL_TO],
    "subject": "Headline Fights Still Has Working Email",
    "html": "<strong>The Headline Fights domain still has an active email API key.</strong><br><br><strong>"
}

while True:
    timeEmailSent = datetime.datetime.now()

    try:
        response = resend.Emails.send(params)
        logging.info(
            timeEmailSent.strftime("%m/%d/%Y, %H:%M:%S")
            + "   Sent email from "
            + EMAIL_FROM
        )
        logging.info("  Resend.com email: " + str(response))
    except Exception as e:
        logging.info(e.message)
    time.sleep(86400)
