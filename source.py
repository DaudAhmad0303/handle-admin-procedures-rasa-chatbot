import json
with open("SampleData.json") as file:
    data = file.read()
    data = json.loads(data)


# For Searching the procedure name in JSON
proc_name = data["subThematics"][0]["sub-subThematics"][0]["title"]
print("Procedure Name:", str(proc_name).capitalize())

# For Searching the procedure Description in JSON
proc_description = data["subThematics"][0]["sub-subThematics"][0]["description"]
print("Procedure Description:", str(proc_description).capitalize())

# To print the receiving administration name
receivingAdministrationName = data["subThematics"][0]["sub-subThematics"][0]["details"]["receivingAdministrations"][0]["title"]
print("Procedure Receiving Administration:", receivingAdministrationName)

# To print the delay in service
timeDelayed = data["subThematics"][0]["sub-subThematics"][0]["details"]["delay"]
print("Time Taken for Procedure:", timeDelayed)

# To print the price to pay for a Procedure
priceForProcedure = data["subThematics"][0]["sub-subThematics"][0]["details"]["price"]
print("Money to Pay for Procedure:", priceForProcedure)

# To print the Documents required for a procedure
listOfDocuments = data["subThematics"][0]["sub-subThematics"][0]["details"]["documents"]
documents = list()
for i in range(len(listOfDocuments)):
    documents.append(str(listOfDocuments[i]["title"]).capitalize())
print("Following documents are required for the specified procedure:")
for i in range(1, len(documents)+1):
    print(f"{i}. {documents[i-1]}.")

for i in range(6):
    print("H")
    # if i == 4:
    #     break
else:
    print("HELLO")
print("world")