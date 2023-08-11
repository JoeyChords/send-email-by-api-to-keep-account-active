import datetime, logging, time, requests
from dotenv import dotenv_values
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

config = dotenv_values(".env")
COLD_URL = config["COLD_URL"]
EMAIL_FROM = config["EMAIL_FROM"]
EMAIL_TO = config["EMAIL_TO"]
SENDGRID_API_KEY = config["SENDGRID_API_KEY"]
logging.basicConfig(filename="warmer.log", level=logging.INFO)
timeStarted = datetime.datetime.now()
logging.info(
    timeStarted.strftime("%m/%d/%Y, %H:%M:%S")
    + "   requestAndWarm started on "
    + COLD_URL
)
alertMessageMailed = False

while True:
    timeOfRequest = datetime.datetime.now()
    try:
        r = requests.get(COLD_URL)
        if r.status_code == 200:
            logging.info(
                timeOfRequest.strftime("%m/%d/%Y, %H:%M:%S")
                + "   "
                + COLD_URL
                + " returned status code "
                + str(r.status_code)
            )
            # Send an email alert when the website is online.
            if alertMessageMailed:
                message = Mail(
                    from_email=EMAIL_FROM,
                    to_emails=EMAIL_TO,
                    subject=COLD_URL + " is Online",
                    html_content="<strong>"
                    + COLD_URL
                    + " is online.</strong><br><br><strong>Status code = "
                    + str(r.status_code)
                    + "</strong>",
                )
                try:
                    sg = SendGridAPIClient(SENDGRID_API_KEY)
                    response = sg.send(message)
                    logging.info(
                        "  Alert message sent with Sendgrid. Site back online."
                    )
                    logging.info("  Sendgrid status: " + str(response.status_code))
                    logging.info(response.body)
                    logging.info(response.headers)
                    alertMessageMailed = False
                except Exception as e:
                    logging.info(e.message)
        else:
            raise Exception()
    except:
        logging.exception(
            timeOfRequest.strftime("%m/%d/%Y, %H:%M:%S")
            + "   Status code "
            + str(r.status_code)
        )
        # Send an email alert when something is wrong with the website.
        if not alertMessageMailed:
            message = Mail(
                from_email=EMAIL_FROM,
                to_emails=EMAIL_TO,
                subject="Problem with " + COLD_URL,
                html_content="<strong>Something is wrong with "
                + COLD_URL
                + "</strong><br><br><strong>Status code = "
                + str(r.status_code)
                + "</strong>",
            )
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                logging.info("  Alert message sent with Sendgrid. Site Error.")
                logging.info("  Sendgrid status: " + str(response.status_code))
                logging.info(response.body)
                logging.info(response.headers)
                alertMessageMailed = True
            except Exception as e:
                logging.info(e.message)
    time.sleep(840)
