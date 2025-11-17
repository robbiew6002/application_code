#This module contains all functions to handle creating new records in the database

from supabaseClient import supabase
from flask import session

def add_asset_to_database(asset_dict):
    response=supabase.table("devices").insert(asset_dict).execute()
    print(response.data)
    return response.data[0]

def add_customer_to_database(customer_dict):
    response=supabase.table("customers").insert(customer_dict).execute()
    print(response.data)
    return response.data[0]

def add_user_to_database(user_dict):
    response=supabase.table("users").insert(user_dict).execute()
    print(response.data)
    return response.data[0]

def create_request(request_dict):
    final_request=dict(request_dict)
    final_request["user_id"] = session["user_id"]
    final_request["status_id"] = 1
    if not final_request["device_id"]:
        final_request["device_id"] = None
    if session["auth_level"] != 1 and session["auth_level"] != 2:
        final_request["customer_id"] = session["customer_id"]
    response=supabase.table("user_requests").insert(final_request).execute()
    add_note_to_ticket({"created_by": session["user_id"], "body": "Ticket Created"},response.data[0]["id"])
    return response.data[0]

def add_note_to_ticket(request_dict, ticket_id):
    print(request_dict)
    final_request=dict(request_dict)
    final_request["created_by"] = session["user_id"]
    final_request["request_id"] = ticket_id
    response=supabase.table("request_notes").insert(final_request).execute()
    return response.data[0]

def post_error_form(error_form):
    print("function triggered")
    print(error_form)
    print(session)
    final_dict={}
    final_dict["user_id"] = session["user_id"]
    final_dict["status_id"] = 1
    final_dict["customer_id"] = 2
    final_dict["device_id"] = None
    final_dict["summary"] = f"A site error has occured."
    bad_url=str(error_form["failed_url"])
    bad_method=str(error_form["failed_method"])
    final_dict["description"]=error_form["body"]
    final_dict["description"] += f" This request occured on url {bad_url} on a {bad_method} request."
    print("")
    print(final_dict)
    response=supabase.table("user_requests").insert(final_dict).execute()
    print(response)
    return response.data