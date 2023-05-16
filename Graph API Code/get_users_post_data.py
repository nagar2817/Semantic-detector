# 'https://graph.facebook.com/v12.0/{ig-user-id}?fields=business_discovery.username({ig-username}){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{id,caption,like_count,comments_count,timestamp,username,media_product_type,media_type,owner,permalink,media_url,children{media_url}}}&access_token={access-token}';
from defines import getCreds, makeApiCall
import csv,re,requests
import pandas as pd

def getUserMedia( params, pagingUrl = '' ) :
	""" Get info on a users account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields=business_discovery.username({ig-username}){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{id,caption,like_count,comments_count,timestamp,username,media_product_type,media_type,owner,permalink,media_url,children{media_url}}}&access_token={access-token}

	Returns:
		object: data from the endpoint

	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'business_discovery.username(' + params['ig_username'] + '){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{id,caption,like_count,comments_count,timestamp,username,media_product_type,media_type,owner,permalink,media_url,children{media_url}}}' # string of fields to get back with the request for the account
	endpointParams['access_token'] = params['access_token'] # access token

	if(''== pagingUrl):
		url = params['endpoint_base'] + params['instagram_account_id'] # endpoint url
	else:
		url = pagingUrl

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

params = getCreds() # get creds
params['debug'] = 'yes' # set debug
response = getUserMedia( params ) # hit the api for some data!

# params['debug'] = 'yes' # set debug
# response = getAccountInfo( params, response['json_data']['paging']['next'] ) 

# print ("\n---- ACCOUNT INFO -----\n") # display latest post info
# no_of_posts = response['json_data']['business_discovery']['media_count']

media_overall = response['json_data']['business_discovery']
ig_username = media_overall['username']
posts = media_overall['media']['data'] 

# after = media_overall['media']['paging'].get("cursors").get("after")
# res_1 = getUserMedia(params,after) 
# media_overall = res_1['json_data']['business_discovery']
# ig_username = media_overall['username']
# posts = media_overall['media']['data'] 
# print(response)
# print(media_overall['id'])

data = {
    'id': [],
    'username':[],
    'caption': [],
    'like_count': [],
    'comments_count':[],
    'hashtags':[],
    'tags':[],
    'timestamp':[],
    'media_product_type':[],
	'media_type':[] 
}
# params['access_token']
# def GetTaggedUsers(post,params, pagingUrl = ''):
# 	endpointParams = dict() # parameter to send to the endpoint
# 	endpointParams['fields'] = 'mentions' # string of fields to get back with the request for the account
# 	endpointParams['access_token'] = params['access_token'] # access token

# 	# url = f"https://graph.instagram.com/{post['id']}?fields=mentions&access_token={params['access_token']}"
# 	# response = requests.get(url)
# 	# res_1 = response.json()
# 	if(''== pagingUrl):
# 		url = params['endpoint_base']  + post['id'] # endpoint url
# 	else:
# 		url = pagingUrl

# 	return makeApiCall( url, endpointParams, params['debug'] ) 

# # Extract tagged users from the 'mentions' field
	# mentions = res_1.get('mentions', [])
	# tagged_users = [mention['username'] for mention in mentions]

	# print(tagged_users)
for post in posts:
	# res_001  = GetTaggedUsers(post,params)
	# print(res_001)

	data['id'].append(post['id'])
	data['username'].append(post['username'])
	post['caption'] = post['caption'].replace('\n', ' ')
	# print(post['caption'])
	data['caption'].append(post['caption'])
	data['like_count'].append(post['like_count'])
	data['comments_count'].append(post['comments_count'])
	caption = post['caption']
	hashtags = re.findall(r'#\w+', caption)
	data['hashtags'].append(hashtags)
	tags_in_caption = re.findall(r'@\w+', caption)
	data['tags'].append(tags_in_caption)
	data['timestamp'].append(post['timestamp'])
	data['media_product_type'].append(post['media_product_type'])
	data['media_type'].append(post['media_type'])




df = pd.DataFrame(data)
df.to_csv('mrunu_3.csv', index=False) 