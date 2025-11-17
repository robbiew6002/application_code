# Module to setup connection and client to supabase cloud database. Module exports client to be used in other files.

import os
from supabase import create_client, Client
url: str = "https://iuqniwkjibuhxkovuymy.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cW5pd2tqaWJ1aHhrb3Z1eW15Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzMDk0NTQsImV4cCI6MjA3ODg4NTQ1NH0.sUaav2Jk8jeghhZsFY5senFRufYje4VhH9ddNFdAQvE"
supabase: Client = create_client(url, key)
