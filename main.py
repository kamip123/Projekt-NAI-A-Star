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

    global label3
    global label4
    label3.destroy()
    label4.destroy()

    routelengthint = str(len(wierzcholki))
    routelength = "Dlugość ścieżki: " + routelengthint
    label3 = tk.Label(window, text=routelength, font=("Helvetica", 15))
    label3.grid(column=0, row=4)

    elapsedtime = math.floor(elapsed_time*100)/100
    elapsedtime = str(elapsedtime)
    elapsedtimestring = "Czas dzialania algorytmu: " + elapsedtime + " sekund"
    label4 = tk.Label(window, text=elapsedtimestring, font=("Helvetica", 15))
    label4.grid(column=0, row=5)


# zmienia tryb - ruchy skośne lub bez
def zmienTryb():
    global typ
    global label2
    global buttonTryb
    # swap po kliknieciu przycisku
    if typ == 0:
        typ = 1
    else:
        typ = 0

    if typ == 0:
        skosneLubBez = "Tryb bez ruchów skośnych"
        buttonNameSkosneLubBez = "Zamien na ruchy skośne"
    else:
        skosneLubBez = "Tryb z ruchami skośnymi"
        buttonNameSkosneLubBez = "Zamien na ruchy bez skosów"

    label2.destroy()
    buttonTryb.destroy()

    label2 = tk.Label(window, text=skosneLubBez, font=("Helvetica", 15))
    label2.grid(column=0, row=3)

    buttonTryb = tk.Button(window, text=buttonNameSkosneLubBez, command=zmienTryb, fg="red")
    buttonTryb.grid(column=2, row=1)


# init interfejsu
def initInterface():
    global window
    window = tk.Tk()
    createWindow()
    initializeWindow()


# stworz interfejs
def createWindow():

    if typ == 0:
        skosneLubBez = "Tryb bez ruchów skośnych"
        buttonNameSkosneLubBez = "Zamien na ruchy skośne"
    else:
        skosneLubBez = "Tryb z ruchami skośnymi"
        buttonNameSkosneLubBez = "Zamien na ruchy bez skosów"

    label = tk.Label(window, text="Projekt NAI - A* + interfejs graficzny", font=("Helvetica", 20))
    label.grid(column=0, row=0)

    buttonUruchom = tk.Button(window, text="Uruchom program", command=uruchomProgram, fg="red")
    buttonUruchom.grid(column=1, row=1)

    global buttonTryb
    global label2

    buttonTryb = tk.Button(window, text=buttonNameSkosneLubBez, command=zmienTryb, fg="red")
    buttonTryb.grid(column=2, row=1)

    buttonZmiany = tk.Button(window, text="Zatwierdz zmiany", command=zmianyInput, fg="red")
    buttonZmiany.grid(column=2, row=7)

    buttonResetuj = tk.Button(window, text="Resetuj", command=getValuesAgain, fg="red")
    buttonResetuj.grid(column=3, row=7)

    label2 = tk.Label(window, text=skosneLubBez, font=("Helvetica", 15))
    label2.grid(column=0, row=3)

    global label3
    global label4

    label3 = tk.Label(window, text="Długość ścieżki: ", font=("Helvetica", 15))
    label3.grid(column=0, row=4)

    label4 = tk.Label(window, text="Czas dzialania algorytmu: ", font=("Helvetica", 15))
    label4.grid(column=0, row=5)

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
    canvas = tk.Canvas(window, width=400, height=400)
    imgToScale = Image.open(inputPNG).convert('RGBA')
    imgToScale = numpy.array(imgToScale)
    imgToScale[finish[0]][finish[1]] = (0, 255, 0, 255)
    imgToScale[start[0]][start[1]] = (255, 255, 0, 255)
    imgToScale = Image.fromarray(imgToScale, 'RGBA')
    imgToScale = imgToScale.resize((400, 400))
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

    if typ == 0:
        zmienTryb()

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
    if typ == 0:
        return abs(b[0]-a[0]) + abs(b[1]-a[1])
    else:
        return math.sqrt(pow(b[0]-a[0], 2) + pow(b[1]-a[1], 2))


# algorytm
def astar(tablicaLabiryntu, start, goal):
    if typ == 1:
        # z skosami
        neighbors = [(1, 1), (-1, 1), (-1, -1), (1, -1),(1, 0), (0, 1), (-1, 0), (0, -1)]
    else:
        # bez skosow
        neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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
    global typ
    typ = 1
    getValues()
    initInterface()

# todo
# DONE 1. Pokaz punkty startowe init interfejs
# DONE 2. Priority dla lini prostych zamiast skośnych
# DONE 3. Zmiana na manhatan i ruch bez skosow
#      4. wymyśl coś jeszcze xd
