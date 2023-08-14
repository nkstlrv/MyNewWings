import os
from dotenv import load_dotenv
import requests
import hubspot

# from hubspot.crm.contacts import SimplePublicObjectInput
# from django.core.mail import send_mail
# from settings.settings import EMAIL_HOST_USER
# from chatgpt import prepare_email_with_suggested_planes

load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

auth_headers = {"authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"}

client = hubspot.Client.create(access_token=HUBSPOT_ACCESS_TOKEN)


def get_all_contacts():
    base_url = "https://api.hubspot.com/crm/v3/objects/contacts"
    properties = (
        "?properties=firstname,email,status,phone,lifecyclestage,aerodromes,budget,"
        "comments,conditions,engines,instruments,preferences"
    )

    response = requests.get(url=base_url + properties, headers=auth_headers)
    response.raise_for_status()

    data = response.json()

    if data and data.get("results"):
        all_contacts: list = data["results"]
        return all_contacts

    return None


def get_just_applied_contacts():
    all_contacts = get_all_contacts()

    just_applied = [
        contact
        for contact in all_contacts
        if contact.get("properties")["lifecyclestage"] == "subscriber"
    ]

    return just_applied


def get_verified_lead_contacts():
    """
    Contacts to which initial emails were send
    """
    all_contacts = get_all_contacts()

    lead_contacts = [
        contact
        for contact in all_contacts
        if contact.get("properties")["lifecyclestage"] == "lead"
    ]

    return lead_contacts


def get_opportunity_contacts():
    """
    Contacts that are manually verified by a manager
    """
    all_contacts = get_all_contacts()

    opportunity_contacts = [
        contact
        for contact in all_contacts
        if contact.get("properties")["lifecyclestage"] == "opportunity"
    ]

    return opportunity_contacts


def get_customer_contacts():
    """
    Contacts that received initial aircraft match
    """
    all_contacts = get_all_contacts()

    customer_contacts = [
        contact
        for contact in all_contacts
        if contact.get("properties")["lifecyclestage"] == "customer"
    ]

    return customer_contacts


# def send_welcome_email():
#     just_applied_contacts = get_just_applied_contacts()
#
#     properties = {"lifecyclestage": "lead"}
#     simple_public_object_input = SimplePublicObjectInput(properties=properties)
#
#     if just_applied_contacts:
#         for contact in just_applied_contacts:
#             api_response = client.crm.contacts.basic_api.update(
#                 contact_id=contact["id"],
#                 simple_public_object_input=simple_public_object_input,
#             )
#             print(api_response)
#
#             send_mail(
#                 subject="Nikita from My New Wings",
#                 message=f"Dear {contact['properties']['firstname']} \n"
#                 f"Welcome to My New Wings family",
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[contact["properties"]["email"]],
#                 fail_silently=False,
#             )
#
#             print("Wellcome email has been sent")
#
#
# def send_initial_plane_options_email():
#     properties = {"lifecyclestage": "customer"}
#     simple_public_object_input = SimplePublicObjectInput(properties=properties)
#
#     validated_contacts = get_opportunity_contacts()
#
#     if validated_contacts:
#         for contact in validated_contacts:
#             api_response = client.crm.contacts.basic_api.update(
#                 contact_id=contact["id"],
#                 simple_public_object_input=simple_public_object_input,
#             )
#             print(api_response)
#
#             message = prepare_email_with_suggested_planes(contact)
#             print(message)
#
#             send_mail(
#                 subject="Initial Plane Options",
#                 message=message,
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[contact["properties"]["email"]],
#                 fail_silently=False,
#             )
#
#             print("Initial plane options email has been sent")


if __name__ == "__main__":
    print(get_all_contacts())
