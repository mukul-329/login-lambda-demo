import os
import html
import json
import boto3


ses = boto3.client("ses")


FROM_EMAIL = os.environ["FROM_EMAIL"]
TO_EMAIL = os.environ["TO_EMAIL"]


def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))

    email = html.escape(body.get("email", ""))
    contact = html.escape(body.get("contact", ""))
    message = html.escape(body.get("message", ""))

    message = message.replace("\n", "<br>")


    # Read HTML template
    template_path = os.path.join(
        os.path.dirname(__file__),
        "email_body.html"
    )

    with open(template_path, "r", encoding="utf-8") as file:
        email_body = file.read()


    # Replace placeholders
    email_body = email_body.replace(
        "{email}",
        email
    )

    email_body = email_body.replace(
        "{contact}",
        contact
    )

    email_body = email_body.replace(
        "{message}",
        message
    )


    # Send email
    ses.send_email(

        Source=FROM_EMAIL,

        Destination={
            "ToAddresses": [
                TO_EMAIL
            ]
        },

        ReplyToAddresses=[
            email
        ],

        Message={

            "Subject": {
                "Data": "New Contact Request — Portfolio"
            },

            "Body": {

                "Html": {
                    "Data": email_body
                },

                "Text": {
                    "Data": f"""
New Contact Request

Email: {email}
Contact: {contact}

Message:
{message}
"""
                }

            }

        }

    )


    return {

        "statusCode": 200,

        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },

        "body": json.dumps({
            "message": "Message sent successfully!"
        })

    }