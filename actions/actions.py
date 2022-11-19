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
with open("data.json", encoding='UTF-8') as file:
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
    for i in range(len(data['data'])):
        proc_name = data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]
        all_procedure_names.append(proc_name)
    
    # Finding the only one string with maximum matching ratio and 
    # its matching ratio all available strings
    sentence, matching_ratio = process.extractOne(procedure, all_procedure_names, scorer=fuzz.token_sort_ratio)
    # print(sentence, matching_ratio)
    if matching_ratio >= 70:
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
        
        # print(received_procedure, self.name())
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        documentsToShow = ""
        final_text = ""
        receivingAdministrations = ""
        timeDelayed = ""
        
        # Searching the procedure name received in entity
        for i in range(len(data['data'])):
            if "documents" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                    listOfDocuments = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["documents"]
                    # Reteriving list of all the documents for a particular procedure and storing only names of
                    # all documents in formatted way
                    for i in range(1, len(listOfDocuments)+1):
                        document = str(listOfDocuments[i-1]["title"]).capitalize()
                        documentsToShow += f"{i}) {document}.<br>"
                    documentsToShow = documentsToShow[:-4]
                    
                    # getting the name of the Receiving Administrations site.
                    if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]:
                        receivingAdministrations = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]["title"]
                    
                    final_text = f"Vous devez soumettre les documents suivants :<br> {documentsToShow} au niveau de {receivingAdministrations}.<br>"
                    
                    # getting the average delay for the procedure
                    if "averageDelay" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                        timeDelayed = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["averageDelay"]
                    
                    final_text += f"La procédure prend {timeDelayed} jour(s).<br>"
                    
                    # getting the cost for the procedure
                    if "price" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                        priceForProcedure = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["price"]
                        if priceForProcedure != 0:
                            final_text += f"Elle coute {priceForProcedure} DHs.<br>"
                        else:
                            final_text += f"Cette procédure est gratuite.<br>"
                    
                    # getting the administration incharge name.
                    if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]:
                        administrationInChargeName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]["title"]
                        final_text += f"Pour plus d'informations , veuillez contacter {administrationInChargeName}."
                    
                    # Stop the search if the required procedure is found in the data
                    break
        
        # Handling the exceptional case
        if required_procedure == None or final_text == "":
            dispatcher.utter_message(text=f"La procédure demandée n'existe pas .Merci de bien vouloir la reformuler...")
            return []
        
        dispatcher.utter_message(text=final_text)

        return []

class ActionProcedureDocuments(Action):
    
    def name(self) -> Text:
        return "action_procedure_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = None
        
        # storing the entity `procedure_name` received through intent
        received_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        
        # print(received_procedure, self.name())
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        documentsToShow = ""
        final_text = ""
        
        # Searching the procedure name received in entity
        for i in range(len(data['data'])):
            if "documents" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                    listOfDocuments = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["documents"]
                    # Reteriving list of all the documents for a particular procedure and storing only names of
                    # all documents in formatted way
                    for i in range(1, len(listOfDocuments)+1):
                        document = str(listOfDocuments[i-1]["title"]).capitalize()
                        documentsToShow += f"{i}) {document}.<br>"
                    documentsToShow = documentsToShow[:-4]
                    
                    final_text = f"Voici la liste des documents requis :<br>{documentsToShow}"
                    
                    # Stop the search if the required procedure is found in the data
                    break
        
        # Handling the exceptional case
        if required_procedure == None or final_text == "":
            dispatcher.utter_message(text=f"La procédure demandée n'existe pas .Merci de bien vouloir la reformuler...")
            return []
        
        dispatcher.utter_message(text=final_text)

        return []

class ActionProcedureDeliveringAdministrations(Action):
    
    def name(self) -> Text:
        return "action_procedure_delivering_administrations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = None
        
        # storing the entity `procedure_name` received through intent
        received_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        
        # print(received_procedure, self.name())
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        outputToShow = ""

        # getting the name of the Delivering Administrations site.
        deliveringAdministrations = ""
        for i in range(len(data['data'])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]:
                    deliveringAdministrations = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]["title"]
                
                if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]:
                    AdministrationInchargeName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]["title"]
                outputToShow += f"Cette procédure est sous la responsabilité de {AdministrationInchargeName}."
        
        # Handling the exceptional case
        if required_procedure == None or outputToShow == "":
            dispatcher.utter_message(text=f"La procédure demandée n'existe pas .Merci de bien vouloir la reformuler...")
            return []
        
        dispatcher.utter_message(text=outputToShow)

        return []

class ActionProcedurePrice(Action):
    
    def name(self) -> Text:
        return "action_procedure_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = None
        
        # storing the entity `procedure_name` received through intent
        received_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        
        # print(received_procedure, self.name())
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        final_text = ""
        # getting the price for the procedure.
        for i in range(len(data['data'])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "price" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                    priceForProcedure = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["price"]
                    priceForProcedure = int(str(priceForProcedure).strip())
                    if priceForProcedure != 0:
                        final_text += f"Elle coute {priceForProcedure} DHs."
                    else:
                        final_text += f"Cette procédure est gratuite."
                break
        
        # Handling the exceptional case
        if required_procedure == None or final_text == "":
            dispatcher.utter_message(text=f"La procédure demandée n'existe pas .Merci de bien vouloir la reformuler...")
            return []

        dispatcher.utter_message(text=final_text)
        return []

class ActionProcedureDelay(Action):
    
    def name(self) -> Text:
        return "action_procedure_delay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        required_procedure = None
        
        # storing the entity `procedure_name` received through intent
        received_procedure = next(tracker.get_latest_entity_values("procedure_name"), None)
        
        # print(received_procedure, self.name())
        # getting the most possible matching procedure name from the database, 
        # if the user mis-spelled the procedure name
        required_procedure = get_matched_procedure(received_procedure)
        
        # getting the time delay for the procedure.
        final_text = ""
        for i in range(len(data['data'])):
            if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
                if "averageDelay" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
                    timeDelayed = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["averageDelay"]
                    final_text += f"La procédure prend {timeDelayed} jour(s)."
                break
        
        # Handling the exceptional case
        if required_procedure == None or final_text == "":
            dispatcher.utter_message(text=f"La procédure demandée n'existe pas .Merci de bien vouloir la reformuler...")
            return []
        
        dispatcher.utter_message(text=final_text)

        return []
