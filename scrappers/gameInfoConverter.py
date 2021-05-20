# a partir de los juegos extraidos, crea una tabla para indicar a que genero y plataforma pertenece cada juego

import csv, requests

def get_platforms_request(page_number):
    """Genera una peticion para un genero especifico
        Atributos
        ------
        genre : genero del cual quiero obtener juegos
        page_number : cada peticion trae 40 juegos. Para obtener 40 mas se aumenta el nro de pagina
    """
    link = "https://rawg.io/api/platforms?&page={}&page_size=40".format(page_number)
    link = link+"&key=7a07bcd210364441a3425a8076375615"
    return link


#extraigo plataformas de rawg.io
platforms = []
page = 1
while True:
    resp = requests.get(get_platforms_request(page))
    if(resp.status_code != 200):
        break
    
    results = resp.json()["results"]
    for res in results:
        print(res["slug"])
        platforms.append(res["slug"])
    nxt = resp.json()["next"]
    page += 1
    if(nxt=="null"):
        break
    

#guardo los generos en una lista
genres = open("/home/rulo/borrar/jQ/py/genres.txt","r")
genre_list = []
for genre_item in genres:
    genre_list.append(genre_item.replace('\n',''))
genres.close()

with open('game_genres.csv',mode='w') as num_games:
    games_writer = csv.writer(num_games, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    with open('scrappers/games.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                games_writer.writerow(["title"] + genre_list)
                line_count += 1
                continue
            
            gameGenres = row[2].split('|')
            nRow = [] #lista de los generos a los que el juego pertenece(1) y no pertenece(0)
            nRow.append(row[1])
            for genre in genre_list:
                if genre in gameGenres:
                    nRow.append(1)
                else:
                    nRow.append(0)
            
            games_writer.writerow(nRow)
        
with open('game_platforms.csv',mode='w') as num_platforms:
    platforms_writer = csv.writer(num_platforms, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    with open('scrappers/games.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                platforms_writer.writerow(["title"] + platforms)
                line_count += 1
                continue
            
            gamePlatforms = row[3].split('|')
            nRow = [] #lista de los generos a los que el juego pertenece(1) y no pertenece(0)
            nRow.append(row[1])
            for plat in platforms:
                if plat in gamePlatforms:
                    nRow.append(1)
                else:
                    nRow.append(0)
            
            platforms_writer.writerow(nRow)
        
