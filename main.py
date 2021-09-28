from random import shuffle, randint
import tkinter

class Piece():
    def __init__(self,color,num,id,wildcard=False):
        self.color=color
        self.num=num
        self.id=id

        if wildcard:
            self.wildCard=True
        else:
            self.wildCard=False
        
    def __repr__(self):
        return f"<Piece {self.id} {self.getCardCode()}>\n"
    
    def getCardCode(self):
        if self.wildCard:
            return f"X:00"

        num="0" if self.num > 9 else ""
        num=f"{num}{self.num}"

        return f"{self.color}:{self.num}"

    def getCardUniqueID(self):
        return self.id
        
class Player():
    def __init__(self,name=""):
        self.hand=[]
        self.name=name

    def draw(self,cards):
        for card in cards:
            self.hand.append(card)

class Board():
    def __init__(self):
        self.sets=[]
        self.changedSets=[]

class Game():
    def __init__(self,players=[]):
        self.drawPile=self.getStartingDeck()
        shuffle(self.drawPile)

        self.board=Board()

        self.players=players

        for player in players:
            player.draw(self.drawHand())

    def drawHand(self):
        hand=[]
        for i in range(14):
            x=randint(0,len(self.drawPile)-1)
            hand.append(self.drawPile[x])
            self.drawPile.pop(x)
        return hand

    def getStartingDeck(self):
        colors=["B","R","P","O"]
        deck=[]
        colorInt=0
        step=1
        id_=0

        for i in range(2):
            color=colors[colorInt]

            for i in range(52):
                deck.append(Piece(color,step,id_))
                step+=1
                id_+=1

                if i==51:
                    continue

                if step>13:
                    colorInt+=1
                    step=1
                    color=colors[colorInt]
                    
            colorInt=0
            step=1

        deck.append(Piece(None,None,id_,wildcard=True))
        deck.append(Piece(None,None,id_+1,wildcard=True))
        
        return deck  

player1=Player()
player2=Player()

game=Game(players=[player1,player2])
