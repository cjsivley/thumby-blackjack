###################################################################
# Blackjack for Thumby
# Todo:
# re-evaluate eatMash(). Needed or is there a better way?
# Fix natural BJ vs 21 win/lose
###################################################################
import thumby
import random
import math
import gc
import time

from sys import path
path.append("/Games/Blackjack")

#save data setup
thumby.saveData.setName("Blackjack")
#heartbeat
print("blackjack.py opened")

#import game files
from cards import *
from banner import *
from blackjackMenu import *



#globals
framerate = 24
pScore = 0
dScore = 0
dealerHandGoal = 17
bust = 22
line1 = 1
line2 = 10
line3 = 19
line4 = 28
xSlideSpeed = 4
ySlideSpeed = 2
textSpeed = 1

playerWins = 0
dealerWins = 0
hitOnSoft17 = 1

cardBack = defaultBack




if (thumby.saveData.hasItem("playerWins")):
    playerWins = int(thumby.saveData.getItem("playerWins"))
if (thumby.saveData.hasItem("dealerWins")):
    dealerWins = int(thumby.saveData.getItem("dealerWins"))
if (thumby.saveData.hasItem("cardBackKey")):
    cardBack = cardBackDict[str(thumby.saveData.getItem("cardBackKey"))]
if (thumby.saveData.hasItem("hitOnSoft17")):
    hitOnSoft17 = int(thumby.saveData.getItem("hitOnSoft17"))
        
###########################################setup
#random.seed(148954)
thumby.display.setFPS(framerate)

#functions
def drawCard(value, suit, x, y):
    newCard = thumby.Sprite(22, 30, cardFront, x, y)
    newSuit = thumby.Sprite(5, 7, suit, x+3, y+11)
    thumby.display.drawSprite(newCard)
    thumby.display.drawText(str(value), x+3, y+3, 0)
    thumby.display.drawSprite(newSuit)
    
def drawdealerHand(hand):
    back = thumby.Sprite(22, 30, cardBack, 1, 20)
    thumby.display.drawSprite(back)
    drawCard(hand[1].face, hand[1].suit, 15, 20)
    
def drawHand(hand):
    pos = [0,15,30,45,60]
    row = [20, 9]
    if len(hand) > 5:
        for i in range(5):
            drawCard(hand[i].face, hand[i].suit, pos[i], row[1])
        for i in range(5,len(hand)):
            drawCard(hand[i].face, hand[i].suit, pos[i-5], row[0])
    else:
        for i in range(len(hand)):
            drawCard(hand[i].face, hand[i].suit, pos[i], row[0])

def valueHand(hand):
    return sum(card.value for card in hand)

def shuffleDeck():
    newDeck = []
    for suit in cardSuits:
        for card in cardFaces:
            newCard = CARD(card, cardFaces[card], suit)
            newDeck.append(newCard)
    return newDeck
    
def slideCard(hand, card):
    #pos is target position
    if len(hand)+1 > 5:
        pos = (len(hand) - 5) * 15
        for y in range (41, 19, -ySlideSpeed):
            drawCard(card.face, card.suit, pos, y)
            thumby.display.update()
    else:
        pos = len(hand) * 15
        for x in range (72, pos - 1, -xSlideSpeed):
            drawCard(card.face, card.suit, x, 20)
            thumby.display.drawFilledRectangle(x+22, 20, xSlideSpeed, 20, 0) #erases previous edge of card
            thumby.display.update()
        
def slideFaceDown(hand):
    pos = hand * 15
    for x in range (72, pos - 1, -xSlideSpeed):
        back = thumby.Sprite(22, 30, cardBack, x, 20)
        thumby.display.drawFilledRectangle(x+22, 20, xSlideSpeed, 20, 0) #erases previous edge of card
        thumby.display.drawSprite(back)
        thumby.display.update()
    
def didPlayerWin(pScore, dScore):
    if pScore > 21:
        return False
    elif dScore > 21:
        return True
    elif pScore > dScore:
        return True
    else:
        return False

def waitForInput(bumper, line):
    continueBan.newText(bumper + continueString)
    wait = True
    while wait:
        thumby.display.drawFilledRectangle(0,line,72,7,0)
        thumby.display.drawText(continueBan.text, continueBan.pos, line, 1)
        thumby.display.update()
        continueBan.step(textSpeed)
        if thumby.buttonA.justPressed():
            wait = False

def splashAnimation():
    #thumby.display.drawText("Blackjack!",6,line1,1)
    thumby.display.drawText("Blackjack!",6,line1,1)
    thumby.display.drawText("A to Start",6,line2,1)
    splashHand = []
    deck = shuffleDeck()

    while True:
        for i in range(5):
            newCard = random.choice(deck)
            slideCard(splashHand, newCard)
            splashHand.append(newCard)
            deck.remove(newCard)
            if thumby.buttonA.justPressed():
                return
        
        for i in range(5):
            slideFaceDown(i)
            if thumby.buttonA.justPressed():
                return
        
        splashHand = []
        deck = shuffleDeck()
        

        
def dealerReveal(hand):
    for y in range (20, 41, ySlideSpeed):
        back = thumby.Sprite(22, 30, cardBack, 1, y)
        thumby.display.drawFilledRectangle(1, y-ySlideSpeed, 22, ySlideSpeed, 0) #erases previous edge of card
        thumby.display.drawSprite(back)
        drawCard(hand[1].face, hand[1].suit, 15, 20)
        thumby.display.update()
    for y in range (41, 19, -ySlideSpeed):
        drawCard(hand[0].face, hand[0].suit, 1, y)
        drawCard(hand[1].face, hand[1].suit, 15, 20)
        thumby.display.update()
        
def eatMash():
    # this function is placed after animations like the card slide
    # or screen changes it prevents the user from accidentally 
    # sending button presses before they see the game state.
    if thumby.buttonA.justPressed():
        print("DEBUG: A dropped")
    if thumby.buttonB.justPressed():
        print("DEBUG: B dropped")
    if thumby.buttonU.justPressed():
        print("DEBUG: U dropped")
    if thumby.buttonL.justPressed():
        print("DEBUG: L dropped")
    if thumby.buttonD.justPressed():
        print("DEBUG: D dropped")
    if thumby.buttonR.justPressed():
        print("DEBUG: R dropped")
    
############### card handler
#the card handler function must be tailored to each game.
#in blackjack the suits don't matter, and there
#are special rules regarding the value of the aces.


deck = shuffleDeck()

#random.shuffle() is not supported in micropython.
#so we can't shuffle the list then pop() each card.
#instead we must manually pull random cards and remove() them

hand = []
dealerHand = []
    
###############game loop

#draw sprites and text

#handle inputs

#decisions
playerHandScore = valueHand(hand)
dealerHandScore = valueHand(dealerHand)

#view shows different screens when d-pad is held
view = 0

#gamestates:
#splash = intro and help
#deal = deal cards and check for blackjack on turn 0.
#playerTurn = player hit/pass choice, loops until bust or pass
#dealerTurn = dramatic dealer reveal, then dealer hits until goal or bust
#scoring = score check and results, save results
#shuffle = shuffle deck and start over
#menu = navigate to help, options, etc

#splash screen
gamestate = "splash"

gameRun = True
while gameRun:
    
    if gamestate == "splash":
        splashAnimation()
        eatMash()
        gamestate = "deal"

    
    if gamestate == "deal":
        thumby.display.fill(0)
        #deal to player
        print("dealing to player")
        thumby.display.drawText("Dealing...",1,line1,1)
        thumby.display.update()
        for i in range(2):
            newCard = random.choice(deck)
            slideCard(hand, newCard)
            hand.append(newCard)
            deck.remove(newCard)
            playerHandScore = valueHand(hand)
        print("dealing to dealer")
        for i in range(2):
            newCard = random.choice(deck)
            dealerHand.append(newCard)
            deck.remove(newCard)
            dealerHandScore = valueHand(dealerHand)
        
        eatMash()
        #did the player get a blackjack?    
        if playerHandScore == 21:
            thumby.display.fill(0)
            thumby.display.drawText("Player: " + str(playerHandScore), 1,line1,1)
            drawHand(hand)
            thumby.display.update()
            waitForInput("Blackjack! ", line2)
            gamestate = "scoring"
        elif playerHandScore == 22: #did player get pair of aces on deal?
            hand[0].value = 1
            print("bust prevented by Ace")
            playerHandScore = valueHand(hand)
            gamestate = "playerTurn"
        else:
            gamestate = "playerTurn"
        
    if gamestate == "playerTurn":
        #LOOPING gamestate
        #display hands and let player take action
        # draw the cards
        
        #display based on view flags previous loop
        if view == 0:
            thumby.display.fill(0)
            thumby.display.drawText("Player: " + str(playerHandScore), 1,line1,1)
            thumby.display.drawText("A=hit,B=stay", 1,line2,1)
            drawHand(hand)
            thumby.display.update()
        
        elif view == 1:
            thumby.display.fill(0)
            thumby.display.drawText("Dealer:", 1, line1, 1)
            thumby.display.drawText("? + " + str(dealerHand[1].value), 1,line2,1)
            drawdealerHand(dealerHand)
            thumby.display.update()
            
        elif view == 2:
            thumby.display.fill(0)
            thumby.display.drawText("Wins: " + str(playerWins), 1,line1,1)
            thumby.display.drawText("Losses: " + str(dealerWins), 1,line2,1)
            thumby.display.update()
            
        elif view == 3:
            thumby.display.fill(0)
            thumby.display.drawText("Up: Dealer", 1, line1, 1)
            thumby.display.drawText("Left: Score", 1, line2, 1)
            thumby.display.drawText("Down: Menu", 1, line3, 1)
            thumby.display.update()
        # Input section
        
        #player looks at dealer hand or enters menu 
        if thumby.buttonU.pressed():
            view = 1
        elif thumby.buttonL.pressed():
            view = 2
        elif thumby.buttonR.pressed():
            view = 3
        elif thumby.buttonD.justPressed():
            menuRun()
            #load data after menu adjustments
            if (thumby.saveData.hasItem("playerWins")):
                playerWins = int(thumby.saveData.getItem("playerWins"))
            if (thumby.saveData.hasItem("dealerWins")):
                dealerWins = int(thumby.saveData.getItem("dealerWins"))
            if (thumby.saveData.hasItem("cardBackKey")):
                cardBack = cardBackDict[str(thumby.saveData.getItem("cardBackKey"))]
            if (thumby.saveData.hasItem("hitOnSoft17")):
                hitOnSoft17 = int(thumby.saveData.getTime("playerWins"))
            eatMash()
        else:
            view = 0
            
        #player hits    
        if thumby.buttonA.justPressed():
            newCard = random.choice(deck)
            slideCard(hand, newCard)
            hand.append(newCard)
            deck.remove(newCard)
            playerHandScore = valueHand(hand)
            
            #check score
            if playerHandScore >= bust:
                # if player has an ace worth 11, swap it for 1.
                for each in hand:
                    if each.value == 11:
                        each.value = 1
                        print("bust prevented by Ace")
                        playerHandScore = valueHand(hand)
                        break
            if playerHandScore >= bust:
                # if we got here, player had no aces and busts    
                thumby.display.fill(0)
                thumby.display.drawText("Player: " + str(playerHandScore), 1,line1,1)
                #thumby.display.drawText("Bust...", 1, line2, 1)
                drawHand(hand)
                thumby.display.update()
                waitForInput("Bust...", line2)
                gamestate = "scoring"
                
        #or player pass
        if thumby.buttonB.justPressed() and playerHandScore < bust:
            gamestate = "dealerTurn"
    
        #player stays, so dealer hits if needed to beat dealer score
    if gamestate == "dealerTurn":
        #LINEAR gamestate
        #show dealer hand
        dealerHandScore = valueHand(dealerHand)
        thumby.display.fill(0)
        thumby.display.drawText("Dealer: ?",1,line1,1)
        thumby.display.update()
        dealerReveal(dealerHand) #dramatic reveal of face down card
        # check for pair aces
        if (dealerHandScore == 22):
            dealerHand[0].value = 1
            dealerHandScore = valueHand(dealerHand)
        
        thumby.display.fill(0)
        thumby.display.drawText("Dealer: " + str(dealerHandScore),1,line1,1)
        drawHand(dealerHand)
        thumby.display.update()
        time.sleep(1)
        
 
            
            
        # Check for soft 17
        if hitOnSoft17 and (dealerHandScore == 17) and \
        ((dealerHand[0].value == 11) or (dealerHand[1].value == 11)):
            newCard = random.choice(deck)
            slideCard(dealerHand, newCard)
            dealerHand.append(newCard)
            deck.remove(newCard)
            dealerHandScore = valueHand(dealerHand)
            # after forced hit, check for bust.
            if dealerHandScore > 21:
                for each in dealerHand:
                    if each.value == 11:
                        each.value = 1
                        print("Dealer bust prevented by Ace")
                        dealerHandScore = valueHand(hand)
                        break
                        thumby.display.fill(0)
            thumby.display.drawText("Dealer:" + str(dealerHandScore),1,line1,1)
            drawHand(dealerHand)
            thumby.display.update()
            time.sleep(1)
        
        # Now dealer hits until 17 or bust.
        while dealerHandScore < dealerHandGoal:
            newCard = random.choice(deck)
            slideCard(dealerHand, newCard)
            dealerHand.append(newCard)
            deck.remove(newCard)
            dealerHandScore = valueHand(dealerHand)
            

            #check for dealer bust
            if dealerHandScore > 21:
                for each in dealerHand:
                    if each.value == 11:
                        each.value = 1
                        print("Dealer bust prevented by Ace")
                        dealerHandScore = valueHand(hand)
                        break
                
            thumby.display.fill(0)
            thumby.display.drawText("Dealer:" + str(dealerHandScore),1,line1,1)
            drawHand(dealerHand)
            thumby.display.update()
            time.sleep(1)
            
            
        #when dealer is done
        
        waitForInput("", line2)
        gamestate = "scoring"
        
        #eval scores to see who won
    if gamestate == "scoring":
        #update all scores
        playerHandScore = valueHand(hand)
        dealerHandScore = valueHand(dealerHand)
        #determine winner
        if playerHandScore == dealerHandScore:
            msg = "Standoff."
        elif didPlayerWin(playerHandScore, dealerHandScore):
            msg = "Player Wins!"
        else:
            msg = "Dealer Wins..."
        #display message to player
        thumby.display.fill(0)
        thumby.display.drawText("P: " + str(playerHandScore) + ", D: " + str(dealerHandScore), 1,line1,1)
        thumby.display.drawText(msg, 1, line2, 1)
        thumby.display.update()    
        #gameRun = False
        waitForInput("", line3)
        if playerHandScore == dealerHandScore:
            pass
        elif didPlayerWin(playerHandScore, dealerHandScore):
            playerWins += 1
            thumby.saveData.setItem("playerWins", playerWins)
        else:
            dealerWins += 1
            thumby.saveData.setItem("dealerWins", dealerWins)
        thumby.saveData.save()    
        gamestate = "shuffle"
    
    if gamestate == "shuffle":
        hand = []
        dealerHand = []
        deck = shuffleDeck()
        print(len(deck))
        gamestate = "deal"
            
        

    
    
