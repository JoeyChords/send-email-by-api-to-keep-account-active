import datetime, logging, time
from dotenv import dotenv_values
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

config = dotenv_values(".env")
EMAIL_FROM = config["EMAIL_FROM"]
EMAIL_TO = config["EMAIL_TO"]
SENDGRID_API_KEY = config["SENDGRID_API_KEY"]
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

message = Mail(
    from_email=EMAIL_FROM,
    to_emails=EMAIL_TO,
    subject="This Account is Active",
    html_content="<strong>contact@headlinefights.com still has an active API key.</strong><br><br><strong>",
)

while True:
    timeOfRequest = datetime.datetime.now()

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(
            timeStarted.strftime("%m/%d/%Y, %H:%M:%S")
            + "   Sent email from "
            + EMAIL_FROM
        )
        logging.info("  Sendgrid status: " + str(response.status_code))
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.info(e.message)
    time.sleep(86400)
