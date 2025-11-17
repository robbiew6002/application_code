#This module contains all scripts for authentication on the application.
import os
from supabaseClient import supabase
from flask import session

def check_credentials(user_details):
    response = (
    supabase.table("users")
    .select("*")
    .execute()
    )
    for user in response.data:
        if user['username'] == user_details['username'] and user['password'] == user_details['password']:
            print(user)
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['customer_id'] = user['customer_id']
            session['auth_level'] = user['auth_level']
            return
    return
    