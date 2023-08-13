import os
from dotenv import load_dotenv
import requests

load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

auth_headers = {"authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"}


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


if __name__ == "__main__":
    print(get_all_contacts())
