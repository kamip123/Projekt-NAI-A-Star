# import
from configparser import ConfigParser  # ustawienia
from PIL import Image  # obsluga png
import numpy  # obsluga array
from heapq import heappush, heappop  # stos do implementacji algorytmu
import math  # math do implementacji algorytmu

numpy.set_printoptions(threshold=numpy.nan)  # python wypisuje pelny array zamiast wersji skroconej

# plik config.ini
config = ConfigParser()

config.read('config.ini')
input = config.get('Config', 'input')
start = config.get('Config', 'start')
finish = config.get('Config', 'finish')
output = config.get('Config', 'output')
outputt = config.get('Config', 'outputt')

# split string'a
start = start.split()
finish = finish.split()
# zamiana kolejnych elementow listy na inty
start[0] = int(start[0])
start[1] = int(start[1])
finish[0] = int(finish[0])
finish[1] = int(finish[1])

print('Plik graficzny z mapą:', input)
print('Punkt startowy:', start)
print('Punkt koncowy:', finish)
print('Plik graficzny z mapą po znalezieniu sciezki:', output)
print('Plik tekstowy z punktami:', outputt)

# otworzenie pliku png i konwersja najpierw na array

img = Image.open(input).convert('RGBA')
arr3 = numpy.array(img)

# przypisanie do nowej tablicy tylko z przeszkodami "1" i pustymi polami "0"
tablicaLabiryntu = numpy.array([[0 for x in range(100)] for y in range(100)])

# wypelnienie
for i in range(0, 100):
    for j in range(0, 100):
        if numpy.array_equal(arr3[i][j], (255, 255, 255, 255)):
            tablicaLabiryntu[i][j] = 1


# metoda heurystyczna - Euclidian Distance
def heuristic(a, b):
    return math.sqrt((b[0] * a[0]) + (b[1] * a[1]))


def astar(tablicaLabiryntu, start, goal):
    neighbors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    # bez skosow
    # neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    closed_set = set()  # zbior wierzcholkow odwiedzonych
    openSet = []  # zbior nie odwiedzonych


    came_from = {}  # z kad przybyl - nabardziej efektywny poprzedni krok
    gScore = {start: 0}  # koszt start - aktualny punkt
    fscore = {start: heuristic(start, goal)}  # koszt start - koniec przez aktualny punkt

    # wrzucenie na stos pierwszego elementu
    heappush(openSet, (fscore[start], start))

    while openSet:
        # sciagamy z stosu aktualny element
        current = heappop(openSet)[1]
        # sprawdzamy czy koniec i wypelniamy liste data punktami
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        #dodajemy do odwiedzonych
        closed_set.add(current)
        # dla wszystkich sasiednich pol
        # i - pierwsza wartosc, j - druga wartosc
        for i, j in neighbors:
            #sprawdzamy dla pierwszego itd
            neighbor = current[0] + i, current[1] + j
            #tentative_gScore koszt aktualnej sciezki + sasiad
            tentative_gScore = gScore[current] + heuristic(current, neighbor)
            # sprawdza czy nie wychodzi poza przedzial tablicy
            if 0 <= neighbor[0] < tablicaLabiryntu.shape[0]:
                if 0 <= neighbor[1] < tablicaLabiryntu.shape[1]:
                    if tablicaLabiryntu[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # sciany y
                    continue
            else:
                # sciany x
                continue
            #droga nie jest najlepsza wiec kontynuuj
            if neighbor in closed_set and tentative_gScore >= gScore.get(neighbor, 0):
                continue
            #droga jest najlepsza wiec ja zapisz na stosie
            if tentative_gScore < gScore.get(neighbor, 0) or neighbor not in [i[1] for i in openSet]:
                #zmienia dla kogo poszukujemy - sasiad staje sie aktualnym wezlem
                came_from[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fscore[neighbor] = tentative_gScore + heuristic(neighbor, goal)
                heappush(openSet, (fscore[neighbor], neighbor))

    return False

# wywolanie funkcji
# print(astar(tablicaLabiryntu, (start[0], start[1]), (finish[0], finish[1])))
wierzcholki = astar(tablicaLabiryntu, (start[0], start[1]), (finish[0], finish[1]))


result = open("result.txt", "w")
# narysowanie sciezki + wpisanie do pliku
for x in range(len(wierzcholki)):
    arr3[wierzcholki[x][0]][wierzcholki[x][1]] = (255, 0, 0, 255)
    temp = (str(x) + ': ' + str(wierzcholki[x][0])+ ', ' + str(wierzcholki[x][1]) + '\n')
    result.write(temp)

result.close()

arr3[finish[0]][finish[1]] = (0, 255, 0, 255)
arr3[start[0]][start[1]] = (255, 255, 0, 255)
# wypisanie ilosci krokow
print(len(wierzcholki))

# konwersja na image, zapisanie, pokazanie
img2 = Image.fromarray(arr3, 'RGBA')
img2.save(output)
img2.show()
