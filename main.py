import tkinter

master = tkinter.Tk()

size = 800
divisions = 50
partition = size / divisions

#simulation time between ticks
tickTime = 200

#is the simulation active?
simulating = False 

#false = dead
#anything else = alive
board = [[False for _ in range(divisions + 1)] for _ in range(divisions + 1)]

#parallel to the board, stores tuples with coordinates for tiles in the board
#used for optimization, no need to check all the tiles
aliveList = []

#to do all the changes simultaneusly and not have a single cell change affect all others
changeList= []

def indexCheck(column, row):
    if(column < 0 or column > divisions or row < 0 or row > divisions):
        return False
    return True


#change
def change(column, row):
    if(board[column][row] == False):
        board[column][row] = canvas.create_rectangle(column * partition, row* partition, (column+1)*partition, (row+1)*partition, fill="red")
        aliveList.append((column, row))

    else:
        canvas.delete(board[column][row])
        board[column][row] = False
        aliveList.remove((column, row))

def processChanges():
    for column, row in changeList:
        change(column, row)
    
    del changeList[:] #empty list

#count alive cells around the target
def count(checkColumn, checkRow):
    count = 0
    #its just easier to do this...
    #note it skips the (0,0) to avoid counting itself (if alive)
    checks = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    for column, row in checks:
        c = column + checkColumn
        r = row + checkRow

        if(indexCheck(c,r) and board[c][r] != False):
            count+=1

    return count

def tick():
    #assemble a list to check
    checkList = []
    checks = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0,0), (0, 1), (1, -1), (1, 0), (1, 1))

    for aliveColumn, aliveRow in aliveList:
        for checkColumn, checkRow in checks:
            column = aliveColumn + checkColumn
            row = aliveRow + checkRow

            if (column, row) not in checkList and indexCheck(column, row):
                checkList.append((column,row))

    #process list
    for column, row in checkList:
        c = count(column, row)
        if(board[column][row] != False):
            if (c < 2 or c > 3):
                changeList.append((column, row))
        elif(c == 3):
            changeList.append((column, row))
    
    #commit changes
    processChanges()

#add pattern
def click(event):
    #check which tile was clicked
    column, row = -1, -1
    for i in range(divisions): #column
        if(event.x >= partition * i and event.x <= partition * (i + 1)):
            column = i
    for i in range(divisions): #row
        if(event.y >= partition * i and event.y <= partition * (i+1)):
            row = i

    change(column, row)

##starter functions
def loop():
    #avoid calling time if unneccesary
    if (simulating):
        tick()
    #run every 200ms
    master.after(tickTime, loop)

def startSimulation():
    global simulating
    simulating = not simulating

def printaliveList():
    print(aliveList)
    
##prepare game
canvas = tkinter.Canvas(master, width=size, height=size)
canvas.pack()

canvas.bind("<Button-1>", click)

#menu
menubar = tkinter.Menu(master)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label = "Start/Stop Simulation", command=startSimulation)
filemenu.add_command(label = "Next Tick", command=tick)
filemenu.add_command(label = "aliveList", command=printaliveList)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.destroy)
menubar.add_cascade(label="File", menu=filemenu)

master.config(menu=menubar) #display menu

#draw the board
for i in range(divisions): #create the lines
    canvas.create_line(0, partition * i, size, partition * i)
    canvas.create_line(partition * i, 0, partition*i, size)

#start the simulation loop for later
loop()

master.mainloop()