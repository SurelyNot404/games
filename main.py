import os
from webbrowser import open_new_tab
import sqlite3
from tabulate import tabulate
import requests

conn = sqlite3.connect("games.db")
cursor = conn.cursor()

if not os.path.exists("games.dp"):
    print('banco de dados não encontrado, baixando...')
    URL = "https://dl.dropboxusercontent.com/s/qdxt512zsmxwkku/games.db?dl=0"
    response = requests.get(URL)
    open("games.db", "wb").write(response.content)
    print("bando de dados baixado")


def download(item, file):
    open_new_tab(f"https://archive.org/download/{item}/{file}")

def search():
    game_name = input("nome do jogo: ")

    data = cursor.execute(f'SELECT * FROM games WHERE name LIKE "%{game_name}%"').fetchall()

    if len(data) != 0:
        result = []

        for i in range(len(data)):
            name, game_id, size, item, file_name = data[i]
            result.append([i, name, game_id, size])

        print(tabulate(result, headers=["index","name","game_id","size"]))

        selected = input("\nselecione o jogo: ")
        if len(selected) != 0:
            selected = int(selected)
            if selected > len(result) or selected < 0:
                print('opção invalida')
            download(data[selected][3], data[selected][4])
        else:
            print("nenhum jogo selecionado")

    else:
        print(f"nenhum jogo encontrado com o nome: {game_name}")

if __name__ == "__main__":
    search()
