"""
Para una lista de juegos, busca reviews de dichos juegos en una serie de users preseleccionados
"""

import requests, time, csv

class GameReview:
    def __init__(self,name,rating):
        self.name = name
        self.rating = rating 

class User:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.reviews = []
    
    def create_review(self,name,rating):
        self.reviews.append(GameReview(name,rating))

    def add_review(self,review : GameReview):
        self.reviews.append(review)

def user_review_request(user,page_number):
    """Genera una peticion de las reviews de un user especifico
        Atributos
        ------
        user : user del cual obtengo informacion
        page_number : cada peticion trae 40 juegos. Para obtener 40 mas se aumenta el nro de pagina
    """
    link = "https://rawg.io/api/users/{}/reviews?&page={}&page_size=40".format(user,page_number)
    link = link+"&key=7a07bcd210364441a3425a8076375615"
    return link

initTime = time.time()
games = []
#extraigo los juegos generados por gameScrapper
with open("/home/rulo/Documentos/UNCU-LINUX/ia/final/repo/ia-final/scrappers/games.csv") as gameFile:
    game_reader = csv.reader(gameFile,delimiter=',')
    x = 0
    for row in game_reader:
        if x==0:
            x+=1
            continue

        games.append(row[1])

#obtengo los users de un archivo
users = open("/home/rulo/Documentos/UNCU-LINUX/ia/final/repo/ia-final/scrappers/users.txt","r")
userCount = 0
userId = 1
userList = []
for user_item in users:
    userCount += 1
    #creo un user
    user_name = user_item.replace('\n','')
    user = User(userId,user_name)
    print("Usuario: "+user_name)

    page = 1
    cached_reviews = []
    lastResp = ""
    #para cada user, busco entre sus reviews si ha puntuado los juegos seleccionados por el otro scrapper
    for game in games:
        revCount = 0
        print("Buscando reviews de: "+game)
        gameFound = False
        while True:
            #cacheo reviews cuando sea necesaro
            if(lastResp != None):
                resp = requests.get(user_review_request(user_name,page))
                if(resp.status_code != 200):
                    break
                jResp = resp.json()
                lastResp = jResp["next"]
                for review in jResp["results"]:
                    cached_reviews.append(GameReview(review["game"]["slug"],review["rating"]))

            #primero busco entre las reviews cacheadas
            for review in cached_reviews:
                if review.name == game:
                    user.add_review(review)
                    gameFound = True
                    break
                
            if gameFound:
                break

            #si no la encuentro cacheo mas reviews
            page += 1
            revCount += 1
            #si ya vi todas las reviews y no quedan mas por cachear, no hay review para el juego
            if lastResp == None and len(cached_reviews) == revCount:
                break
    cached_reviews.clear()
    userList.append(user)
    userId += 1
users.close()
print('Para {} users tardó {} segundos'.format(userCount,time.time()-initTime))

#escribo los resultados en un archivo csv
with open('ratings.csv',mode='w') as ratings_file:
    rf_writer = csv.writer(ratings_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    rf_writer.writerow(['userId','gameId','rating'])
    for user in userList:
        for review in user.reviews:
            nRev = []
            nRev.append(user.id)
            nRev.append(review.name)
            nRev.append(review.rating)
            rf_writer.writerow(nRev)
