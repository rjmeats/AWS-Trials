from bs4 import BeautifulSoup

def lambda_handler(event, context):

	urlString = event['site']

	bytes = "<html><head><title>My title</title></head><body></body></html>"

	soup = BeautifulSoup(bytes, features="html.parser")
	results = soup.find_all("title")
	title = results[0].get_text()

	#print(results)
	#print(title)

	return {
		'url' : urlString,
		'title' : title
	}


if __name__ == "__main__" :
	#print("Running as main")
	param = { "site" : "https://x.x" }
	ret = lambda_handler(param, 0)
	print(ret)

