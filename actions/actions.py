# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import json
# Reading the JSON provided file as Database
data = ""
with open("DatasetGovProc.json", encoding='UTF-8') as file:
    data = file.read()
    data = json.loads(data)

def get_matched_procedure(procedure :str):
    """This function takes the name of the procedure as input and returns 
    the maximum matching string extracted from `data`.
    
    `data` contains whole JSON file, saved globaly.

    Args:
        procedure (str): The name of the procedure

    Returns:
        _type_: `None` if the matching proportion is less than 30,
                    Otherwise, the `str` with the maximum matching ratio.
    """
    if procedure == None:   return None
    
    # Stroring all the names of the procedures in a list
    all_procedure_names = list()
    for i in range(len(data['data'][0])):
        proc_name = data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]
        all_procedure_names.append(str(proc_name).capitalize().strip())
    
    # Finding the only one string with maximum matching ratio and 
    # its matching ratio all available strings
    sentence, matching_ratio = process.extractOne(procedure, all_procedure_names, scorer=fuzz.token_sort_ratio)
    
    if matching_ratio >= 30:
        return sentence
    else:
        return None


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Okays?")

        return []

class ActionProcedureDescription(Action):
    
    def name(self) -> Text:
        return "action_procedure_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = None
        
        # storing the entity `procedure_name` received through intent
        received_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        
        print(received_procedure)
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        # Handling the exceptional case
        if required_procedure == None:
            dispatcher.utter_message(text=f"Provided procedure name does not found!<br>Please try re-phrasing it...")
            return []
        
        documentsToShow = ""
        
        # Searching the procedure name received in entity
        for i in range(len(data['data'][0])):
            if "documents" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                    listOfDocuments = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["documents"]
                    # Reteriving list of all the documents for a particular procedure and storing only names of
                    # all documents in formatted way
                    for i in range(1, len(listOfDocuments)+1):
                        document = str(listOfDocuments[i-1]["title"]).capitalize()
                        documentsToShow += f"{document}, "
                    documentsToShow = documentsToShow[:-2]
                    # Stop the search if the required procedure is found in the data
                    break
        
        # getting the name of the Receiving Administrations site.
        receivingAdministrations = ""
        for i in range(len(data['data'][0])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]:
                    receivingAdministrations = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]["title"]
                break
        
        documentsToShow += f" to the {receivingAdministrations}.<br>"
        
        
        final_text = f"You have to submit the following documents for {required_procedure}; {documentsToShow}"
        
        # getting the average delay for the procedure
        for i in range(len(data['data'][0])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "averageDelay" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                    timeDelayed = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["averageDelay"]
                    final_text += f"This procedure takes {timeDelayed} day(s)"
                break
        
        # getting the cost for the procedure
        for i in range(len(data['data'][0])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "price" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                    priceForProcedure = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["price"]
                    if priceForProcedure != 0:
                        final_text += f" and costs {priceForProcedure} dollars.<br>"
                    else:
                        final_text += f" and the procedure is free of cost.<br>"
                break
        
        # getting the administration incharge name.
        for i in range(len(data['data'][0])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]:
                    receivingAdministrationName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]["title"]
                    final_text += f"For more information , you can reach out to the {receivingAdministrationName}."
        
        dispatcher.utter_message(text=final_text)

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
                    documentsToShow += f"{i}. {document}.<br>"
                
                # Stop the search if the required procedure is found in the data
                break
        
        # getting the name of the Receiving Administrations site.
        receivingAdministrations = ""
        for i in range(len(data["subThematics"][0]["sub-subThematics"])):
            if required_procedure == data["subThematics"][0]["sub-subThematics"][i]["title"]:
                receivingAdministrations = data["subThematics"][0]["sub-subThematics"][i]["details"]["receivingAdministrations"][0]["title"]
        documentsToShow += f"These documents must be filed in {receivingAdministrations}."
        
        # Handling the exceptional case move this section to line no 105
        if required_procedure == None or documentsToShow == "":
            dispatcher.utter_message(text=f"Provided procedure name does not found!\nPlease try re-phrasing it...")
            return []
        
        dispatcher.utter_message(text=f"Here is the documents list:<br>{documentsToShow}")

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
