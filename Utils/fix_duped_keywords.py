import os

from dotenv import load_dotenv

load_dotenv()

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# all_companies = supabase.table('Companies').select('*').execute().data
#
# for company in all_companies:
#     if company['City'] is None:
#         company['City'] = []
#
#     supabase.table('Companies').update(
#         {'City': list(set(company['City']))}
#     ).eq('id', company['id']).execute()

all_posts = supabase.table('Posts').select('*').execute().data

for post in all_posts:
    if post['City'] is None:
        post['City'] = []

    if post['Keywords'] is None:
        post['Keywords'] = []

    supabase.table('Posts').update(
        {'City': list(set(post['City'])),
         'Keywords': list(set(post['Keywords']))}
    ).eq('id', post['id']).execute()
