from celery import shared_task
import time
import logging
from hubspot_api import get_just_applied_contacts, get_opportunity_contacts
import os
from dotenv import load_dotenv
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput
from django.core.mail import send_mail
from settings.settings import EMAIL_HOST_USER
from chatgpt import prepare_email_with_suggested_planes

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(message)s")

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
auth_headers = {"authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"}

client = hubspot.Client.create(access_token=HUBSPOT_ACCESS_TOKEN)


@shared_task
def debug_task():
    for i in range(10):
        logging.info(f"TESTING WORKER")
        time.sleep(0.3)
    return True


@shared_task
def send_welcome_email():
    just_applied_contacts = get_just_applied_contacts()

    properties = {"lifecyclestage": "lead"}
    simple_public_object_input = SimplePublicObjectInput(properties=properties)

    if just_applied_contacts:
        for contact in just_applied_contacts:
            api_response = client.crm.contacts.basic_api.update(
                contact_id=contact["id"],
                simple_public_object_input=simple_public_object_input,
            )

            logging.info(f"SUBSCRIBER -> LEAD\n {api_response}")

            send_mail(
                subject="Nikita from My New Wings",
                message=f"Dear {contact['properties']['firstname']} \n"
                f"Welcome to My New Wings family",
                from_email=EMAIL_HOST_USER,
                recipient_list=[contact["properties"]["email"]],
                fail_silently=False,
            )

            logging.info("WELCOME EMAIL HAS BEEN SENT")


@shared_task
def send_initial_plane_options_email():
    properties = {"lifecyclestage": "customer"}
    simple_public_object_input = SimplePublicObjectInput(properties=properties)

    validated_contacts = get_opportunity_contacts()

    if validated_contacts:
        for contact in validated_contacts:
            api_response = client.crm.contacts.basic_api.update(
                contact_id=contact["id"],
                simple_public_object_input=simple_public_object_input,
            )
            logging.info(f"OPPORTUNITY -> CUSTOMER\n {api_response}")

            message = prepare_email_with_suggested_planes(contact)
            print(message)

            send_mail(
                subject="Initial Plane Options",
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[contact["properties"]["email"]],
                fail_silently=False,
            )

            logging.info("INITIAL PLANE OPTIONS EMAIL HAS BEEN SENT")
