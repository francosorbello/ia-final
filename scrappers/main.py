import requests

resp = requests.get("https://rawg.io/api/genres?page_size=50");
jResp = resp.json()

results = jResp["results"]
for item in results:
    print("{}".format(item["slug"]))

#extraer reviews de un user
# resp = requests.get("https://rawg.io/api/users/ibarin/reviews?page_size=50&key=7a07bcd210364441a3425a8076375615");
# jResp = resp.json()

# results = jResp["results"]
# for item in results:
#     print("{}\n{}".format(item["game"]["name"],item["rating"]))
#     print("#--#")