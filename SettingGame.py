import tkinter as tk
from tkinter import messagebox

import Constants as c


class SettingGame:
    
    __time = []

    def __init__(self, pMaster, pFrame):
        """
        Constructor
        """
        self.__master = pMaster
        self.__frame = pFrame
        self.__frame.title("SETTING GAME")
        self.__frame.geometry("{}x{}+{}+{}".format(c.CONFIGURE_WEIGTH, c.CONFIGURE_HEIGHT,
                                                    c.FRAME_X, c.FRAME_Y))
        self.__frame.resizable(width=False, height=False)
        self.__levelContainer = tk.Canvas(self.__frame)
        self.__watchContainer = tk.Canvas(self.__frame)
        self.__personalizeContainer = tk.Canvas(self.__frame)
        self.__level = tk.IntVar()
        self.__level.set(1)
        self.__watchOption = tk.IntVar()
        self.__watchOption.set(1)
        self.__fillOption = tk.IntVar()
        self.__fillOption.set(1)
        self.initComponents()
        self.createLevelPanel()
        self.createWatchPanel()
        self.createPersonalizePanel()
        self.__frame.protocol('WM_DELETE_WINDOW', self.saveSetting)


    def initComponents(self):
        """
        Create the components that this frame contain
        """
        toolbar = tk.Menu(self.__frame)
        self.__frame.config(menu=toolbar)
        toolbar.add_command(labe="LEVEL", command=self.showLevel)
        toolbar.add_command(labe="WATCH", command=self.showWatch)
        toolbar.add_command(labe="PERSONALIZE", command=self.showPersonalize)
        self.showLevel()


    def showLevel(self):
        """

        """
        self.__frame.geometry("{}x{}".format(300, 300))
        self.__watchContainer.pack_forget()
        self.__personalizeContainer.pack_forget()
        self.__levelContainer.pack()


    def showWatch(self):
        """
        Show the setting of watch
        """
        self.__frame.geometry("{}x{}".format(c.CONFIGURE_WEIGTH, 250))
        self.__levelContainer.pack_forget()
        self.__personalizeContainer.pack_forget()
        self.__watchContainer.pack()
        self.checkWatch()


    def showPersonalize(self):
        """
        show the options of fill cell
        """
        self.__frame.geometry("{}x{}".format(c.CONFIGURE_WEIGTH, c.CONFIGURE_HEIGHT))
        self.__levelContainer.pack_forget()
        self.__watchContainer.pack_forget()
        self.__personalizeContainer.pack()


    def createWatchPanel(self):
        """
        Create the components of the watch view
        """
        self.__watchContainer.config(width=c.CONFIGURE_WEIGTH,
                                    height=c.CONFIGURE_HEIGHT)
        tk.Label(self.__watchContainer, text="Select watch option",
                fg="black", font=c.FONT_BUTTON).place(x=50,y=20)
        tk.Label(self.__watchContainer, text="Set time",
        fg="black", font=c.FONT_BUTTON).place(x=250,y=20)
        watchAtivated = tk.Radiobutton(master=self.__watchContainer, padx=25,
                                text="Activated", variable=self.__watchOption, 
                                font=c.FONT_CONFIGURE, value=1, command=self.checkWatch)
        watchAtivated.place(x=50 , y=50)
        watchDisable = tk.Radiobutton(master=self.__watchContainer, padx=25,
                                text="Disable", variable=self.__watchOption, 
                                font=c.FONT_CONFIGURE, value=2, command=self.checkWatch)
        watchDisable.place(x=50 , y=80)
        timer = tk.Radiobutton(master=self.__watchContainer, padx=25,
                                text="Timer", variable=self.__watchOption,
                                font=c.FONT_CONFIGURE, value=3, command=self.checkWatch)
        timer.place(x=50 , y=110)
        watch = tk.Canvas(self.__watchContainer, width=200,
                        height=100, bg="white")
        watch.place(x=250,y=50)
        for i in range(3):
            subcontainer = tk.Canvas(watch, 
                                width=70, height=70,
                                bg="white")
            subcontainer.grid(row=1,column=i,padx=4, pady=4)
            tk.Label(master=watch, text = c.WACTH_LABEL[i],
                    bg="gray", fg="black",
                    font=c.FONT_CONFIGURE).grid(row=0,column=i)
            entry = tk.Entry(master=watch, state="disabled",
                            bg="white", fg="black",
                            font=c.FONT_CONFIGURE,
                            width=4)
            entry.grid(row=1,column=i)
            entry.bind('<KeyRelease>', self.checkEntriesTimes)
            self.__time.append(entry)
    

    def createLevelPanel(self):
        """
        Create the components of the watch view
        """
        self.__levelContainer.config(width=c.CONFIGURE_WEIGTH,
                                    height=c.CONFIGURE_HEIGHT)
        tk.Label(self.__levelContainer, text="Select dificulty",
                fg="black", font=c.FONT_BUTTON).place(x=20, y=10)
        levelEasy = tk.Radiobutton(master=self.__levelContainer, padx=59,
                                text="Easy", indicatoron = 0,
                                variable=self.__level, bg="white", 
                                font=c.FONT_CONFIGURE, value=1, command = self.checkWatch)
        levelEasy.place(x=50 , y=50)
        levelNormal = tk.Radiobutton(master=self.__levelContainer, padx=50,
                                text="Normal", indicatoron = 0, 
                                variable=self.__level, bg="white",
                                font=c.FONT_CONFIGURE, value=2, command = self.checkWatch)
        levelNormal.place(x=50 , y=80)
        levelHard = tk.Radiobutton(master=self.__levelContainer, padx=59,
                                text="Hard", indicatoron = 0,
                                variable=self.__level, bg="white",
                                font=c.FONT_CONFIGURE, value=3, command = self.checkWatch)
        levelHard.place(x=50 , y=110)
    

    def createPersonalizePanel(self):
        """
        Create the components of the watch view
        """
        self.__personalizeContainer.config(width=c.CONFIGURE_WEIGTH,
                                        height=c.CONFIGURE_HEIGHT)
        tk.Label(self.__personalizeContainer, text="Select an option to fill the game",
                fg="black", font=c.FONT_BUTTON).place(x=20, y=10)
        numbers = tk.Radiobutton(master=self.__personalizeContainer, 
                                text="Numbers", variable=self.__fillOption,
                                font=c.FONT_CONFIGURE, value=1)
        numbers.place(x=50, y=50)
        letters = tk.Radiobutton(master=self.__personalizeContainer, 
                                text="Letters", variable=self.__fillOption,
                                font=c.FONT_CONFIGURE, value=2)
        letters.place(x=150, y=50)
        colors = tk.Radiobutton(master=self.__personalizeContainer, 
                                text="Colors", variable=self.__fillOption,
                                font=c.FONT_CONFIGURE, value=3)
        colors.place(x=250, y=50)
        poolBall = tk.Radiobutton(master=self.__personalizeContainer, 
                                text="Pool ball", variable=self.__fillOption,
                                font=c.FONT_CONFIGURE, value=4)
        poolBall.place(x=350, y=50)
        for index in range(len(c.MATRIX_NUMBERS)):
            option = tk.Button(self.__personalizeContainer, text = c.MATRIX_NUMBERS[index],
                                fg = "black" , bg = "white", borderwidth = 2,
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2, font= c.FONT_BUTTON)
            if index < 6:
                option.place(x= 50 + index*10, y= 100 + (index*45))
            else:
                option.place(x= 50 + (10-index)*10, y= 100 + (index*45))
            option = tk.Button(self.__personalizeContainer, text = c.MATRIX_LETTERS[index],
                                fg = "black" , bg = "white", borderwidth = 2,
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2, font= c.FONT_BUTTON)
            if index < 6:
                option.place(x= 150 + index*10, y= 100 + (index*45))
            else:
                option.place(x= 150 + (10-index)*10, y= 100 + (index*45))
            option = tk.Button(self.__personalizeContainer, text = "",
                                fg = "black" , bg = c.MATRIX_COLORES[index], borderwidth = 2,
                                relief="solid" ,highlightcolor = "black",
                                width = 5, height= 2, font= c.FONT_BUTTON)
            if index < 6:
                option.place(x= 250 + index*10, y= 100 + (index*45))
            else:
                option.place(x= 250 + (10-index)*10, y= 100 + (index*45))
            option = tk.Button(self.__personalizeContainer, image = c.MATRIX_POOL_BALLS[index],
                                fg = "black" , bg = "white", borderwidth = 2,
                                relief="solid" ,highlightcolor = "black",
                                width = 50, height= 50, font= c.FONT_BUTTON)
            if index < 6:
                option.place(x= 350 + index*10, y= 100 + (index*45))
            else:
                option.place(x= 350 + (10-index)*10, y= 100 + (index*45))
        

    def checkWatch(self):
        """
        Check if the watch if active of disable
        """
        for index in range(len(self.__time)):
            self.__time[index].delete(0,"end")
            if self.__watchOption.get() == 1 or self.__watchOption.get() == 2:
                self.__time[index].config(state="disabled")
            else:
                self.__time[index].config(state="normal")
        if self.__level.get() == 1:
            self.__time[1].insert(0,"30")
            self.__time[0].insert(0,"0")
            self.__time[2].insert(0,"0")
        elif self.__level.get() == 2:
            self.__time[0].insert(0,"1")
            self.__time[1].insert(0,"0")
            self.__time[2].insert(0,"0")
        elif self.__level.get() == 3:
            self.__time[0].insert(0,"2")
            self.__time[1].insert(0,"0")
            self.__time[2].insert(0,"0")


    def checkEntriesTimes(self,event):
        """
        check if a entris of hours, minutes and seconds have correct format
        """
        hours = self.__time[0].get()
        minutes = self.__time[1].get()
        seconds = self.__time[2].get()
        if hours != "":
            if not hours.isdigit():
                 self.__time[0].delete(0,"end")   
            else:
                hours = int(hours)
                if hours < 0 or hours > 4:
                    self.__time[0].delete(0,"end")
                    messagebox.showerror("Hours Format", "Las horas deben estar entre 0 - 4")
        if minutes != "":
            if not minutes.isdigit():
                self.__time[1].delete(0,"end")
            else:
                minutes = int(minutes)
                if minutes < 0 or minutes > 59:
                    self.__time[1].delete(0,"end")
                    messagebox.showerror("Minutes Format", "Las minutos deben estar entre 0 - 59")
        if seconds != "":
            if not seconds.isdigit():
                self.__time[2].delete(0,"end")
            else:
                seconds = int(seconds)
                if seconds < 0 or seconds > 59:
                    self.__time[2].delete(0,"end")
                    messagebox.showerror("Seconds Format", "Los segundos deben estar entre 0 - 59")


    def saveSetting(self):
        """
        Save the adjusment of the game
        """
        file = open("sudoku2019Setting.dat","w+")
        file.write(str(self.__level.get()) + "\n")
        file.write(str((self.__fillOption.get())) + "\n")
        file.write(str((self.__watchOption.get())) + "\n")
        hours = self.__time[0].get()
        minutes = self.__time[1].get()
        seconds = self.__time[2].get()
        if hours == "":
            hours = '0'
        if minutes == '':
            minutes = '0'
        if seconds == '':
            seconds = '0'
        file.write("["+str(hours)+"," + str(minutes)+ ","+ str(seconds)+"]")
        file.close()
        self.__frame.withdraw()
        self.__master.focus_force()
        self.__master.grab_set()
        self.__master.deiconify()