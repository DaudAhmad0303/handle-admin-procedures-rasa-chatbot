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
        if isinstance(required_procedure ,str):
            required_procedure = required_procedure.capitalize()
        documentsToShow = ""
        
        # Searching the procedure name received in entity
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                listOfDocuments = data["subThematics"][0]["sub-subThematics"][i]["details"]["documents"]
                # Reteriving list of all the documents in json and storing only names of
                # all documents in formatted way
                for i in range(1, len(listOfDocuments)+1):
                    document = str(listOfDocuments[i-1]["title"]).capitalize()
                    documentsToShow += f"{document}, "
                documentsToShow = documentsToShow[:-2]
                # Stop the search if the required procedure is found in the data
                break
        
        # getting the name of the Receiving Administrations site.
        receivingAdministrations = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                receivingAdministrations = data["subThematics"][0]["sub-subThematics"][i]["details"]["receivingAdministrations"][0]["title"]
        else:
            documentsToShow += f" in {receivingAdministrations}."
        
        # Handling the exceptional case
        if required_procedure == None or documentsToShow == "":
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=f"To get {required_procedure}, you have to file the following documents; {documentsToShow} ")

        return []

class ActionProcedureDocuments(Action):
    
    def name(self) -> Text:
        return "action_procedure_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        print(required_procedure, type(required_procedure))
        if isinstance(required_procedure ,str):
            required_procedure = required_procedure.capitalize()
        documentsToShow = ""
        
        # Searching the procedure name received in entity
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                listOfDocuments = data["subThematics"][0]["sub-subThematics"][i]["details"]["documents"]
                # Reteriving list of all the documents in json and storing only names of
                # all documents in formatted way
                for i in range(1, len(listOfDocuments)+1):
                    document = str(listOfDocuments[i-1]["title"]).capitalize()
                    documentsToShow += f"{i}. {document}.\n"
                
                # Stop the search if the required procedure is found in the data
                break
        
        # getting the name of the Receiving Administrations site.
        receivingAdministrations = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                receivingAdministrations = data["subThematics"][0]["sub-subThematics"][i]["details"]["receivingAdministrations"][0]["title"]
        documentsToShow += f"These documents must be filed in {receivingAdministrations}."
        
        # Handling the exceptional case
        if required_procedure == None or documentsToShow == "":
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=f"Here is the documents list:\n{documentsToShow}")

        return []

class ActionProcedureDeliveringAdministrations(Action):
    
    def name(self) -> Text:
        return "action_procedure_delivering_administrations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        if isinstance(required_procedure ,str):
            required_procedure = required_procedure.capitalize()
        outputToShow = ""

        # getting the name of the Delivering Administrations site.
        deliveringAdministrations = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                deliveringAdministrations = data["subThematics"][0]["sub-subThematics"][i]["details"]["deliveringAdministrations"][0]["title"]
        outputToShow += f"You can get it from {deliveringAdministrations}."
        
        # Handling the exceptional case
        if required_procedure == None or outputToShow == "":
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=outputToShow)

        return []

class ActionProcedurePrice(Action):
    
    def name(self) -> Text:
        return "action_procedure_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        if isinstance(required_procedure ,str):
            required_procedure = required_procedure.capitalize()

        # getting the price for the procedure.
        price = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                price = data["subThematics"][0]["sub-subThematics"][i]["details"]["price"]
        
        # Handling the exceptional case
        if required_procedure == None:
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=f"The procedure costs {price}.")

        return []

class ActionProcedureDelay(Action):
    
    def name(self) -> Text:
        return "action_procedure_delay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        if isinstance(required_procedure ,str):
            required_procedure = required_procedure.capitalize()

        # getting the time delay for the procedure.
        delay = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                delay = data["subThematics"][0]["sub-subThematics"][i]["details"]["delay"]
        
        # Handling the exceptional case
        if required_procedure == None:
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=f"The procedure takes {delay} days.")

        return []
