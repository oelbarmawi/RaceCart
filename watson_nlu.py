import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions

API_KEY = "HLiuAqMBW9td4_lrcKwo67alISdgzflsv0u3KwxggLkz"
URL = "https://gateway.watsonplatform.net/natural-language-understanding/api"

TARGETS = ['peanut butter', 'milk', 'eggs']
item_locations = {'peanut butter': 'aisle 6', 'milk': 'aisle 9', 'eggs': 'aisle 16'}



def createResponse(raw_text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        iam_apikey=API_KEY,
        url=URL
    )

    response = natural_language_understanding.analyze(
        # url='www.ibm.com',
        text=raw_text,
        features=Features(sentiment=SentimentOptions(targets=TARGETS))).get_result()
    # print(json.dumps(response, indent=2))

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



if __name__ == '__main__':
    SAMPLE_TEXT1 = "Where is the peanut butter, and eggs?"
    SAMPLE_TEXT2 = "Where's the milk"
    SAMPLE_TEXT3 = "I'm looking for eggs today."

    print(createResponse(SAMPLE_TEXT1), "\n")
    print(createResponse(SAMPLE_TEXT2), "\n")
    print(createResponse(SAMPLE_TEXT3), "\n")



