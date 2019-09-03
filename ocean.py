from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Label
from random import randint
from time import sleep


def loadImg(name):
    global N, W, buf
    d = (W // N)
    load = Image.open(name)
    load = load.resize((d, d), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    return img


def drawCeil(x, y, px, py):
    global canvas, N, W
    d = (W // N)
    canvas.create_rectangle((x * d + px, y * d + py), (x * d + d + px,y * d + d + py))


def drawSmth(x, y, w, px, py):
    global canvas, N, W
    d = (W // N)
    bo = False
    if w == 2:
        smth = loadImg("ocean/fish.png")
        bo = True
    elif w == 1:
        smth = loadImg("ocean/rock.png")
        bo = True
    elif w == 3:
        smth = loadImg("ocean/crevette.png")
        bo = True
    if bo:
        canvas.create_window(x * d + px + (d // 2), y * d + py + (d // 2), window=smth)


def write():
    global canvas
    tx = Label(canvas, text="press any key to see the ocean life")
    canvas.create_window(300, 550, window=tx)


def drawField(px=0, py=0):
    global N, ocean
    for i in range(N):
        for j in range(N):
            drawSmth(j, i, ocean[i][j], px, py)
            drawCeil(j, i, px, py)


def update(a): #0 - nothing, 1 - death, 2 - born fish, 3 - born shrimp
    global ocean, N
    for i in range(N):
        for j in range(N):
            if a[i][j] == 1:
                ocean[i][j] = 0
            elif a[i][j] == 2:
                ocean[i][j] = 2
            elif a[i][j] == 3:
                ocean[i][j] = 3


def gen(i, j):
    global N
    ans = []
    if i != 0 and j != 0:
        ans.append([i - 1, j - 1])
    if i != 0:
        ans.append([i - 1, j])
    if i != 0 and j != N - 1:
        ans.append([i - 1, j + 1])
    if j != 0:
        ans.append([i, j - 1])
    if j != N - 1:
        ans.append([i, j + 1])
    if i != N - 1 and j != 0:
        ans.append([i + 1, j - 1])
    if i != N - 1:
        ans.append([i + 1, j])
    if i != N - 1 and j != N - 1:
        ans.append([i + 1, j + 1])
    return ans


def checkDeathCeil(x, y, n):
    global ocean
    if ocean[x][y] != n:
        return False
    g = gen(x, y)
    counter = 0
    for i in g:
        if ocean[i[0]][i[1]] == n:
            counter += 1
    if counter < 2 or counter >= 4:
        return True
    return False


def checkDeath(n):
    global N
    ans = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            if checkDeathCeil(i, j, n):
                ans[i][j] = 1
    return ans


def checkBornCeil(x, y, n):
    global ocean
    if ocean[x][y] != 0:
        return False
    g = gen(x, y)
    counter = 0
    for i in g:
        if ocean[i[0]][i[1]] == n:
            counter += 1
    if counter == 3:
        return True
    return False


def checkBorn(n, a):
    global N
    ans = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            if not (n == 3 and a[i][j] == 2):
                if checkBornCeil(i, j, n):
                    ans[i][j] = n
    return ans


def year():
    a = checkDeath(2)
    b = checkDeath(3)
    c = checkBorn(2, b)
    d = checkBorn(3, c)
    update(a)
    update(b)
    update(c)
    update(d)


def clear():
    global canvas
    canvas.delete("all")


def run(event):
    global canvas, ocean
    clear()
    year()
    drawField(50, 20)
    write()
    canvas.pack()

N = 10 #field size
W = 500 #field width
ocean = [[randint(0, 3) for i in range(N)] for j in range(N)]

master = Tk()

canvas = Canvas(master, height = 600, width = 600)

drawField(50, 20)
write()
canvas.pack()
master.bind("<KeyPress>", run)
master.mainloop()
