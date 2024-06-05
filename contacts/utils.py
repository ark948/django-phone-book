from contacts.models import Contact
from icecream import ic
ic.configureOutput(includeContext=True)

def make_new_contact_entry(contact_object: dict):
    result = {}
    contact = Contact()
    try:
        contact.title = contact_object["title"]
        contact.first_name = contact_object["first_name"]
        contact.last_name = contact_object["last_name"]
        contact.phone_number = contact_object["phone_number"]
        contact.email = contact_object["email"]
        contact.address = contact_object["address"]
        contact.owner = contact_object["owner"]
    except Exception as adding_dict_items_to_contact:
        ic(adding_dict_items_to_contact)
        result["status"] = False
    try:
        contact.save()
        result["status"] = True
        result["message"] = "Successfully added new contact"
    except Exception as error:
        result["status"] = False
        result["message"] = error
    return result