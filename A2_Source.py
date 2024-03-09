import turtle
import random
import time

g_screen = None
g_statusArea = None
g_motionArea = None
g_intro = None
g_contact = 0
g_time = 0
g_motion = "Paused"
g_message = None
g_snake = None
g_monster = None
g_food = [''] * 9
g_tailPositions = []
g_tailLength = 5
g_startTime = 0
g_monsterTimerRate = 700

def setTurtle(shape="square", color="black", x=0, y=0):  # set all Turtle objects
    t = turtle.Turtle(shape)
    t.penup()  # set pen up to avoid drawing lines while moving
    t.color(color)
    t.setpos(x,y)
    return t
    
def setGameArea():
    g_screen = turtle.Screen()
    g_screen.title("Snake")
    g_screen.setup(660, 740)
    g_screen.tracer(0)                 # turn off auto screen refresh
    g_statusArea = setTurtle(y=250)
    g_statusArea.color("black", "")    # black border without filling color
    g_statusArea.shapesize(4, 25, 3)   # default square: 20x20 status area: 80x500 border index: 3
    g_motionArea = setTurtle(y=-40)
    g_motionArea.color("black", "")
    g_motionArea.shapesize(25, 25, 3)  # motion area: 500x500
    return g_screen, g_statusArea, g_motionArea

def findAllPositions(a,b,c,d):  # find all possible positions given a=xmin, b=xmax, c=ymin, d=ymax
    allPositions = []
    for i in list(range(a, b, 20)):       # all possible xcor
        for j in list(range(c, d, 20)):   # all possible ycor
            allPositions.append((i,j))
    return allPositions

def setMonster():
    g_monster = setTurtle(color="purple")
    allPositions = findAllPositions(-230,250,-270,210)  # all possible positions for monster
    while True:
        pos = random.choice(allPositions)  # randomly choose a position from all the possible positions
        if g_snake.distance(pos) >= 200:   # check if the initial distance between monster and snake is more than 200pixels
            g_monster.setpos(pos)
            break
        else:
            continue
    return g_monster

def setFood():  # 9 food items
    allPositions = findAllPositions(-245,240,-290,200)  # all possible positions for food
    allPositions.remove((-5,-10))  # food should not coincide with snake at the beginning 
    pos = random.sample(allPositions, 9)  # randomly choose 9 positions for food 
    for k in range(9):
        g_food[k] = setTurtle()
        g_food[k].hideturtle()
        g_food[k].setpos(pos[k])  
        g_food[k].write(k+1, font=("Arial",18,"normal"))
    return g_food

def setIntro():  # Intro message on the screen at the beginning
    g_intro = setTurtle(x=-195, y=50)
    g_intro.hideturtle()
    g_intro.write("Welcome to the game of snake!\n\nYou are going to use the 4 arrow keys to move the snake\naround the screen, trying to consume all the food items\nbefore the monster catches you.\n\nClick anywhere on the screen to start the game, have fun!!!",
                  font=("Arial",16,"normal"))
    return g_intro

def setMessage():  # status message on the top
    g_message = setTurtle(y=240)
    g_message.hideturtle()
    g_message.write("Contact: %d  Time: %d  Motion: %s"%(g_contact, g_time, g_motion), 
                    align="center", font=("Arial", 20, "bold"))
    return g_message

def continueGame():  # check whether to continue the game or not
    if g_monster.distance(g_snake) <= 15:  # monster make a head-on collision with the snake
        return False
    elif g_food == ['']*9 and g_tailLength == len(g_tailPositions):  # all the foods have been consumed and the snake has fully extended
        return False
    else:
        return True

def moveMonster():  # define the motion of the monster
    global g_contact
    if continueGame():  # call the function only when the game has not finished
        (xm, ym) = g_monster.pos()
        (xs, ys) = g_snake.pos()
        if abs(xm-xs) <= abs(ym-ys):  # compare the difference of xcor and ycor of monster and snake
            if ym <= ys:  # monster is lower
                g_monster.setheading(90)  # go up
            else:  # monster is higher
                g_monster.setheading(270)  # go down
        else:
            if xm <= xs:  # monster on the left
                g_monster.setheading(0)  # go right
            else:  # monster on the right
                g_monster.setheading(180)  # go left
        g_monster.fd(20)  # move forward
        i = 0
        while i < len(g_tailPositions):
            if g_monster.distance(g_tailPositions[i]) <= 15:  # check if monster coincides with any of the tail
                g_contact += 1  # set contact number
                break
            else:
                i = i + 1
        g_screen.update()  # refresh the screen
        g_monsterTimerRate = random.randrange(300,800,100)  # randomly choose timer rate of monster, between 400 and 700
        g_screen.ontimer(moveMonster, g_monsterTimerRate)   # timer rate of monster

def eatFood():  # define the process of eating food
    global g_tailLength
    if continueGame():  # call the function only when the game has not finished
        for k in range(9):
            if g_food[k] != '':  # food_k has not been consumed
                yf = g_food[k].ycor()  
                ys = g_snake.ycor()
                if g_snake.distance(g_food[k]) <= 15 and yf < ys:  # when distance of snake and food_k smaller than 15 and ycor of food_k is bigger than snake, eat food!
                    g_tailLength += k+1  # extend snake's tail by k+1
                    g_food[k].clear()    # clear the food 
                    g_food[k] = ''       # set food to be '' after eating
        g_screen.ontimer(eatFood, 100)   # call the function every 0.1 second to check whether eat food or not

def snakeExtend():                  # extend the snake
    g_snake.color("blue", "black")  # change snake color to tail color
    g_snake.stamp()                 # make a copy of the snake to be the tail
    g_snake.color("red")            # change the color of snake back to red
    g_tailPositions.append(g_snake.pos())  # record the position of the snake which is also the tail position
    g_snake.fd(20) 
    g_screen.update()
    g_screen.ontimer(moveSnake, 600)  # while extending, timer rate of snake slow down to be 0.6 second

def moveTail():  # move the tail of the snake
    g_snake.color("blue", "black")
    g_snake.stamp()
    g_snake.color("red")
    g_tailPositions.append(g_snake.pos())
    g_snake.fd(20)
    g_snake.clearstamps(1)  # clear the first copy of the snake, which is the last tail
    g_tailPositions.remove(g_tailPositions[0])  # remove the position of the last tail
    g_screen.update()
    g_screen.ontimer(moveSnake, 300)  # velocity of snake: move every 0.3 second

def extendOrMove():  # decide whether to extend the snake or move the tail
    if len(g_tailPositions) < g_tailLength:  # tail of the snake shorter than what it has to have
        snakeExtend()  # extend the snake
    else:  # snake has been already extended
        moveTail()  # move the snake and tail

def moveSnake():  # define the motion of snake
    if continueGame():
        (x, y) = g_snake.pos()
        if g_motion == "Right":                       # motion: right
            g_snake.setheading(0)
            if x < 230:                               # haven't reach the right border of the motion area
                extendOrMove()
            else:                                     # the snake is already at the border, stop
                g_screen.ontimer(moveSnake, 300)      # moving timer rate: 0.3 second
        elif g_motion == "Up":                        # motion: up
            g_snake.setheading(90)
            if y < 190:                               # haven't reach the upper bound
                extendOrMove()
            else:                                     # already at the border, stop
                g_screen.ontimer(moveSnake, 300)
        elif g_motion == "Left":                      # motion: left
            g_snake.setheading(180)
            if x > -230:                              # haven't reach the lower bound
                extendOrMove()
            else:                                     # already at the border, stop
                g_screen.ontimer(moveSnake, 300)
        elif g_motion == "Down":                      # motion: down
            g_snake.setheading(270)
            if y > -270:                              # haven't reach the left border
                extendOrMove()
            else:                                     # already at the border, stop
                g_screen.ontimer(moveSnake, 300)
        else:                                         # motion: paused
            g_screen.ontimer(moveSnake, 300)
    else:                                             # if the game is finished
        termination()                                 # call game termination function

def moveSnakeRight():
    global g_motion
    g_motion = "Right"  # set global motion to be "right"

def moveSnakeUp():
    global g_motion
    g_motion = "Up"  # set global motion to be "up"

def moveSnakeLeft():
    global g_motion
    g_motion = "Left"  # set global motion to be "left"

def moveSnakeDown():
    global g_motion
    g_motion = "Down"  # set global motion to be "down"

def pauseSnake():
    global g_motion
    if g_motion != "Paused":  # motion before is left/right/up/down
        g_motion = "Paused"  # change to be "paused"
    else:
        if g_snake.heading() == 0:  # motion before paused: right
            g_motion = "Right"
        elif g_snake.heading() == 90:  # motion before paused: up
            g_motion = "Up"
        elif g_snake.heading() == 180:  # motion before paused: left
            g_motion = "Left"
        elif g_snake.heading() == 270:  # motion before paused: down
            g_motion = "Down"

def setKeys():  # bind keys with function 
    g_screen.onkey(moveSnakeRight, "Right")
    g_screen.onkey(moveSnakeUp, "Up")
    g_screen.onkey(moveSnakeLeft, "Left")
    g_screen.onkey(moveSnakeDown, "Down")
    g_screen.onkey(pauseSnake, "space")
    g_screen.ontimer(setKeys, 300)  # call the function every 0.3 second

def setTime():  # set up time 
    global g_time
    if continueGame():
        timeAtNow = time.time()  # time at now in seconds
        g_time = int(timeAtNow - g_startTime - 0.5)  # game time = time at now - start time - 0.5(initial delay)
        g_screen.ontimer(setTime, 100)  # call the function every 0.1 second to update the time

def updateMessage():  # update message: contact, time, and motion
    if continueGame():
        g_message.clear()  # clear message written before
        g_message.write("Contact: %d  Time: %d  Motion: %s"%(g_contact, g_time, g_motion),
                        align="center", font=("Arial", 20, "bold"))
        g_screen.ontimer(updateMessage, 100)  # update message every 0.1 second

def termination():  # game termination
    if g_monster.distance(g_snake) <= 15:  # monster catches the snake
        g_monster.write("Game Over!!!", font=("Arial", 20, "bold"))
    else:  # snake has consumed all the food
        g_snake.write("Winner!!!", font=("Arial", 20, "bold"))

def startUp(x,y):
    global g_food
    global g_startTime
    g_screen.onclick(None)  # cancel the bind of startup function and mouseclick
    g_intro.clear()         # clear the intro message
    g_food = setFood()      # set up food
    g_screen.update()       # update the screen
    g_startTime = time.time()  # record the start time
    # start the game after delaying for 0.5 second
    g_screen.ontimer(setTime, 500)
    g_screen.ontimer(updateMessage, 500)
    g_screen.ontimer(moveMonster, 500)
    g_screen.ontimer(setKeys, 500)
    g_screen.ontimer(moveSnake, 500)
    g_screen.ontimer(eatFood, 500)


if __name__ == "__main__":
    g_screen, g_statusArea, g_motionArea = setGameArea()  # set game area
    g_snake = setTurtle(color="red", y=-40)               # set snake
    g_monster = setMonster()                              # set monster
    g_intro = setIntro()                                  # set intro message
    g_message = setMessage()                              # set message
    g_screen.update()                                     # update the screen after setting
    g_screen.onclick(startUp)                             # bind mounseclick with startUp function
    g_screen.listen()
    g_screen.mainloop()