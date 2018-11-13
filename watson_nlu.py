import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions

API_KEY = "HLiuAqMBW9td4_lrcKwo67alISdgzflsv0u3KwxggLkz"
URL = "https://gateway.watsonplatform.net/natural-language-understanding/api"

TARGETS = ['peanut butter', 'milk', 'eggs']
item_locations = {'peanut butter': 'aisle 6', 'milk': 'aisle 9', 'eggs': 'aisle 16'}



def createResponse():
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey=API_KEY,
    url=URL
)



SAMPLE_TEXT = "Where is the peanut butter, and eggs?"

response = natural_language_understanding.analyze(
    # url='www.ibm.com',
    text=SAMPLE_TEXT,
    features=Features(sentiment=SentimentOptions(targets=TARGETS))).get_result()


response_targets = response['sentiment']['targets']
response_items = []
response_locations = []
for r in response_targets:
	item = r['text']
	if item in item_locations:
		response_items.append(item)
		response_locations.append(item_locations[item])

response_string = "For the items: " + ", ".join(response_items) + ".\nGo to " + ", ".join(response_locations)
print(response_string)




# print(json.dumps(response, indent=2))
