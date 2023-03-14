from telnetlib import theNULL
from urllib import response
from requests_oauthlib import OAuth1Session
import json
import requests
from datetime import datetime, timedelta, timezone



#set API Keys
with open("twitterAPI.json") as twitterapi:
    keys = json.load(twitterapi)

APIKey = keys.get("APIKey")
APIKeySecret = keys.get("APIKeySecret")
BearerToken = keys.get("BearerToken")
AccessToken = keys.get ("AccessToken")
AccessTokenSecret = keys.get("AccessTokenSecret")

#find start_tiem
today = datetime.now(timezone.utc)
onehourago = today.__add__(timedelta(hours=-1))

#search API
search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = {'query': 'braidsmaids -is:retweet', 'start_time': onehourago.isoformat(), 'tweet.fields': 'author_id,reply_settings', 'expansions': 'author_id', 'user.fields': 'location,name,username'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BearerToken}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


json_response = connect_to_endpoint(search_url, query_params)
results = json.loads(json.dumps(json_response, indent=4, sort_keys=True))

if 'data' in results:
    results_data = results['data']
    print("RESULTS DATA: ",results_data)

if 'includes' in results:
    results_users = results['includes']['users']
    print("RESULTS USERS: ", results_users)


#function to send replies
def send_reply(username, tweet_id):
    payload = {"text": "@" + username + " bridesmaids*", "reply": {"in_reply_to_tweet_id": tweet_id}}
    
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(APIKey, client_secret=APIKeySecret)

    # Make the request
    oauth = OAuth1Session(
        APIKey,
        client_secret=APIKeySecret,
        resource_owner_key=AccessToken,
        resource_owner_secret=AccessTokenSecret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )


    # if response.status_code != 201:
    #     raise Exception(
    #         "Request returned an error: {} {}".format(response.status_code, response.text)
    #     )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    # json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


# if __name__ == '__main__':
#Loop through search results and tweet replies

# for data in results_data:
#     if data['reply_settings'] == 'everyone':
#         #find the username of the tweet
#         for user in results_users:
#             if user['id'] == data['author_id']:                       
#                 #send a reply
#                 send_reply(user['username'], data['id'])
#                 break