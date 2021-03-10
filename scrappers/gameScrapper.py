"""
Para cada genero, obtiene un numero de juegos y los guarda en una lista
"""
import requests, csv, time


class Game:
    def __init__(self,title,id,genres,platforms):
        """
        Constructor de la clase
        Atributos
        ------
        title : titulo del juego
        id : id del juego establecido por la api
        genres : lista de generos a los que pertenece el juego
        plaforms : lista de plataformas en las que ha sido publicado
        """
        self.title = title
        self.id = id
        self.genres = genres
        self.platforms = platforms

    def as_array(self):
        """Transforma el objeto en una lista facil de guardar en un archivo"""
        gameArray = []
        gameArray.append(self.id)
        gameArray.append(self.title)


class GameList:
    def __init__(self) -> None:
        self.games = []

    def add_game(self,game:Game):
        self.games.append(game)

    def contains(self, gameName):
        for game in self.games:
            if(game.title == gameName):
                return True
        
        return False
    
    def as_array(self):
        return self.games

def list_to_string(oldList):
        """Transforma una lista de items en un string"""
        strList = ""
        for item in oldList:
            strList += item
            strList += '|' #separador de items

        strList = strList[:-1] #elimino el ultimo separador
        return strList

def get_genre_request(genre,page_number):
    """Genera una peticion para un genero especifico
        Atributos
        ------
        genre : genero del cual quiero obtener juegos
        page_number : cada peticion trae 40 juegos. Para obtener 40 mas se aumenta el nro de pagina
    """
    link = "https://rawg.io/api/games?genres={}&page={}&page_size=40".format(genre,page_number)
    link = link+"&key=7a07bcd210364441a3425a8076375615"
    return link

def get_clean_genres(genres):
    """
    Transforma los generos de un juego a una lista de solo los nombres
    Elimina informacion necesaria, como el id y la fecha de creacion
    """
    nGenres = []
    for genre in genres:
        nGenres.append(genre["slug"])
    return nGenres

def get_clean_platforms(platforms):
    """
    Transforma las plataformas en las que esta un juego a una lista de solo los nombres
    Elimina informacion necesaria, como el id y la fecha de creacion
    """
    nPlatforms = []
    for plat in platforms:
        nPlatforms.append(plat["platform"]["slug"])
    return nPlatforms

initTime = time.time()

gameQuant = 5 #cantidad de juegos que extraigo por genero
gamesList = GameList()

#busco gameQuant juegos para cada genero que tengo guardado en un archivo
genres = open("/home/rulo/borrar/jQ/py/genres.txt","r")
genreCount = 0
for genre_item in genres:
    genreCount+=1
    genre = genre_item.replace('\n','')
    page = 1
    currentGameQuant = 0
    while True:
        resp = requests.get(get_genre_request(genre,page))
        if(resp.status_code != 200 or currentGameQuant == gameQuant):
            break
        games = resp.json()["results"]
        for gm in games:
            if not ( gamesList.contains( gm["slug"] ) ):
                gamesList.add_game(
                    Game(
                        gm["slug"],gm["id"],
                        get_clean_genres(gm["genres"]),
                        get_clean_platforms(gm["platforms"])
                        )
                    )
                currentGameQuant += 1
            
            if(currentGameQuant == gameQuant):
                break
        
        page = page+1
genres.close()
print('Para {} juegos tardó {} segundos'.format(gameQuant*genreCount,time.time()-initTime))

#paso la info obtenida a un archivo csv
with open('games.csv', mode='w') as games_file:
    gf_writer = csv.writer(games_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    gf_writer.writerow(['gameId','title','genres','platforms'])
    for game in gamesList.as_array():
        nGame = []
        nGame.append(game.id)
        nGame.append(game.title)
        nGame.append(list_to_string(game.genres))
        nGame.append(list_to_string(game.platforms))
        gf_writer.writerow(nGame)
games_file.close()