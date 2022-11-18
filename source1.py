from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import json

data = dict()
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
    for i in range(len(data['data'])):
        proc_name = data["data"][i]["subThematics"][0]["govprocedure"][0]["title"]
        all_procedure_names.append(proc_name)
    
    # Finding the only one string with maximum matching ratio and 
    # its matching ratio all available strings
    sentence, matching_ratio = process.extractOne(procedure, all_procedure_names, scorer=fuzz.token_sort_ratio)
    
    if matching_ratio >= 30:
        return sentence
    else:
        return None


print(get_matched_procedure("Medical certificate for driving license"))
print(get_matched_procedure("passport"))

# str_list = ['Joe Biden', 'Joseph Biden', 'Joseph R Biden']

# match_ratios = process.extract('joe r biden', str_list, scorer=fuzz.token_sort_ratio)
# print(match_ratios)

# best_match = process.extractOne('', str_list, scorer=fuzz.token_sort_ratio)
# print(best_match)

