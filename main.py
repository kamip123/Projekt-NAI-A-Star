# import
from configparser import ConfigParser  # ustawienia
from PIL import Image  # obsluga png
import numpy  # obsluga array
from heapq import heappush, heappop  # stos do implementacji algorytmu
import math  # math do implementacji algorytmu
import tkinter as tk # interfejs
import time # liczenie czasu
from PIL import ImageTk # umożliwia pokazywanie obrazow w interfejsie

#Potrzebne do testow
#numpy.set_printoptions(threshold=numpy.nan)  # python wypisuje pelny array zamiast wersji skroconej

# pobiera dane
def getValues():
    # plik config.ini
    config = ConfigParser()

    config.read('config.ini')
    global inputPNG
    global start
    global finish
    global output
    global outputt
    inputPNG = config.get('Config', 'input')
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

    #print('Plik graficzny z mapą:', inputPNG)
    #print('Punkt startowy:', start)
    #print('Punkt koncowy:', finish)
    #print('Plik graficzny z mapą po znalezieniu sciezki:', output)
    #print('Plik tekstowy z punktami:', outputt)


# edycja obrazow + konwersja na matrix + algorytm
def imageThings():
    # otworzenie pliku png i konwersja najpierw na array
    img = Image.open(inputPNG).convert('RGBA')
    arr3 = numpy.array(img)

    # przypisanie do nowej tablicy tylko z przeszkodami "1" i pustymi polami "0"
    tablicaLabiryntu = numpy.array([[0 for x in range(100)] for y in range(100)])

    # wypelnienie
    for i in range(0, 100):
        for j in range(0, 100):
            if numpy.array_equal(arr3[i][j], (255, 255, 255, 255)):
                tablicaLabiryntu[i][j] = 1


    # wywolanie funkcji
    # print(astar(tablicaLabiryntu, (start[0], start[1]), (finish[0], finish[1])))
    start_time = time.time()
    global wierzcholki
    global elapsed_time
    wierzcholki = astar(tablicaLabiryntu, (start[0], start[1]), (finish[0], finish[1]))
    elapsed_time = time.time() - start_time

    result = open(outputt, "w")
    # narysowanie sciezki + wpisanie do pliku
    for x in range(len(wierzcholki)):
        arr3[wierzcholki[x][0]][wierzcholki[x][1]] = (255, 0, 0, 255)
        temp = (str(x) + ': ' + str(wierzcholki[x][0]) + ', ' + str(wierzcholki[x][1]) + '\n')
        result.write(temp)

    result.close()

    arr3[finish[0]][finish[1]] = (0, 255, 0, 255)
    arr3[start[0]][start[1]] = (255, 255, 0, 255)
    # wypisanie ilosci krokow
    #print(len(wierzcholki))

    # konwersja na image, zapisanie, pokazanie
    img2 = Image.fromarray(arr3, 'RGBA')
    img2.save(output)
    #img2.show()


# przycisk inicjujacy program - imageThings + dodatkowe informacje
def uruchomProgram():
    imageThings()

    createImage(output)

    routelengthint = str(len(wierzcholki))
    routelength = "Dlugość ścieżki: " + routelengthint
    label = tk.Label(window, text=routelength, font=("Helvetica", 15))
    label.grid(column=0, row=3)

    elapsedtime = math.floor(elapsed_time*100)/100
    elapsedtime = str(elapsedtime)
    elapsedtimestring = "Czas dzialania algorytmu: " + elapsedtime + " sekund"
    label = tk.Label(window, text=elapsedtimestring, font=("Helvetica", 15))
    label.grid(column=0, row=4)


# init interfejsu
def initInterface():
    global window
    window = tk.Tk()
    createWindow()
    initializeWindow()


# stworz interfejs
def createWindow():
    label = tk.Label(window, text="Projekt NAI - A* + interfejs graficzny", font=("Helvetica", 20))
    label.grid(column=0, row=0)

    button = tk.Button(window, text="Uruchom program", command=uruchomProgram, fg="red")
    button.grid(column=1, row=1)

    buttonZmiany = tk.Button(window, text="Zatwierdz zmiany", command=zmianyInput, fg="red")
    buttonZmiany.grid(column=2, row=7)

    buttonZmiany = tk.Button(window, text="Resetuj", command=getValuesAgain, fg="red")
    buttonZmiany.grid(column=3, row=7)

    label = tk.Label(window, text="Długość ścieżki: ", font=("Helvetica", 15))
    label.grid(column=0, row=3)

    label = tk.Label(window, text="Czas dzialania algorytmu: ", font=("Helvetica", 15))
    label.grid(column=0, row=4)

    global entryInputPNG
    global entryStart
    global entryStartt
    global entryFinish
    global entryFinishh
    global entryOutput
    global entryOutputt

    entryInputPNG = tk.Entry(window)
    entryStart = tk.Entry(window)
    entryStartt = tk.Entry(window)
    entryFinish = tk.Entry(window)
    entryFinishh = tk.Entry(window)
    entryOutput = tk.Entry(window)
    entryOutputt = tk.Entry(window)

    entryInputPNGL = tk.Label(window, text="Plik z labiryntem")
    entryStartL = tk.Label(window, text="Poczatek: x, y")
    entryFinishL = tk.Label(window, text="Koniec: x, y")
    entryOutputL = tk.Label(window, text="Plik z labiryntem i sciezka")
    entryOutputtL = tk.Label(window, text="Plik z koordynatami")

    entryInputPNG.insert(tk.END, inputPNG)
    entryStart.insert(tk.END, start[1])
    entryStartt.insert(tk.END, start[0])
    entryFinish.insert(tk.END, finish[1])
    entryFinishh.insert(tk.END, finish[0])
    entryOutput.insert(tk.END, output)
    entryOutputt.insert(tk.END, outputt)

    entryInputPNGL.grid(column=1, row=2)
    entryStartL.grid(column=1, row=3)
    entryFinishL.grid(column=1, row=4)
    entryOutputL.grid(column=1, row=5)
    entryOutputtL.grid(column=1, row=6)

    entryInputPNG.grid(column=2, row=2)
    entryStart.grid(column=2, row=3)
    entryStartt.grid(column=3, row=3)
    entryFinish.grid(column=2, row=4)
    entryFinishh.grid(column=3, row=4)
    entryOutput.grid(column=2, row=5)
    entryOutputt.grid(column=2, row=6)
    createImage(inputPNG)


# pokaz interfejs
def initializeWindow():
    window.mainloop()


# stworz obraz do wyswietlenia
def createImage(inputPNG):
    canvas = tk.Canvas(window, width=300, height=300)
    imgToScale = Image.open(inputPNG).convert('RGBA')
    imgToScale = imgToScale.resize((300, 300))
    labirynt = ImageTk.PhotoImage(imgToScale)
    canvas.image = labirynt
    canvas.grid(column=0, row=1)
    canvas.create_image(0, 0, image=labirynt, anchor="nw")


# aktualizuj pola
def zmianyInput():
        global start
        global finish
        global output
        global outputt
        global inputPNG

        start[1] = int(entryStart.get())
        start[0] = int(entryStartt.get())
        finish[1] = int(entryFinish.get())
        finish[0] = int(entryFinishh.get())
        output = entryOutput.get()
        outputt = entryOutputt.get()
        inputPNG = entryInputPNG.get()

        createImage(inputPNG)


# reset - pobiera ponownie dane z pliku i aktualizuje pole
def getValuesAgain():
    config = ConfigParser()

    config.read('config.ini')
    global start
    global finish
    global output
    global outputt
    global inputPNG

    inputPNG = config.get('Config', 'input')
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

    entryInputPNG.delete(0, tk.END)
    entryStart.delete(0, tk.END)
    entryStartt.delete(0, tk.END)
    entryFinish.delete(0, tk.END)
    entryFinishh.delete(0, tk.END)
    entryOutput.delete(0, tk.END)
    entryOutputt.delete(0, tk.END)

    entryInputPNG.insert(tk.END, inputPNG)
    entryStart.insert(tk.END, start[0])
    entryStartt.insert(tk.END, start[1])
    entryFinish.insert(tk.END, finish[0])
    entryFinishh.insert(tk.END, finish[1])
    entryOutput.insert(tk.END, output)
    entryOutputt.insert(tk.END, outputt)

    createImage(inputPNG)


# metoda heurystyczna - Euclidian Distance
def heuristic(a, b):
    return math.sqrt((b[0] * a[0]) + (b[1] * a[1]))


# algorytm
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

# pocztek programu
if __name__ == "__main__":
    getValues()
    initInterface()

# todo
#   1. Pokaz punkty startowe init interfejs
#   2. Priority dla lini prostych zamiast skośnych
#   3. Zmiana na manhatan i ruch bez skosow
#   4. wymyśl coś jeszcze xd
