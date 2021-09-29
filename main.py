from random import shuffle, randint
from tkinter import Tk,Label,Frame,Canvas
from tkinter.font import Font

import threading,time

pieceActivated=None
threads=[]

class Piece():
    def __init__(self,color,num,id,wildcard=False):
        self.color=color
        self.num=num
        self.id=id

        self.tkPiece=None

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

    def defineTkPiece(self,x):
        self.tkPiece=x        
        
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

        self.initializeTk()

        self.gameScreen()

        self.root.mainloop()

    def initializeTk(self):
        self.root=Tk()

        self.fontPrimary="Lexend"
        self.fontSecondary="Roboto"

        self.titleFont=Font(
            family=self.fontPrimary,
            size="36",
            weight="bold"
        )

        self.headerFont=Font(
            family=self.fontSecondary,
            size="24",
        )

        self.captionFont=Font(
            family=self.fontPrimary,
            size="30",
            weight="bold"
        )

        self.bodyFont=Font(
            family=self.fontPrimary,
            size="12"
        )

        self.colors = {
            "dark":"#111111",
            "light":"#fdfdfd",

            "danger":"#EA5D5C",
            "warning":"#ffc107",
            "success":"#4dbd74",

            "primary": {
                "light": "#384461",
                "accent": "#2F3951",
                "normal": "#252D40",
                "dark": "#131720"
            },

            "secondary": {
                "light": "#FEC87C",
                "accent": "#FDBD63",
                "normal": "#FDB34B",
                "dark": "#FC9D17"
            },

            "accent1": {
                "light": "#83D7BB",
                "accent": "#70D1B1",
                "normal": "#5DCBA6",
                "dark": "#3BB98F"
            },

            "accent2": {
                "light": "#EF8476",
                "accent": "#EC7060",
                "normal": "#E95A47",
                "dark": "#E4331B"
            },

            "gray": {
                "100":"#cfcfd7",
                "200":"#c2cfd6",
                "300":"#c1c1cf",
                "400":"#9f9fab",
            }
        }

        self.bgcolor=self.colors["light"]

        self.root.title("Rummikub")
        self.w=self.root.winfo_screenwidth()
        self.h=self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.minsize(self.w,self.h)
        self.root.state("zoomed")

        #self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.configure(bg=self.bgcolor)
        #self.root.attributes("-alpha",0.9)

    def gameScreen(self):
        title=self.createTitle()
        
        board=Frame(self.root,bg=self.bgcolor)
        board.grid(row=1,column=0)

        deck=Frame(board,bg=self.bgcolor)
        deck.grid(row=0,column=0,pady=50)
        
        i=0
        for piece in self.players[0].hand:
            l=self.createPiece(deck,piece)
            piece.defineTkPiece(l)
            l.grid(row=1,column=i,padx=2)
            i+=1

    def createTitle(self):
        title=Label(self.root,text="Rummikub in tkinter", font=self.titleFont,fg=self.colors["primary"]["normal"],bg=self.bgcolor)
        title.grid(row=0,column=0)
        return title

    def createPiece(self,root,piece):        

        def labelHilight(e):
            global pieceActivated
            
            if pieceActivated is not None:
                pieceActivated.config(bg=self.colors["gray"]["100"])
            e.widget.config(bg=self.colors["gray"]["300"])
            pieceActivated=e.widget

        def jokerRotate(j):
            colors=[self.colors["primary"]["light"],self.colors["accent2"]["dark"],self.colors["accent1"]["dark"],self.colors["secondary"]["dark"]]
            i=0
            while True:
                if i >= 4:
                    i=0
                j.config(fg=colors[i])
                i+=1
                time.sleep(0.1)

        joker=False
       
        if piece.color=="B":
            pieceColor=self.colors["primary"]["light"]
        elif piece.color=="R":
             pieceColor=self.colors["accent2"]["dark"]
        elif piece.color=="P":
             pieceColor=self.colors["accent1"]["dark"]
        elif piece.color=="O":
            pieceColor=self.colors["secondary"]["dark"]
        else:
            pieceColor=self.colors["gray"]["400"]
            joker=True
            
        label=Label(
            root,
            font=self.captionFont,
            text=piece.num if piece.num != None else "☺",
            bg=self.colors["gray"]["100"],
            cursor="plus",
            width=3,
            height=2,
            highlightbackground=self.colors["gray"]["200"],
            relief="groove",
            bd=5,
            fg=pieceColor,
        )

        label.bind("<Button-1>",labelHilight)

        if joker:
            t = threading.Thread(target=jokerRotate, args=[label])
            threads.append(t)
            t.start()

        return label
        

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
