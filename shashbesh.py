import pygame
import random
import tkinter as tk

pygame.init()
# window size
display_width = 1000
display_height = 700
# stone size
stone_width = 64
stone_height = 64
# border size
border_width = 65
border_height = 350

# create screen
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("SHESHBESH")
clock = pygame.time.Clock()

Board = pygame.image.load('Board.jpg')
Board = pygame.transform.scale(Board, (1000, 700))
blackStone = pygame.image.load('blackStoneSmall.png')
blackStone = pygame.transform.scale(blackStone, (stone_width, stone_height))
whiteStone = pygame.image.load('whiteStoneSmall.png')
whiteStone = pygame.transform.scale(whiteStone, (stone_width, stone_height))
upperBorder = pygame.image.load('upperBorder.png')
upperBorder = pygame.transform.scale(upperBorder, (border_width, border_height))
downBorder = pygame.image.load('downBorder.png')
downBorder = pygame.transform.scale(downBorder, (border_width, border_height))

black = (0, 0, 0)
white = (255, 255, 255)
white1 = (220, 220, 220)
green = (0, 255, 0)
bright_green = (0, 220, 0)

crashed = False  # we play until we are not crashed
mouse = pygame.mouse.get_pos()
flag = True
whosturn = True  # True =white player, False = black player
keytomove = None  # the key we are moving now
stonefirstlocx = None  # stone first x location
stonefirstlocy = None  # stone first x location
key = 'blabla'
backtobordflag = False
leftclick = False  # if we clicked on left button of the mouse
newgame = None  # flag for new game
xpos = 0
ypos = 0
cube1 = None  # cube 1 of the game
cube2 = None  # cube 2 of the game
flagcube1 = None  # flag that show the current status of cube 1
flagcube2 = None  # flag that show the current status of cube 2
diceflag = None  # did we dice or not
newdice = True  # if True we can dice if False we cant dice
movecounter = 0  # count how many steps we did in this turn

# those dicts are used to know the location of each stone
# the location is combination of 2 dicts 1 dict for x axis and 1 for y axis


xDOWNPosition_dict = {1: 832, 2: 767, 3: 699, 4: 638, 5: 570, 6: 506, 7: 328, 8: 269, 9: 199, 10: 138, 11: 70, 12: 5,
                      26: 418}  # position of axis x at the lower part of the bord
xUPPosition_dict = {13: 5, 14: 70, 15: 138, 16: 199, 17: 269, 18: 328, 19: 506, 20: 570, 21: 638, 22: 699, 23: 767,
                    24: 830, 25: 418}  # position of axis x at the upper part of the bord
yDOWNPosition_dict = {1: 632, 2: 568, 3: 504, 4: 440,
                      5: 376}  # , 6: 376, 7: 376, 8: 376, 9: 376, 10: 376}   # position of axis y at the lower part of the bord
yUPPosition_dict = {1: 4, 2: 68, 3: 132, 4: 196, 5: 260,
                    6: 324}  # , 7: 292, 8: 228, 9: 164, 10: 100}    # position of axis y at the upper part of the bord
position_dict = {'xdown': xDOWNPosition_dict, 'xup': xUPPosition_dict, 'ydown': yDOWNPosition_dict,
                 'yup': yUPPosition_dict}  # this guide us to whict dict we go

stones_dict = {}  # main dict, here we save all the data about the stones

whiteStonesList = []
blackStonesList = []
stonesList = []


def popupmsg(msg):
    """
    this func get a string and pop it up to the screen as a message window
    :param msg: string
    """
    popup = tk.Tk()
    popup.wm_title('!')
    label = tk.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)
    b1 = tk.Button(popup, text='Okay', command=popup.destroy)
    b1.pack()
    popup.mainloop()


def findPixelsWithCells(x, y):
    """
    the func get x,y of cell and give it's pixel location on the screen
    :param x: location x of the cell
    :param y: location x of the cell
    :return: x,y and pixels
    """
    xpos = 0
    ypos = 0
    if x <= 12 and x >= 0 or x == 26:
        xpos = position_dict['xdown'].get(x)
        ypos = position_dict['ydown'].get(y)
    elif x <= 25 and x >= 13:
        xpos = position_dict['xup'].get(x)
        ypos = position_dict['yup'].get(y)
    return xpos, ypos


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def dice():
    """
    this function responsible to dice our cubes
    """
    global diceflag
    global newdice
    if newgame == False and newdice == True:
        newdice = False
        global cube1
        global cube2
        global flagcube1
        global flagcube2

        cube1 = random.randint(1, 6)
        cube2 = random.randint(1, 6)
        flagcube1 = cube1
        flagcube2 = cube2

        diceflag = True
    elif newgame == False and newdice == False:
        popupmsg('you allready diced')
    else:
        popupmsg('start a game before dice')


def whichCubeisUsed(stonefirstloc1, newloc, type):
    """
    this function calculate which cube1 is used by getting the old location and the new location
    :param stonefirstloc: old location of the stone
    :param newloc: the new location of the stone
    :param type: type of the stone
    :return: int: 1 - cube1, 2 - cube2, 3 - cube1&cube2
    """
    if stonefirstloc1 == 26:
        stonefirstloc = 25
    elif stonefirstloc1 == 25:
        stonefirstloc = 0
    else:
        stonefirstloc = stonefirstloc1
    if type == blackStone:
        if newloc - stonefirstloc == cube1:
            return 1
        elif newloc - stonefirstloc == cube2:
            return 2
        elif newloc - stonefirstloc == (cube1 + cube2):
            return 3
    else:  # whitestone
        if stonefirstloc - newloc == cube1:
            return 1
        elif stonefirstloc - newloc == cube2:
            return 2
        elif stonefirstloc - newloc == (cube1 + cube2):
            return 3


def makeStone(type, x, y, key):
    """
    this func init the object "stone". there are 2 types 'w' - white stone, 'b' - black stone. x,y are the location
    of the cell where the stone stays. key is the name of the stone.
    :param type: string
    :param x: int
    :param y: int
    :param key: string
    :return: stone object
    """
    xpos, ypos = findPixelsWithCells(x, y)
    if type == 'b':
        return ('blackStoneSmall.png', xpos, ypos, key)
    elif type == 'w':
        return ('whiteStoneSmall.png', xpos, ypos, key)


def findKey(xloc, yloc):
    """
    get x,y location and search for stone at the same place.
    :param xloc: int
    :param yloc: int
    :return: if stone was found return the key else None
    """
    print(xloc, yloc)
    for key in stones_dict.keys():
        if stones_dict[key][1] == xloc and stones_dict[key][2] == yloc:
            return stones_dict[key][3]


def changeFlagCubeToUse(number):
    """
    this func change the flag of each cube if it was used the number we get means which cube were used.
    1 - flagcube1, 2 - flagcube2, 3 - flagcube1 and flagcube2
    :param number: int
    """
    global flagcube1
    global flagcube2
    global cube1
    global cube2
    global movecounter
    if cube1 != cube2 or ((cube1 == cube2) and movecounter >= 2):
        if number == 1:
            flagcube1 = None
        elif number == 2:
            flagcube2 = None
        elif number == 3:
            flagcube1 = None
            flagcube2 = None


def checkDropLocation(stonefirstlocx, x, type, etan=None):
    """
    this func check if the drop location is available
    :param stonefirstlocx: the old place of the stone
    :param x: new place to place the stone
    :param type: black or white so we know how to "walk" to which direction
    :param etan: check if there is any eaten player
    :return: True place is available else False
    """
    global flagcube1
    global flagcube2
    if cube1 == None or cube2 == None:
        popupmsg("you need to dice before you play")
        return False
    if cube1 == cube2:
        print('cube1 == cube2')
    if type == blackStone:
        if stonefirstlocx == 25:
            stonefirstlocx1 = 0
        else:
            stonefirstlocx1 = stonefirstlocx
        if (stonefirstlocx1 + cube1) == x and flagcube1 != None:
            return True
        elif (stonefirstlocx1 + cube2) == x and flagcube2 != None:
            return True
        elif (stonefirstlocx1 + cube1 + cube2) == x and etan == None and (flagcube1 != None or flagcube1 != None):
            return True
    elif type == whiteStone:
        if stonefirstlocx == 26:
            stonefirstlocx1 = 25
        else:
            stonefirstlocx1 = stonefirstlocx
        if (stonefirstlocx1 - cube1) == x and flagcube1 != None:
            return True
        elif (stonefirstlocx1 - cube2) == x and flagcube2 != None:
            return True
        elif (stonefirstlocx1 - cube1 - cube2) == x and etan == None and (flagcube1 != None or flagcube1 != None):
            return True
    return False


def countMovment(numberOfSteps=None):
    global backtobordflag
    global movecounter
    global newdice
    if backtobordflag == True:
        print("264")
    if numberOfSteps == 1 or numberOfSteps == 2:
        movecounter += 1
    elif numberOfSteps == 3:
        movecounter += 2

    if cube1 == cube2 and movecounter == 4:  # check for "double" movement
        movecounter = 0
        newdice = True
        changePlayerTurn()
    elif cube1 != cube2 and movecounter == 2:
        movecounter = 0
        newdice = True
        changePlayerTurn()
    if (cube2 == cube1 and movecounter > 4) or (cube2 != cube1 and movecounter > 2):
        if numberOfSteps == 1 or numberOfSteps == 2:
            movecounter -= 1
        else:
            movecounter -= 2
        return False
    else:
        return True


def entryNotAvailable(msg):
    popupmsg(msg)
    pass


def backToBord():
    global backtobordflag
    backtobordflag = True
    x, y = findStoneLocation(mouse[0], mouse[1])
    etanstone = etanStone()
    keytomovetype = checkType(keytomove)

    if etanstone != None and etanstone == keytomove:
        if x >= 1 and x <= 6:
            if checkDropLocation(25, x, keytomovetype, True) == True:
                moveStone()
            else:
                entryNotAvailable("entry not available ")

        elif x >= 18 and x <= 24:
            if checkDropLocation(26, x, keytomovetype, True) == True:
                moveStone()
            else:
                entryNotAvailable("entry not available ")


def moveStone():
    print(' move stone')
    x, y = findStoneLocation(mouse[0], mouse[1])
    for highesty in range(15, 0, -1):
        newstoneplace = findKey(x, highesty)
        newstoneplacetype = checkType(newstoneplace)
        keytomovetype = checkType(keytomove)

        if newdice == True:
            popupmsg('you have to dice before you play!')
            break

        if keytomovetype != checkWhosTurn():
            if keytomovetype == whiteStone:
                qwe = 'white'
            else:
                qwe = 'black'
            msg = 'it is not '
            msg += qwe
            msg += ' turn'
            popupmsg(msg)
            break

        elif newstoneplace != None and highesty >= 2 and newstoneplacetype != keytomovetype:  # different type
            if checkDropLocation(stonefirstlocx, x, keytomovetype) == True:
                print('cant go here taken by other player')
                stones_dict[keytomove][1], stones_dict[keytomove][2] = stonefirstlocx, stonefirstlocy
                pygame.display.update()
                break
        elif newstoneplace != None and highesty >= 1 and newstoneplacetype == keytomovetype:  # same type
            if checkDropLocation(stonefirstlocx, x, keytomovetype) == True:
                print('stone joined to the building')
                usedcube = whichCubeisUsed(stonefirstlocx, x, keytomovetype)
                countMovment(usedcube)
                changeFlagCubeToUse(usedcube)
                stones_dict[keytomove][1], stones_dict[keytomove][2] = x, y
                moveStonesDownInSlot(stonefirstlocx)
                moveStonesDownInSlot(x)
                pygame.display.update()
                break
        elif newstoneplace != None and highesty == 1 and newstoneplacetype != keytomovetype:  # eat player
            if checkDropLocation(stonefirstlocx, x, keytomovetype) == True:
                print('eat player')
                print('newstoneplace ', newstoneplace)
                if newstoneplacetype == blackStone:
                    k = None
                    for i in range(1, 15):
                        k = findKey(25, i)
                        if k == None:
                            k = i
                            break
                    stones_dict[newstoneplace][1], stones_dict[newstoneplace][2] = 25, k
                    pygame.display.update()
                else:
                    k = None
                    for i in range(1, 15):
                        k = findKey(26, i)
                        if k == None:
                            k = i
                            break
                    stones_dict[newstoneplace][1], stones_dict[newstoneplace][2] = 26, k
                moveStonesDownInSlot(stonefirstlocx)
                stones_dict[keytomove][1], stones_dict[keytomove][2] = x, 1
                usedcube = whichCubeisUsed(stonefirstlocx, x, keytomovetype)
                countMovment(usedcube)
                changeFlagCubeToUse(usedcube)
                pygame.display.update()
                break
        elif newstoneplace == None and highesty == 1:  # move player to empty place
            if checkDropLocation(stonefirstlocx, x, keytomovetype) == True:
                print('move the stone here')
                print('newstoneplace ', newstoneplace)
                stones_dict[keytomove][1], stones_dict[keytomove][2] = x, 1
                moveStonesDownInSlot(stonefirstlocx)
                usedcube = whichCubeisUsed(stonefirstlocx, x, keytomovetype)
                countMovment(usedcube)
                changeFlagCubeToUse(usedcube)
                pygame.display.update()
            else:
                print('bad location')
            pygame.display.update()
            break


def showBorder(x):
    # for down border axis y is 350
    # for down border axis x is border_width * number of place
    if x >= 1 and x <= 6:
        gameDisplay.blit(downBorder, (xDOWNPosition_dict[x], 350))
    elif x >= 7 and x <= 12:
        gameDisplay.blit(downBorder, (xDOWNPosition_dict[x], 350))
    elif x >= 13 and x <= 18:
        gameDisplay.blit(upperBorder, (xUPPosition_dict[x], 0))
    elif x >= 19 and x <= 24:
        gameDisplay.blit(upperBorder, (xUPPosition_dict[x], 0))
    pygame.display.update()


def initStones():
    print('init stones')
    ws1 = makeStone('w', 24, 1, 'ws1')
    stonesList.append(ws1)
    ws2 = makeStone('w', 24, 2, 'ws2')
    stonesList.append(ws2)
    ws3 = makeStone('w', 6, 1, 'ws3')
    stonesList.append(ws3)
    ws4 = makeStone('w', 6, 2, 'ws4')
    stonesList.append(ws4)
    ws5 = makeStone('w', 6, 3, 'ws5')
    stonesList.append(ws5)
    ws6 = makeStone('w', 6, 4, 'ws6')
    stonesList.append(ws6)
    ws7 = makeStone('w', 6, 5, 'ws7')
    stonesList.append(ws7)
    ws8 = makeStone('w', 8, 1, 'ws8')
    stonesList.append(ws8)
    ws9 = makeStone('w', 8, 2, 'ws9')
    stonesList.append(ws9)
    ws10 = makeStone('w', 8, 3, 'ws10')
    stonesList.append(ws10)
    ws11 = makeStone('w', 13, 1, 'ws11')
    stonesList.append(ws11)
    ws12 = makeStone('w', 13, 2, 'ws12')
    stonesList.append(ws12)
    ws13 = makeStone('w', 13, 3, 'ws13')
    stonesList.append(ws13)
    ws14 = makeStone('w', 13, 4, 'ws14')
    stonesList.append(ws14)
    ws15 = makeStone('w', 13, 5, 'ws15')
    stonesList.append(ws15)
    bs1 = makeStone('b', 1, 1, 'bs1')
    stonesList.append(bs1)
    bs2 = makeStone('b', 1, 2, 'bs2')
    stonesList.append(bs2)
    bs3 = makeStone('b', 12, 1, 'bs3')
    stonesList.append(bs3)
    bs4 = makeStone('b', 12, 2, 'bs4')
    stonesList.append(bs4)
    bs5 = makeStone('b', 12, 3, 'bs5')
    stonesList.append(bs5)
    bs6 = makeStone('b', 12, 4, 'bs6')
    stonesList.append(bs6)
    bs7 = makeStone('b', 12, 5, 'bs7')
    stonesList.append(bs7)
    bs8 = makeStone('b', 17, 1, 'bs8')
    stonesList.append(bs8)
    bs9 = makeStone('b', 17, 2, 'bs9')
    stonesList.append(bs9)
    bs10 = makeStone('b', 17, 3, 'bs10')
    stonesList.append(bs10)
    bs11 = makeStone('b', 19, 1, 'bs11')
    stonesList.append(bs11)
    bs12 = makeStone('b', 19, 2, 'bs12')
    stonesList.append(bs12)
    bs13 = makeStone('b', 19, 3, 'bs13')
    stonesList.append(bs13)
    bs14 = makeStone('b', 19, 4, 'bs14')
    stonesList.append(bs14)
    bs15 = makeStone('b', 19, 5, 'bs15')
    stonesList.append(bs15)

    print(stonesList)

    for i in range(0, 30):
        x, y = findStoneLocation(stonesList[i][1], stonesList[i][2])
        if stonesList[i][0] == 'whiteStoneSmall.png':
            key = stonesList[i][3]  # 'ws' + str(i + 1)
            stones_dict.setdefault(key, [])
            stones_dict[key].append('whiteStoneSmall.png')
            stones_dict[key].append(x)
            stones_dict[key].append(y)
            stones_dict[key].append(stonesList[i][3])
        else:
            key = stonesList[i][3]  # 'bs' + str((i-15) + 1)
            stones_dict.setdefault(key, [])
            stones_dict[key].append('blackStoneSmall.png')
            stones_dict[key].append(x)
            stones_dict[key].append(y)
            stones_dict[key].append(stonesList[i][3])
    """for i in range(0, 15):
        x, y = findStoneLocation(blackStonesList[i][1], blackStonesList[i][2])
        key = 'bs' + str(i + 1)
        stones_dict.setdefault(key, [])
        stones_dict[key].append('blackStoneSmall.png')
        stones_dict[key].append(x)
        stones_dict[key].append(y)
        stones_dict[key].append(blackStonesList[i][3])"""

    for s in stones_dict:
        print(s, ' ', stones_dict[s])


def findStoneLocation(x, y):
    """
    this function get x and y location of the mouse and turn it to x and y of 'cell' location
    :param x: mouse x location
    :param y: mouse y location
    :return: x,y location of the 'cell'
    """
    xloc = 2000
    yloc = 2000
    if y >= 0 and y <= 330:
        for yval in yUPPosition_dict.keys():
            if y >= yUPPosition_dict[yval] and y <= yUPPosition_dict[yval] + 63:
                yloc = yval
        for xval in xUPPosition_dict.keys():
            if x >= xUPPosition_dict[xval] and x <= xUPPosition_dict[xval] + 63:
                xloc = xval
    elif y >= 375 and y <= 696:
        for yval in yDOWNPosition_dict.keys():
            if y >= yDOWNPosition_dict[yval] and y <= yDOWNPosition_dict[yval] + 63:
                yloc = yval
        for xval in xDOWNPosition_dict.keys():
            if x >= xDOWNPosition_dict[xval] and x <= xDOWNPosition_dict[xval] + 63:
                xloc = xval

    return xloc, yloc


def findMouseLocation():
    """
    this function find the mouse location and convert it to specific pixel where the cell begins
    :return:the exact position of the beginning of the cell
    """
    mouse = pygame.mouse.get_pos()
    xloc = 2000
    yloc = 2000
    y = mouse[1]
    x = mouse[0]
    if y >= 0 and y <= 330:
        for yval in yUPPosition_dict.keys():
            if y >= yUPPosition_dict[yval] and y <= yUPPosition_dict[yval] + 63:
                yloc = yUPPosition_dict[yval]
        for xval in xUPPosition_dict.keys():
            if x >= xUPPosition_dict[xval] and x <= xUPPosition_dict[xval] + 63:
                xloc = xUPPosition_dict[xval]
    elif y >= 375 and y <= 696:
        for yval in yDOWNPosition_dict.keys():
            if y >= yDOWNPosition_dict[yval] and y <= yDOWNPosition_dict[yval] + 63:
                yloc = yDOWNPosition_dict[yval]
        for xval in xDOWNPosition_dict.keys():
            if x >= xDOWNPosition_dict[xval] and x <= xDOWNPosition_dict[xval] + 63:
                xloc = xDOWNPosition_dict[xval]

    return xloc, yloc



def checkType(key):
    type = None
    if key == None:
        return type
    elif stones_dict[key][0] == 'blackStoneSmall.png':
        type = blackStone
        print('black')
    elif stones_dict[key][0] == 'whiteStoneSmall.png':
        type = whiteStone
        print('white')
    return type


def showNextSteps(cube1, cube2, keytomove):
    x, y = findMouseLocation()
    xloc = stones_dict[keytomove][1]
    type = checkType(keytomove)
    if cube1 == None or cube2 == None:
        popupmsg("you need to dice before you play")
    elif x + stone_width > mouse[0] >= x and y + stone_height > mouse[1] >= y:
        if type == blackStone:  # show border for black stone
            if xloc == 25:
                showBorder(cube1)
                showBorder(cube2)
            else:
                showBorder(cube1 + xloc)
                showBorder(cube2 + xloc)
                showBorder(cube1 + cube2 + xloc)
        else:  # show border for white stone
            if xloc == 26:
                showBorder(25 - cube1)
                showBorder(25 - cube2)
            else:
                showBorder(xloc - cube1)
                showBorder(xloc - cube2)
                showBorder(xloc - (cube1 + cube2))


def firstClickLocation():
    stonefirstlocx, stonefirstlocy = findStoneLocation(mouse[0], mouse[1])
    return stonefirstlocx, stonefirstlocy, False


def checkWhosTurn():
    """
    True - white stone turn
    False - black stone turn
    :return: True/False
    """
    if whosturn:
        return whiteStone
    return blackStone


def changePlayerTurn():
    global whosturn
    if checkWhosTurn() == whiteStone:
        whosturn = False
    else:
        whosturn = True


def moveStonesDownInSlot(xloc):
    """
    this func get the slot of the moving stone and move down all the stones at the same slot
    :return:
    """
    lowest_i = None
    for i in range(1, 14):
        next_i = i + 1
        lowerkey = findKey(xloc, i)
        upperkey = findKey(xloc, next_i)
        if lowerkey != None:
            lowest_i = i
        if lowerkey == None and upperkey == None and i == 13:
            break
        elif lowerkey == None and upperkey == None:
            pass
        elif lowerkey == None and upperkey != None and lowest_i != None:
            stones_dict[upperkey][2] = lowest_i + 1
        elif lowerkey == None and upperkey != None and lowest_i == None:
            stones_dict[upperkey][2] = i


def restartGame():
    global newgame
    global diceflag
    if newgame != None:
        stonesList.clear()
        stones_dict.clear()
        pygame.display.update()
        diceflag = False
    newgame = True


def etanStone():
    print('etanstone')
    x25 = findKey(25, 1)  # black stone
    x26 = findKey(26, 1)  # white stone
    type = checkWhosTurn()
    if type == whiteStone:
        print('etan stone white')
        return x26
    elif type == blackStone:
        print('etan stone black')
        return x25
    else:
        print('etan stone None')
        return None


def button(msg, x, y, w, h, hover_color, active_color, action=None):
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, hover_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
    smallText = pygame.font.Font('freesansbold.ttf', 12)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


while not crashed:

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x, y = findMouseLocation()
    x, y = findStoneLocation(x, y)
    pygame.display.update()
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.display.update()
        if event.type == pygame.QUIT:
            crashed = True

        gameDisplay.blit(Board, (0, 0))
        button("DICE", 920, 330, 60, 40, white1, white, dice)  # dice button
        button('NEW GAME', 920, 5, 60, 40, bright_green, green, restartGame)  # start new game button
        if diceflag:
            msg = str(cube1)
            msg += ' : '
            msg += str(cube2)
            turn = checkWhosTurn()
            smallText = pygame.font.Font('freesansbold.ttf', 20)
            textSurf, textRect = text_objects(msg, smallText)
            textRect.center = (450, 350)
            gameDisplay.blit(textSurf, textRect)
            if not newdice:
                if turn == whiteStone:
                    turnmsg = "White move"
                else:
                    turnmsg = "Black move"
            smallerText = pygame.font.Font('freesansbold.ttf', 12)
            textSurf, textRect = text_objects(turnmsg, smallerText)
            textRect.center = (450, 370)
            gameDisplay.blit(textSurf, textRect)

        if newgame:
            print('newgame')
            whosturn = True
            initStones()
            newgame = False

        for stone in stonesList:
            for keystone in stones_dict.keys():
                if stone[3] == keystone:
                    if stone[0] == 'blackStoneSmall.png':
                        type = blackStone
                    else:
                        type = whiteStone
                    x, y = findPixelsWithCells(stones_dict[keystone][1], stones_dict[keystone][2])
                    gameDisplay.blit(type, (x, y))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('MOUSEBUTTONDOWN')
            pygame.display.update()
            if flag:
                stonefirstlocx, stonefirstlocy, flag = firstClickLocation()

            keytomove = findKey(stonefirstlocx, stonefirstlocy)
            type = checkType(keytomove)
            print(stones_dict)
            if click[2] == 1 and keytomove != None:  # and type == checkWhosTurn():
                print('right click')
                showNextSteps(cube1, cube2, keytomove)
            elif click[0] == 1:
                print('left click')
                leftclick = True
                if flag:
                    stonefirstlocx, stonefirstlocy, flag = firstClickLocation()

                keytomove = findKey(stonefirstlocx, stonefirstlocy)

                if keytomove != None:
                    x, y = findStoneLocation(mouse[0], mouse[1])
                    stones_dict[keytomove][1], stones_dict[keytomove][2] = x, y  # mouse[0], mouse[1]
                    type = checkType(keytomove)
                    break
            else:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            print('MOUSEBUTTONUP')
            if leftclick:
                leftclick = False
                flag = True
                print(keytomove)
                etanstone = etanStone()
                if keytomove == None:
                    print('keytomove == None ', stonefirstlocx, stonefirstlocy)
                elif etanstone != None and etanstone != keytomove:
                    popupmsg('you need to move etan stones first')
                elif etanstone != None and etanstone == keytomove:
                    backToBord()
                elif keytomove != None:
                    moveStone()

                pygame.display.update()

        pygame.display.update()
    flag = True
    clock.tick(60)

pygame.display.update()

clock.tick(60)

pygame.quit()
