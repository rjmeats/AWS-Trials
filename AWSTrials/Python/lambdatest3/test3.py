from bs4 import BeautifulSoup
import requests

def lambda_handler(event, context):

	urlString = event['site']
	try :
		r = requests.get(urlString, timeout=10)
		if r.status_code != 200:
			return {
				'url' : urlString,
				'status' : r.status_code
			}
		else :
			bytes = r.text
	except requests.ConnectionError as e:
		return {
			'url' : urlString,
			'error' : str(e)		
		}

	# bytes = "<html><head><title>My title</title></head><body></body></html>"

	soup = BeautifulSoup(bytes, features="html.parser")
	results = soup.find_all("title")
	if len(results) == 0:
		title = '[No title found]'
	else :
		title = results[0].get_text()

	#print(results)
	#print(title)

	return {
		'url' : urlString,
		'title' : title,
		'status' : r.status_code
	}


if __name__ == "__main__" :
	#print("Running as main")
	param = { "site" : "https://www.bbc.co.uk/" }
	ret = lambda_handler(param, 0)
	print(ret)


import requests

