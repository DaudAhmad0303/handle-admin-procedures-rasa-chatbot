# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
with open("SampleData.json") as file:
    data = file.read()
    data = json.loads(data)

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World! --How are you?")

        return []

class ActionProcedureDescription(Action):
    
    def name(self) -> Text:
        return "action_procedure_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        print(required_procedure, "\n\n\n\n")
        # for i in range(len(data["subThematics"][0]["sub-subThematics"])):
        #     if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
        #         proc_name = data["subThematics"][0]["sub-subThematics"][i]["title"]
        #         listOfDocuments = data["subThematics"][0]["sub-subThematics"][0]["details"]["documents"]
        #         documents = list()
        #         for i in range(len(listOfDocuments)):
        #             documents.append(str(listOfDocuments[i]["title"]).capitalize())
        #         documentsToShow = ""
        #         for i in range(1, len(documents)+1):
        #             documentsToShow += f"{i}. {documents[i-1]}.\n"
        #         break
        
        # if required_procedure == None:
        #     dispatcher.utter_message(text=f"Provided procedure name does not found...")
        #     return []
        
        # dispatcher.utter_message(text=f"To get {required_procedure} you have to file the following documents:\n{documentsToShow} ")

        return []
