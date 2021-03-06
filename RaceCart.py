import json
import requests
from flask import Flask, request
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from pymessenger.bot import Bot

FB_API_URL = "https://graph.facebook.com/v2.6/me/messages"
IBM_API_KEY = "HLiuAqMBW9td4_lrcKwo67alISdgzflsv0u3KwxggLkz"
URL = "https://gateway.watsonplatform.net/natural-language-understanding/api"

TARGETS = ['peanut butter', 'milk', 'eggs', 'fruit', 'pasta sauce', 'cereal']
item_locations = {'peanut butter': 'Aisle 6', 'milk': 'Aisle 9', 'eggs': 'Aisle 16', 'fruit': 'Aisle 2', 'pasta sauce': 'Aisle 14', 'cereal': 'Aisle 19'}

app = Flask(__name__)
FB_ACCESS_TOKEN = 'EAAC7ZC1ZAgpTQBABQy4KUy27rOWr7VFLQ16Ok0CHo6lrqh84aT8mFq7xdJp5sHy0wSQYE7nZA6RyN5DW4vxpYZBgiyBNHcIGUC0GXwyZCADwSZB8TuBCPFqdbFnjou40q5WabIwZAIcVU2fHVJSM9KwtlT99BiUxkd8d2C52EuynAZDZD'
FB_VERIFY_TOKEN = 'racecat_watson_nlu'
bot = Bot(FB_VERIFY_TOKEN)

@app.route('/')
@app.route('/watson_nlu_test', methods=['POST', 'GET'])
def testWatsonNLU():
    if request.method == 'GET':
        # return "It's working."
        return createResponse("Where is the milk?")
    else:
        # req = request.json()
        sample_texts = ["Where is the peanut butter, and eggs?", "Where's the milk", "I'm looking for eggs today."]
        return_string = ""
        for sample_text in sample_texts:
            return_string += createResponse(sample_text) + "\n"
        return return_string

@app.route('/watson_nlu', methods=['POST', 'GET'])
def watsonNLU():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        #Echo
        req = request.get_json()
        print("THE JSON",json.dumps(req))
        for event in req['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = createResponse(message['message']['text'])
                        send_message_new(recipient_id, response_sent_text)
                        return 'Message sent.'
        # return return_string
        return 'Message not sent.'

def createResponse(raw_text):
    raw_text = raw_text.lower()
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        iam_apikey=IBM_API_KEY,
        url=URL
    )
    try:
        response = natural_language_understanding.analyze(
            # url='www.ibm.com',
            text=raw_text,
            features=Features(sentiment=SentimentOptions(targets=TARGETS))).get_result()
        # print(json.dumps(response, indent=2))
    except:
        return "I'm sorry, I did not understand. Can you repeat that?"
    return getItemLocations(response)


def getItemLocations(response):
    response_items, response_locations = [], []
    response_targets = response['sentiment']['targets']
    
    for r in response_targets:
        item = r['text']
        if item in item_locations:
            response_items.append(item)
            response_locations.append(item_locations[item])

    response_string = "For the items: " + ", ".join(response_items) + ".\nGo to " + ", ".join(response_locations)
    return response_string

def verify_fb_token(token_sent):
    if token_sent == FB_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def send_message_new(recipient_id, response):
    payload = {
        "message_type": "RESPONSE",
        "recipient": {
            "id": recipient_id,
        },
        "message": {
            "text": response
        }
    }
    auth = {
        "access_token": FB_ACCESS_TOKEN
    }
    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )
    return response.json()

if __name__ == '__main__':
    app.run()
