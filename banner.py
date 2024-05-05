#banner class stores strings that are scrolled across screen
print("banner.py imported")
fontWidth = 6
screenWidth = 72
framerateBuffer = 12 #if buffer == fps, this delays appearance by 1 second

class banner:
    def __init__(self, text):
        self.text = text
        self.textLen = len(self.text) * fontWidth
        self.pos = screenWidth + framerateBuffer
    
    def reset(self):
        self.pos = screenWidth + framerateBuffer
        
    def step(self, space):
        self.pos = self.pos - space
        if self.pos < -self.textLen:
            self.pos = screenWidth
            
    def newText(self, newTxt):
        self.text = newTxt
        self.textLen = len(self.text) * fontWidth
        self.pos = screenWidth + framerateBuffer


#banner was made for scrolling long text strings. Here's some for Blackjack.

# Gameplay Banners
continueString = "Press A to continue."
continueBan = banner(continueString)

# Settings Menu Banners
objectiveBan = banner("Try to get your cards to equal 21.")
bustBan = banner("If you go over 21, that's a bust!")
scoringBan = banner("Face cards are worth 10. Aces are worth 11 or 1.")

h17Ban = banner("Dealer must hit on soft 17?")
creditsBan = banner("By Codey for Keili <3")
