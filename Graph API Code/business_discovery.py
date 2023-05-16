from defines import getCreds, makeApiCall

def getAccountInfo( params ) :
	""" Get info on a users account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields=business_discovery.username({ig-username}){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}&access_token={access-token}

	Returns:
		object: data from the endpoint

	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'business_discovery.username(' + params['ig_username'] + '){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}' # string of fields to get back with the request for the account
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + params['instagram_account_id'] # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

params = getCreds() # get creds
params['debug'] = 'no' # set debug
response = getAccountInfo( params ) # hit the api for some data!

print ("\n---- ACCOUNT INFO -----\n") # display latest post info
print (f"username: {response['json_data']['business_discovery']['username']}") # label
print (f"website: {response['json_data']['business_discovery']['website']}") # label
print (f"number of posts: {response['json_data']['business_discovery']['media_count']}") # label
print (f"followers: {response['json_data']['business_discovery']['followers_count']}") # label
print (f"following: {response['json_data']['business_discovery']['follows_count']}") # label
# print (f"profile picture url:{response['json_data']['business_discovery']['profile_picture_url']}") # label
print (f"biography:\n {response['json_data']['business_discovery']['biography']}") # label