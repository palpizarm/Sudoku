"""Wrapper functions for Tcl/Game.

This class manager all function to play the game
"""
import tkinter as tk
from tkinter import messagebox
import ast


import Constants as c
from LoadImages import *


class Game:
    __matrix = []
    __buttons_label = ["START GAME", "UNDO", "FINISH GAME", "ERASE GAME", "TOP 10"]
    __buttons = dict().fromkeys(__buttons_label)
    __seleceted_options = ""
    __watchAtivited = ""
    __time = ["0"]*3
    __timeEntry = []

    def __init__(self, pMaster):
        """
        Create and configure the window
        """
        self.__master = pMaster
        loadImages()
        self.__frame = tk.Tk()
        self.__frame.title("SUDOKU GAME")
        self.__frame.geometry("{}x{}+{}+{}".format(c.GAME_WEIGTH, c.GAME_HEIGHT,
                                                    c.FRAME_X, c.FRAME_Y))
        self.__frame.resizable(width=False,height=False)
        self.__options_label = []
        self.__options_bg = []
        self.__options_images = [] 
        self.__getSettingGame()
        self.initComponents()
        self.initListeners()
        self.createTable()

        self.__frame.mainloop()
    

    def __getSettingGame(self):
        """
        Read the file to get the adjusment of the game
        """
        file = open("sudoku2019Setting.dat","r")
        level = int(file.readline())
        fillOption = int(file.readline())
        self.__watchAtivited = int(file.readline())
        if self.__watchAtivited == 3:
            self.__time = file.readline()
            self.__time = ast.literal_eval(self.__time)
        file.close()
        self.__options_label,self.__options_bg,self.__options_images = c.FILL_OPTION[fillOption-1]
        self.__difficulty = tk.Label(self.__frame,
                            fg = "black", text="PRUEBA",
                            font= c.FONT_BUTTON)
        self.__difficulty.place(x=c.DIFFICULTY_X, y=c.DIFFICULTY_Y)
        if level == 1:
            self.__difficulty.config(text = "DIFFICULTY: EASY")
        elif level == 2:
            self.__difficulty.config(text = "DIFFICULTY: NORMAL")
        elif level == 3:
            self.__difficulty.config(text = "DIFFICULTY: HARD")
        # do the function in handler to get the game matrix


    def initComponents(self):
        """
        Create the label, entry and other widgets need
        """
        tk.Label(self.__frame, text = "SUDOKU",
                fg = "white" , bg = "red", borderwidth = 2,
                relief="solid" ,highlightcolor = "black",
                font= c.FONT).pack()
        tk.Label(self.__frame, text = "PLAYER",
                fg = "black",
                font= c.FONT_BUTTON).place(x=c.PLAYER_X, y=c.PLAYER_Y)
        self.playerName = tk.Entry(self.__frame,
                                    bg="white",
                                    fg="black",
                                    width=45)
        self.playerName.place(x=c.PLAYER_NAME_X, y=c.PLAYER_NAME_Y)
        for index in range(9):
            option = tk.Button(self.__frame, text = self.__options_label[index],
                                fg = "black" ,  borderwidth = 2, bg = self.__options_bg[index],
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2, image = self.__options_images[index], 
                                font= c.FONT_BUTTON, command = "")
            if index < 6:
                option.place(x=c.OPTION_X + index*10, y=c.OPTION_Y + (index*45))
            else:
                option.place(x=c.OPTION_X + (10-index)*10, y=c.OPTION_Y + (index*45))
        # To show the watch in the frame if a selceted option is 1 or 3
        print(self.__watchAtivited)
        if self.__watchAtivited == 1 or self.__watchAtivited == 3:
            watch = tk.Canvas(self.__frame, width=200,
                            height=100, bg="white")
            watch.place(x=c.WATCH_X,y=c.WATCH_Y)
            for i in range(3):
                subcontainer = tk.Canvas(watch, 
                                    width=70, height=70,
                                    bg="white")
                subcontainer.grid(row=1,column=i, padx=4, pady=4)
                tk.Label(master=watch, text = c.WACTH_LABEL[i],
                        bg="white", fg="black",
                        font=c.FONT_CONFIGURE).grid(row=0,column=i)
                entry = tk.Entry(master=watch,bg="white", 
                                fg="black", width=4,
                                font=c.FONT_CONFIGURE)
                entry.grid(row=1,column=i)
                entry.bind('<KeyRelease>', self.checkEntriesTimes)
                self.__timeEntry.append(entry)

    def selected(self):
        """
        Call when the buttons options is press
        """
        self.__seleceted_options


    def initListeners(self):
        """
        Create the buttons and other listeners like keyboard entries
        """
        for index in range(len(self.__buttons_label)):
            button = tk.Button(self.__frame, 
                            text= self.__buttons_label[index],
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON)
            button.place(x = c.BUTTON_X + index * 120, y = c.BUTTON_Y)
            self.__buttons[self.__buttons_label[index]] = button
        self.__buttons[self.__buttons_label[0]].config(command = self.startGame)
        self.__buttons[self.__buttons_label[1]].config(command = self.undo)
        self.__buttons[self.__buttons_label[2]].config(command = self.finishGame)
        self.__buttons[self.__buttons_label[3]].config(command = self.erase)
        self.__buttons[self.__buttons_label[4]].config(command = self.top10)
        self.btSaveGame = tk.Button(self.__frame, text= "LOAD GAME",
                                    bg= "brown", fg= "white",
                                    width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                                    command = self.saveGame)
        self.btSaveGame.place(x = c.BTSAVE_X, y = c.BTSAVE_Y)
        self.btLoadGame = tk.Button(self.__frame, text= "SAVE GAME",
                            bg= "brown", fg= "white",
                            width = c.BUTTON_WIDTH, font= c.FONT_BUTTON,
                            command = self.loadGame)
        self.btLoadGame.place(x = c.BTLOAD_X, y = c.BTLOAD_Y)


    def createTable(self):
        """
        Create the visual matrix 9x9
        """
        container = tk.PanedWindow(self.__frame,bg="black")
        container.place(x=c.CONTAINER_X,y=c.CONTAINER_Y)
        for i in range(9):
            filas = []
            for j in range(9):
                square = tk.PanedWindow(container)
                square.grid(row=i, column=j, padx=1, pady=3)
                if j % 3 == 0:
                    square.grid(row=i, column=j, padx=3, pady=1)
                if i % 3 == 0:
                    square.grid(row=i, column=j, padx=1, pady=3)
                field = tk.Label(master=square, text="",
                                bg="white", justify="center",
                                fg="black", font=c.FONT_MATRIX, 
                                width=c.SQUARE_WIDTH, height=c.SQUARE_HEIGHT)
                field.grid()
                filas.append(field)
            self.__matrix.append(filas)


    def updateTable(self):
        """
        look for changes in the logical matrix and update the visual matrix
        """

    
    def loadGame(self):
        """
        Load the game from the file
        """
        file = open('sudoku2019juegoactual.dat', 'r')
    

    def saveGame(self):
        """
        Save the actual game in the file
        """
        file = open('sudoku2019juegoactual.dat', 'w+')
    

    def startGame(self):
        """
        Check and  start the game if is possible
        """
    

    def undo(self):
        """
        Delete the last move
        """
    

    def finishGame(self):
        """
        Exit and delete the game
        """
    
    
    def erase(self):
        """
        Delete all move that the players did
        """

    
    def top10(self):
        """
        show the top10 of each levels
        """
    

    def checkEntriesTimes(self,event):
        """
        check if a entris of hours, minutes and seconds have correct format
        """
        hours = self.__timeEntry[0].get()
        minutes = self.__timeEntry[1].get()
        seconds = self.__timeEntry[2].get()
        if hours != "":
            if not hours.isdigit():
                 self.__timeEntry[0].delete(0,"end")   
            else:
                hours = int(hours)
                if hours < 0 or hours > 4:
                    self.__timeEntry[0].delete(0,"end")
                    messagebox.showerror("Hours Format", "Las horas deben estar entre 0 - 4")
        if minutes != "":
            if not minutes.isdigit():
                self.__timeEntry[1].delete(0,"end")
            else:
                minutes = int(minutes)
                if minutes < 0 or minutes > 59:
                    self.__timeEntry[1].delete(0,"end")
                    messagebox.showerror("Minutes Format", "Las minutos deben estar entre 0 - 59")
        if seconds != "":
            if not seconds.isdigit():
                self.__timeEntry[2].delete(0,"end")
            else:
                seconds = int(seconds)
                if seconds < 0 or seconds > 59:
                    self.__timeEntry[2].delete(0,"end")
                    messagebox.showerror("Seconds Format", "Los segundos deben estar entre 0 - 59")