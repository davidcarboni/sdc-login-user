import requests
from json import dumps
from decoder import get_json


def get(url, parameters={}, headers={}):
    response = requests.get(url, params=parameters, headers=headers)
    return process(response)


def post(url, json, headers={}):
    headers["Content-Type"] = "application/json"
    response = requests.post(url, data=json, headers=headers)
    return process(response)


def process(response):
    if response.status_code < 400:
        #print(response.status_code)
        return {
            "status": response.status_code,
            "json": response.json()
        }
    else:
        return {
            "status": response.status_code,
            "text": response.text
        }


# Test the authentication / authorisation API

component = "sdc-login-user"
url = "https://" + component + ".herokuapp.com"
# url = "http://localhost:5000"
print(" >>> Testing " + component + " at " + url)


# Data we're going to work through


# Email address options

# email = "florence.nightingale@example.com"
# email = "chief.boyce@example.com"
email = "fireman.sam@example.com"
# email = "rob.dabank@example.com"


# Internet access code options

access_code = "abc123"
# access_code= "def456"
# access_code= "ghi789"


token = None
respondent_id = None


# Internet access code

uri = "/code"
print("\n --- " + uri + " ---")
input = {"code": access_code}
print(">>> " + repr(input))
result = post(url + uri, dumps(input))
if result["status"] == 200:
    json = result["json"]
    token = json["token"]
    print("<<< Token: " + token)
    content = get_json(token)
    print("Token content: " + repr(content))
    questionnaire_id = content["questionnaire_id"]
    print("questionnaire_id for internet access code " + access_code + " is " + str(questionnaire_id))
else:
    print("Error: " + str(result["status"]) + " - " + repr(result["text"]))


# Accout login

uri = "/login"
print("\n --- " + uri + " ---")
input = {"email": email}
print(">>> " + repr(input))
result = post(url + uri, dumps(input))
if result["status"] == 200:
    json = result["json"]
    token = json["token"]
    print("<<< Token: " + token)
    content = get_json(token)
    print("Token content: " + repr(content))
    respondent_id = content["respondent_id"]
    print("respondent_id for " + email + " is " + str(respondent_id))
else:
    print("Error: " + str(result["status"]) + " - " + repr(result["text"]))


# Profile

uri = "/profile"
print("\n --- " + uri + " (query) ---")
print(">>> (token content) " + repr(get_json(token)))
result = get(url + uri, headers={"token": token})
if result["status"] == 200:
    json = result["json"]
    print("<<< " + dumps(json))
else:
    print("Error: " + str(result["status"]) + " - " + repr(result["text"]))

uri = "/profile"
print("\n --- " + uri + " (update) ---")
print(">>> (token content) " + repr(get_json(token)))
result = post(url + uri, dumps({"name": "Spiderman"}), headers={"token": token})
if result["status"] == 200:
    json = result["json"]
    print("<<< " + dumps(json))
else:
    print("Error: " + str(result["status"]) + " - " + repr(result["text"]))


# Respondent units the respondent is associated with

respondent_units = []
uri = "/respondent_units"
print("\n --- " + uri + " ---")
print(">>> (token content) " + repr(get_json(token)))
result = get(url + uri, headers={"token": token})
if result["status"] == 200:
    json = result["json"]
    token = json["token"]
    print("<<< Token: " + token)
    content = get_json(token)
    print("Token content: " + repr(content))
    respondent_units = json["respondent_units"]
    print("<<< Associated respondent units: " + repr(respondent_units))
else:
    print("Error: " + str(result["status"]) + " - " + repr(result["text"]))


# Respondents for the respondent unit

uri = "/respondents"
if len(respondent_units) > 0:
    print("\n --- " + uri + " ---")
    reference = respondent_units[0]["reference"]
    print(">>> RU ref: " + repr(reference))
    parameters = {"reference": reference}
    result = get(url + uri, parameters=parameters, headers={"token": token})
    if result["status"] == 200:
        json = result["json"]
        print("<<< " + str(len(json)) + " result(s): " + repr(json))
    else:
        print("Error: " + str(result["status"]) + " - " + repr(result["text"]))
else:
    print(" * No respondent unit to query.")
