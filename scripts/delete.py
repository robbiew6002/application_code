#This module contains all functions to handle deleting records from the database
from supabaseClient import supabase

def delete_asset_by_id (asset_id):
    response = supabase.table("devices").delete().eq("id", asset_id).execute()

def delete_customer_by_id(customer_id):
    response = supabase.table("customers").delete().eq("id", customer_id).execute()

def delete_user_by_id(user_id):
    response = supabase.table("users").delete().eq("id", user_id).execute()

    
def delete_ticket_by_id(ticket_id):
    response = supabase.table("user_requests").delete().eq("id", ticket_id).execute()

def delete_note_by_id(note_id):
    resposnse = supabase.table("request_notes").delete().eq("id", note_id).execute()