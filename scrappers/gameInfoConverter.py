# crea un csv nuevo a partir de games.csv

import csv

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
        
