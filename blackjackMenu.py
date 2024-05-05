#menu for Blackjack
import thumby
from banner import *
from cards import *

print("menu.py imported")
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

class MENU:
    #menu class can be either a toggle or a list of items
    def __init__(self, title):
        self.title = title
        self.index = 0
        self.items = []
        self.toggle = False
        
    def inc(self):
        self.index += 1
        if self.index > len(self.items)-1:
            self.index = len(self.items)-1
            
    def dec(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
            
    def flipToggle(self):
        self.toggle = not(self.toggle)
        
    def cur(self):
        return self.items[self.index]


#create menu items

def drawHorizontalBars(*rows):
    for row in rows:
        thumby.display.drawLine(0, row, 72, row, 1)
    

def menuRun():
    print("DEBUG: Menu Run opened")

    line1 = 1
    line2 = 11
    line3 = 20
    line4 = 29
    banScroll = 2

    topMenu = MENU("Menu") #view stats here too

    helpMenu = MENU("Help")
    helpMenu.items = [objectiveBan, bustBan, scoringBan]

    dealerMenu = MENU("Rules")
    
    cardMenu = MENU("Card Backs")
    cardMenu.items = ["Weave", "Castle","Robot","Mr. Clip","Cafe","Spade"]
    cardMenu.cards = {
        "Weave": defaultBack,
        "Castle": castle,
        "Robot":robot,
        "Mr. Clip":mrClip,
        "Cafe":cafe,
        "Spade":bigSpade}
    if (thumby.saveData.hasItem("cardBackKey")):
        cardMenu.index = cardMenu.items.index(thumby.saveData.getItem("cardBackKey"))
        
    resetMenu = MENU("Reset Score")
    
    creditsMenu = MENU("Credits")
    
    menuList = [topMenu, helpMenu, dealerMenu, cardMenu, resetMenu, creditsMenu]

    inMenu = True
    page = 0
    sequence = ""
    doubleCheck = 0
    
    eatMash()
    
    while inMenu:
        #check for inputs first
        if thumby.buttonR.justPressed():
            page += 1
            if page >= len(menuList):
                page = 0
            eatMash()
            
        elif thumby.buttonL.justPressed():
            page -= 1
            if page < 0:
                page = len(menuList)-1
            eatMash()
            
        elif thumby.buttonB.justPressed():
            print("DEBUG: menuRun exiting")
            inMenu = False
            
        #draw current title
        thumby.display.fill(0)
        thumby.display.drawText(menuList[page].title, 1, line1, 1)
        drawHorizontalBars(9)
        
        
        #handle each menu
        if menuList[page].title == "Menu":
            thumby.display.drawText("dPad: scroll", 1, line2, 1)
            thumby.display.drawText("(A): toggle", 1, line3, 1)
            thumby.display.drawText("(B): back", 1, line4, 1)
            thumby.display.update()
            
        elif menuList[page].title == "Help":
            currentBanner = helpMenu.cur()
            thumby.display.drawText(currentBanner.text, currentBanner.pos, line2, 1)
            thumby.display.drawText("Scroll (U/D)", 1, line3, 1)
            thumby.display.drawText("FastFwd (A)", 1, line4, 1)
            thumby.display.update()
            currentBanner.step(banScroll)
            
            if thumby.buttonD.justPressed():
                currentBanner.reset()
                helpMenu.inc()
            elif thumby.buttonU.justPressed():
                currentBanner.reset()
                helpMenu.dec()
            elif thumby.buttonA.pressed():
                currentBanner.step(1) #to fast-forward tips
            
        
        elif menuList[page].title == "Rules":
            thumby.display.drawText("Dealer hits", 1, line2, 1)
            thumby.display.drawText("on soft 17?", 1, line3, 1)
            if dealerMenu.toggle:
                thumby.display.drawText("Yes", 1, line4, 1)
            else:
                thumby.display.drawText("No", 1, line4, 1)
                
            if thumby.buttonA.justPressed():
                dealerMenu.flipToggle()
            thumby.display.update()
            
            
        elif menuList[page].title == "Card Backs":
            currentCardTitle = cardMenu.cur()
            currentCardSprite = thumby.Sprite(22, 30, cardMenu.cards[currentCardTitle], 51, 10)
            
            thumby.display.drawText(currentCardTitle, 1, line2, 1)
            thumby.display.drawText("Press", 1, line3, 1)
            thumby.display.drawText("(U/D)", 1, line4, 1)
            thumby.display.drawSprite(currentCardSprite)
            
            if thumby.buttonD.justPressed():
                cardMenu.inc()
                thumby.saveData.setItem("cardBackKey", cardMenu.cur())
                thumby.saveData.save()
            elif thumby.buttonU.justPressed():
                cardMenu.dec()
                thumby.saveData.setItem("cardBackKey", cardMenu.cur())
                thumby.saveData.save()
                
            thumby.display.update()
                
        elif menuList[page].title == "Reset Score":
            thumby.display.drawText("Enter Code:",1,line2,1)
            thumby.display.drawText("DUUDUDDA",1,line3,1)
            thumby.display.drawText(sequence, 1,line4,1)
            thumby.display.update()
            
            #enter code to reset
            if thumby.buttonU.justPressed():
                sequence += "U"
            elif thumby.buttonD.justPressed():
                sequence += "D"
            elif thumby.buttonA.justPressed():
                if sequence == "DUUDUDD":
                    thumby.saveData.setItem("playerWins", 0)
                    thumby.saveData.setItem("dealerWins", 0)
                    thumby.saveData.save()
                    sequence = "Score = 0:0"
                else:
                    sequence = ""
                    print("Sequence broken")

                
        elif menuList[page].title == "Credits":
            thumby.display.drawText(creditsBan.text, creditsBan.pos, line2, 1)
            thumby.display.update()
            creditsBan.step(banScroll)
            if thumby.buttonA.pressed():
                creditsBan.step(1)
        

            
            
#show current options
#if l scroll left
#if r scroll right
#U/D scroll through menu
#press A to toggle
#press B to return

#flow:
#show current page
#get inputs