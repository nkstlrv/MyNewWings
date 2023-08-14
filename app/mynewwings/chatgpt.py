import os
from dotenv import load_dotenv
import openai

load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")

openai.api_key = API_KEY


def demo_prompt():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Say hello"}]
    )
    print(response)


def prepare_email_with_suggested_planes(contact: dict):
    name = contact["properties"]["firstname"]
    flight_objective = contact["properties"]["preferences"]
    aerodromes_to_use = contact["properties"]["aerodromes"]
    meteo_conditions_to_fly = contact["properties"]["conditions"]
    number_of_engines = contact["properties"]["engines"]
    nav_instruments = contact["properties"]["instruments"]
    approx_budget = contact["properties"]["budget"]
    additional_info = contact["properties"]["comments"]

    prompt = (
        f"You are general aviation estate agent. Your responsibilities are preparing initial 3 planes "
        "that approximately match customers application form data. We are not selling planes, only suggesting and than"
        "proceeding deal. Planes to suggest are general aviation ones. "
        "Do not suggest business jets"
        "The answer should be in a format of email, but do not write subject. "
        "Our slogan is 'Feel the Freedom of Being Winged'"
        "Company name is My New Wings. Here are data: customer name - "
        f"{name}, flying objectives - {flight_objective}, type of aerodrome pavement to use - {aerodromes_to_use}, "
        f"meteorological conditions to be able to fly in - {meteo_conditions_to_fly}, engine-amount configuration - "
        f"{number_of_engines}, navigational equipment and instruments configuration - {nav_instruments}, "
        f"approximate budget range in US dollars - {approx_budget}, additional information - {additional_info} ("
        f"use additional information only if it does not contradict the original configuration "
        f"and is important and logical). Add short description of each aircraft to highlight their advantages. "
        f"At the end say that customer will have a personal manager will contact soon and together "
        f"with customer they will continue cooperation. Beginning - Dear {name}; "
        f"Ending - Feel the freedom of being winged! Best regards, My New Wings team. Leave contacts: +1-541-754-3010"
        f" support@mynewwings.com"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = response["choices"][0]["message"]["content"]
    return response_text


if __name__ == "__main__":
    ...
