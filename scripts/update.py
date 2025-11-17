#This module contains all functions to handle updating records in the database

from search import get_ticket_by_id
from supabaseClient import supabase

def update_asset(asset_id,asset_details):
    current_details=supabase.table("devices").select('*').eq('id', asset_id).execute().data[0]
    if asset_details["hostname"]:
        if asset_details["hostname"] != current_details["hostname"]:
            response=supabase.table("devices").update({"hostname":asset_details["hostname"]}).eq('id', asset_id).execute()
    if int(asset_details["type_id"]) != current_details["type_id"]:
        response=supabase.table("devices").update({"type_id":int(asset_details["type_id"])}).eq('id', asset_id).execute()
    if int(asset_details["customer_id"]) != current_details["customer_id"]:
        response=supabase.table("devices").update({"customer_id":int(asset_details["customer_id"])}).eq('id', asset_id).execute()
    if int(asset_details["status_id"]) != current_details["status_id"]:
        response=supabase.table("devices").update({"status_id":int(asset_details["status_id"])}).eq('id', asset_id).execute()
    print(response)
    return

def update_customer(customer_id, customer_details):
    current_details=supabase.table("customers").select('*').eq('id', customer_id).execute().data[0]
    if customer_details["customer_name"]:
        if customer_details["customer_name"] != current_details["customer_name"]:
            response=supabase.table("customers").update({"customer_name":customer_details["customer_name"]}).eq('id', customer_id).execute()
    if int(customer_details["teir"]) != current_details["teir"]:
        response=supabase.table("customers").update({"teir":int(customer_details["teir"])}).eq('id', customer_id).execute()
    return 

def update_user(user_id, user_details):
    current_details=supabase.table("users").select('*').eq("id", user_id).execute().data[0]
    if user_details["username"]:
        if user_details["username"] != current_details["username"]:
            response=supabase.table("users").update({"username":user_details["username"]}).eq('id', user_id).execute()
    if user_details["customer_id"]:
        if int(user_details["customer_id"]) != current_details["customer_id"]:
            response=supabase.table("users").update({"customer_id":int(user_details["customer_id"])}).eq('id', user_id).execute()
    if user_details["auth_level"]:
        if int(user_details["auth_level"]) != current_details["auth_level"]:
            response=supabase.table("users").update({"auth_level":int(user_details["auth_level"])}).eq('id', user_id).execute()
    return

def change_ticket_device(request_dict, ticket_id):
    request_dict=dict(request_dict)
    if not request_dict["device_id"]:
        request_dict["device_id"] = None
    else:
        ticket_customer=supabase.table("user_requests").select("customer_id").eq("id",ticket_id).execute().data[0]
        device_customer=supabase.table("devices").select("customer_id").eq("id", request_dict["device_id"]).execute().data[0]
        if ticket_customer["customer_id"] != device_customer["customer_id"]:
            update_customer=supabase.table("user_requests").update({"customer_id": device_customer["customer_id"]}).eq("id",ticket_id).execute()
    response=supabase.table("user_requests").update({"device_id": request_dict["device_id"]}).eq("id", ticket_id).execute()
    print(response)
    return response.data

def change_ticket_customer(request_dict, ticket_id):
    request_dict=dict(request_dict)
    ticket_details=get_ticket_by_id(ticket_id)
    if ticket_details["device_id"]:
        device_customer=supabase.table("devices").select("customer_id").eq("id", ticket_details["device_id"]).execute().data[0]
        if device_customer["customer_id"] != request_dict["customer_id"]:
            update_customer=supabase.table("user_requests").update({"device_id": None}).eq("id",ticket_id).execute()
    response=supabase.table("user_requests").update({"customer_id": request_dict["customer_id"]}).eq("id", ticket_id).execute()
    print(response)
    return response.data

def change_ticket_user(request_dict, ticket_id):
    request_dict=dict(request_dict)
#    ticket_details=get_ticket_by_id(ticket_id)
#    get_user_details=return_user_by_id(request_dict["user_id"])
#    if ticket_details["device_id"]:
#        device_customer=supabase.table("devices").select("customer_id").eq("id", ticket_details["device_id"]).execute().data[0]
#        if device_customer["customer_id"] != get_user_details["customer_id"]:
#            update_customer=supabase.table("user_requests").update({"device_id": None}).eq("id",ticket_id).execute()
    response=supabase.table("user_requests").update({"user_id": request_dict["user_id"]}).eq("id", ticket_id).execute()
    print(response)
    return response.data

def change_ticket_status(ticket_id, status_id):
    response = supabase.table("user_requests").update({"status_id": status_id}).eq("id", ticket_id).execute()
    return response.data

def reassign_ticket_user(ticket_id, user_id):
    response=supabase.table("user_requests").update({"assigned_team_member_id": user_id}).eq("id", ticket_id).execute()
    return response.data