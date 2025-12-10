# Automated testing module to test security features
# This module tests for correct use of authentication, authorization and password hashing
# to ensure adhearance to OWASP broken authentication security

import pytest
from flask import session
import os
from supabaseClient import supabase

#Test redirect from homepage if session is unauthenticated
def test_redirect(client):
    response=client.get("/home", follow_redirects=True)
    assert response.request.path == "/"

#Test incorrect username and password and cannot access home page
def test_incorrect_auth(client):
    with client:
        client.post("/login", data={"username": "test", "password": "test"})
        response=client.get("/home", follow_redirects=True)
        assert not session.get('logged_in') and response.request.path == "/"

#Test correct username and password is able to log in and is redirected to home page
def test_correct_auth(client):
    with client:
        response=client.post("/login", data={"username": os.environ["USER"], "password":os.environ["PASSWORD"]}, follow_redirects=True)
        assert session.get("logged_in") == True and response.request.path == "/home"

#Test passwords are hashed and stored in hashed format
def test_password_hashing(client,bcrypt):
    with client:
        client.post("/login", data={"username": os.environ["USER"], "password":os.environ["PASSWORD"]}, follow_redirects=True)
        client.post("/users/create", data={"username": "test@ampito.com", "password": "test", "customer_id": 2, "auth_level": 3})
        user_details=supabase.table("users").select("*").eq('username', "test@ampito.com").execute()
        print(bcrypt.generate_password_hash(user_details.data[0]["password"]).decode("utf-8"))
        assert bcrypt.check_password_hash(user_details.data[0]["password"], "test")
        supabase.table("users").delete().eq("id", user_details.data[0]["id"]).execute()

#Test user auth access is correct and user cannot access other customer data or data they shouldn't access
def test_auth_levels(client):
    with client:
        client.post("/login", data={"username": os.environ["CONNELLS_USER"], "password": os.environ["CONNELLS_PASSWORD"]}, follow_redirects=True)
        print(session)
        device_response=client.get("/assets/17", follow_redirects=True)
        user_response=client.get("/users", follow_redirects=True)
        assert device_response.request.path and user_response.request.path == "/home"