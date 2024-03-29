import json
with open("data.json", encoding='UTF-8') as file:
    data = file.read()
    data = json.loads(data)
required_procedure = "Medical certificate for drinving license"
# # Previouse Document ('SampleData.json') based Extracting
# # For Searching the procedure name in JSON
# proc_name = data["subThematics"][0]["sub-subThematics"][0]["title"]
# print("Procedure Name:", str(proc_name).capitalize())

# # For Searching the procedure Description in JSON
# proc_description = data["subThematics"][0]["sub-subThematics"][0]["description"]
# print("Procedure Description:", str(proc_description).capitalize())

# # To print the receiving administration name
# receivingAdministrationName = data["subThematics"][0]["sub-subThematics"][0]["details"]["receivingAdministrations"][0]["title"]
# print("Procedure Receiving Administration:", receivingAdministrationName)

# # To print the delay in service
# timeDelayed = data["subThematics"][0]["sub-subThematics"][0]["details"]["delay"]
# print("Time Taken for Procedure:", timeDelayed)

# # To print the price to pay for a Procedure
# priceForProcedure = data["subThematics"][0]["sub-subThematics"][0]["details"]["price"]
# print("Money to Pay for Procedure:", priceForProcedure)

# # To print the Documents required for a procedure
# listOfDocuments = data["subThematics"][0]["sub-subThematics"][0]["details"]["documents"]
# documents = list()
# for i in range(len(listOfDocuments)):
#     documents.append(str(listOfDocuments[i]["title"]).capitalize())
# print("Following documents are required for the specified procedure:")
# for i in range(1, len(documents)+1):
#     print(f"{i}. {documents[i-1]}.")

# -----------------------------------------------------------------------------------------------------------------

# # New Document ('DatasetGovProc.json') based Extracting
# For Searching the procedure name in JSON
# for i in range(len(data['data'])):
#     if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]:
#         proc_name = data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]
#         print("Procedure Name:", str(proc_name).capitalize())

# # For Searching the procedure Description in JSON
# for i in range(len(data['data'])):
#     if "description" in data["data"][i]["subThematics"][0]["govprocedure"][0]:
#         proc_description = data["data"][i]["subThematics"][0]["govprocedure"][0]["description"]
#         print("Procedure Description:", str(proc_description).capitalize())

# # To print the receiving administration name
# for i in range(len(data['data'])):
#     if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]:
#         receivingAdministrationName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["receivingAdministrations"][0]["title"]
#         print("Procedure Receiving Administration:", receivingAdministrationName)

# # To print the delivering administration name
for i in range(len(data['data'])):
    if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["deliveringAdministrations"][0]:
        deliveringAdministrationName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["deliveringAdministrations"][0]["title"]
        print("Procedure Delivering Administration:", deliveringAdministrationName)

# # To print the administration Incharge name
# for i in range(len(data['data'])):
#     if "title" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]:
#         receivingAdministrationName = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["administrationInCharge"]["title"]
#         print("Procedure Administration Incharge:", receivingAdministrationName)

# # To print the average delay in service
# for i in range(len(data['data'])):
#     if "averageDelay" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
#         timeDelayed = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["averageDelay"]
#         print("Time Taken for Procedure:", timeDelayed)

# # To print the price to pay for a Procedure
# for i in range(len(data['data'])):
#     if required_procedure == data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]:
#         if "price" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
#             priceForProcedure = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["price"]
#             print("Money to Pay for Procedure:", priceForProcedure)

# # To print the Documents required for a procedure
# for i in range(len(data['data'])):
#     if "documents" in data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]:
#         listOfDocuments = data["data"][i]["subThematics"][0]["govprocedure"][0]["details"]["documents"]
#         documents = list()
#         for i in range(len(listOfDocuments)):
#             documents.append(str(listOfDocuments[i]["title"]).capitalize())
#         print("Following documents are required for the specified procedure:")
#         for i in range(1, len(documents)+1):
#             print(f"{i}. {documents[i-1]}.")
#         print()
