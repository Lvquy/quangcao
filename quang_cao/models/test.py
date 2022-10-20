import requests
import urllib.parse as p
import num2text


print(num2text.docso(333))
# get the API KEY here: https://developers.google.com/custom-search/v1/overview
# API_KEY = "AIzaSyCEoVh9VrtlEHpGlt-kOHuRxqv--K8aD64"
# API_KEY = "AIzaSyCpHv1izURmm3nYjprLhgtDZLzFVHGyLJA"
# get your Search Engine ID on your CSE control panel
# SEARCH_ENGINE_ID = "92e17de76de7847ad"
# SEARCH_ENGINE_ID = "85a0b22e4a83b497c"
# the search query you want
# query = "python"
# using the first page
# page = 1
# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
# start = (page - 1) * 10 + 1
# url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
# make the API request
# data = requests.get(url).json()
# print(data)
# get the result items
# search_items = data.get("items")
# print(search_items)
# if search_items:
#     for i, search_item in enumerate(search_items, start=1):
#         try:
#             long_description = search_item["pagemap"]["metatags"][0]["og:description"]
#         except KeyError:
#             long_description = "N/A"
        # get the page title
        # title = search_item.get("title")
        # page snippet
        # snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        # html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        # link = search_item.get("link")
        # print the results
        # print("="*10, f"Result #{i+start-1}", "="*10)
        # print("Title:", title)
        # print("Description:", snippet)
        # print("Long description:", long_description)
        # print("URL:", link, "\n")