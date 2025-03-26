from tkinter import *
import tkinter.ttk as ttk
import ctypes, random, os, sys, shutil, subprocess

ctypes.windll.shcore.SetProcessDpiAwareness(1)

bg_color = "#460B0C"
font = "Georgia"

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # Running as a bundled executable
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller unpacks files
    else:
        base_path = os.path.abspath(".")  # Running as a script

    return os.path.join(base_path, relative_path)

FrameMenu_visible = False
def toggleMenu():
    global FrameMenu_visible

    if FrameMenu_visible:
        FrameMenu.place_forget()
    else:
        FrameMenu.place(relx=0.01,rely=0.15)

    FrameMenu_visible = not FrameMenu_visible

def showMenu():
    for widget in FrameMenu.winfo_children():
        widget.place_forget()

    BtnRules = Button(FrameMenu, text="Noteikumi", command=showRules,
                    font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
    BtnRules.place(relx=0.5, rely=0.2, anchor=CENTER, relwidth=0.9)

    BtnReset = Button(FrameMenu, text="Jauna spēle", command=resetGame, font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
    BtnReset.place(relx=0.5, rely=0.4, anchor=CENTER, relwidth=0.9)

    BtnAuthors = Button(FrameMenu, text="Autori", command=showAuthors,
                        font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
    BtnAuthors.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.9)

    BtnQuit = Button(FrameMenu, text="Iziet", command=quitGame, font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
    BtnQuit.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.9)

def showRules():
    FrameGame.place_forget()
    FrameRules.place(relx=0, rely=0, relwidth=1, relheight=1)

def showAuthors():
    for widget in FrameMenu.winfo_children():
        widget.place_forget()

    AuthorsLabel = Label(FrameMenu, text="""SPĒLES AUTORI\n
Nensija Betija Aukmane - Vizuālais noformējums FIGMA
Edžus Krūmiņš - Dizaina implementācija, spēles izstrāde""",
                        font=(font, 15), fg="white",bg="#7B5B48", wraplength=300)
    AuthorsLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    BtnBack = Button(FrameMenu, text="Atpakaļ", command=showMenu, font=(font, 18))
    BtnBack.place(relx=0.5, rely=0.9, anchor=CENTER)

lastChallenge = ""
def roll():
    global lastChallenge

    rndDigit = random.randint(1,6)

    # Padara iepriekšējo dice neredzamu
    for dice in dice_labels:
        dice.place_forget()

    dice_labels[rndDigit - 1].place(relx=0.75, rely=0.8)

    #Pārvieto iepriekšējo challenge uz usedCards
    if not lastChallenge == "":
        usedChallenge.config(text=lastChallenge, image=Img_ChallengeBg)

    # Nolasa challenges no attiecīgā faila
    file_name = text_filesTemp[rndDigit - 1]
    with open (file_name, encoding="utf-8") as file:
        lines = file.readlines() # Visas teksta faila rindas ieliek listā

        if not lines:
            print(f"Failā {file_name} beidzās izaicinājumu, kārtis tiek iemaisītas atpakaļ.")

            shutil.copy(text_files[rndDigit - 1], file_name)
            with open (file_name, encoding="utf-8") as file:
                lines = file.readlines() # Visas teksta faila rindas ieliek listā

        content = random.choice(lines).strip() # Randomā izvēlas vienu no rindām
        lines.remove(content + "\n") if (content + "\n") in lines else lines.remove(content)
        lastChallenge = content

        with open(file_name, "w", encoding="utf-8") as file:
            file.writelines(lines)

        challenge.config(text=content)
    
    # Pogas "Apstiprināt" un "Iedzert" ir enabled, poga "Mest" ir disabled
    BtnAccept.config(state="normal")
    BtnDrink.config(state="normal")
    BtnRoll.config(state="disabled")

def drink():
    # Shot pogas ir enabled, pārējais ir disabled.
    for btn in shot_buttons:
        if btn["image"] != str(Img_shotEmpty):
            btn.config(state="normal")

    BtnAccept.config(state="disabled")
    BtnDrink.config(state="disabled")
    BtnRoll.config(state="disabled")

blackoutChance = 0
respectLevel = 0
drinks = 0
def drinkShot(btn_name):
    global blackoutChance, respectLevel, drinks
    drinks += 1

    for btn in shot_buttons:
        if btn.cget("text") == btn_name:  # Pārbauda, vai pogas teksts sakrīt
            btn.config(image=Img_shotEmpty)  # Pogas image ir "shotEmpty"

    for btn in shot_buttons:
        btn.config(state="disabled")

    BtnRoll.config(state="normal")

    if (respectLevel - 5) >= 0:
        respectLevel -= 5
        
    if blackoutChance != 45:
        blackoutChance += 5
    else:
        blackoutChance = 100

    if random.randint(1,100) <= blackoutChance:
        gameOver("loss")

    drunkBar["value"] = blackoutChance*2
    blackoutChanceLabel.config(text=f"{blackoutChance*2}%")

    respectBar["value"] = respectLevel
    respectLevelLabel.config(text=f"{respectLevel}%")

questionsAnswered = 0
def AcceptChallenge():
    global respectLevel, questionsAnswered
    questionsAnswered += 1

    if (respectLevel + 10) <= 100:
        respectLevel += 10
    else:
        respectLevel = 100

    if respectLevel == 100:
        gameOver("win")

    respectBar["value"] = respectLevel
    respectLevelLabel.config(text=f"{respectLevel}%")
    
    BtnAccept.config(state="disabled")
    BtnDrink.config(state="disabled")
    BtnRoll.config(state="normal")

def gameOver(type):
    global GAME_OVER

    FrameGameOver = Frame(window, bg=bg_color)
    FrameGameOver.pack(expand=True, fill=BOTH)

    if type == "loss":
        GAME_OVER = Label(FrameGameOver, text="TU ZAUDĒJI! \nSpēle beigusies!", font=("Consolas", 50), fg="#ECB5B5", bg=bg_color)
        GAME_OVER.place(relx=0.5, rely=0.6, anchor=CENTER)
        Label(FrameGameOver, image=ImgShotLoss, bg=bg_color).place(relx=0.5, rely=0.3, anchor=CENTER)
    elif type == "win":
        GAME_OVER = Label(FrameGameOver, text="TU UZVARĒJI! \nSpēle beigusies!", font=("Consolas", 50), fg="#ECB5B5", bg=bg_color)
        GAME_OVER.place(relx=0.5, rely=0.6, anchor=CENTER)
        Label(FrameGameOver, image=ImgShotWin, bg=bg_color).place(relx=0.5, rely=0.3, anchor=CENTER)

    Button(FrameGameOver, text="Iziet", command=quitGame,
            font=("Consolas", 30), fg="#ECB5B5", bg=bg_color).pack(side=BOTTOM)
    
    Button(FrameGameOver, text="Tava statistika", command=getStatistics,
            font=("Consolas", 30), fg="#ECB5B5", bg=bg_color).pack(side=BOTTOM)
    
    Button(FrameGameOver, text="Jauna spēle", command=resetGame,
            font=("Consolas", 30), fg="#ECB5B5", bg=bg_color).pack(side=BOTTOM)

def resetGame():
    try:
        subprocess.Popen([sys.executable] + sys.argv)
    except Exception as e:
        print(f"Failed to restart: {e}")
    sys.exit()

def getStatistics():
    global GAME_OVER

    GAME_OVER.config(text=f"""
Tu izdzēri {drinks} šotus un izvēlējies atbildēt uz {questionsAnswered} jautājumiem!
Tu biji {blackoutChance*2}% piedzēries!
Tavs Respekta līmenis: {respectLevel}%!""", font=("Consolas", 30))

def quitGame():
    window.destroy()

def startGame():
    FrameMainMenu.place_forget()
    FrameGame.place(relx=0, rely=0, relwidth=1, relheight=1)

def returnToMenu():
    FrameGame.place_forget()
    FrameMainMenu.place(relx=0, rely=0, relwidth=1, relheight=1)

def backToGame():
    FrameRules.place_forget()
    FrameGame.place(relx=0, rely=0, relwidth=1, relheight=1)

window = Tk()
window.attributes("-fullscreen", True)
window.configure(background=bg_color)

dice_images = [
    PhotoImage(file=resource_path("images/dice1.png")).subsample(2, 2),
    PhotoImage(file=resource_path("images/dice2.png")).subsample(2, 2),
    PhotoImage(file=resource_path("images/dice3.png")).subsample(2, 2),
    PhotoImage(file=resource_path("images/dice4.png")).subsample(2, 2),
    PhotoImage(file=resource_path("images/dice5.png")).subsample(2, 2),
    PhotoImage(file=resource_path("images/dice6.png")).subsample(2, 2),
]

shot_images = [
    PhotoImage(file=resource_path("images/BtnShot1.png")),
    PhotoImage(file=resource_path("images/BtnShot2.png")),
    PhotoImage(file=resource_path("images/BtnShot3.png")),
    PhotoImage(file=resource_path("images/BtnShot4_7.png")),
    PhotoImage(file=resource_path("images/BtnShot5.png")),
    PhotoImage(file=resource_path("images/BtnShot6.png")),
    PhotoImage(file=resource_path("images/BtnShot4_7.png")),
    PhotoImage(file=resource_path("images/BtnShot8.png")),
    PhotoImage(file=resource_path("images/BtnShot9.png")),
    PhotoImage(file=resource_path("images/BtnShot10.png")),
]

shot_names = [
    "\nUzlējums",
    "\nBrendijs",
    "\nŠņabis",
    "\nRums",
    "\nViskijs",
    "\n  Tekila",
    "\nKonjaks",
    "\nLiķieris",
    "\nDžins",
    "\nNāves ļuļļa",
]

text_files = [resource_path("challenges/lvl1.txt"),
            resource_path("challenges/lvl2.txt"),
            resource_path("challenges/lvl3.txt"),
            resource_path("challenges/lvl4.txt"), 
            resource_path("challenges/lvl5.txt"),
            resource_path("challenges/lvl6.txt")]

text_filesTemp = [shutil.copy(text_files[0], resource_path("challenges/lvl1Temp.txt")),
            shutil.copy(text_files[1], resource_path("challenges/lvl2Temp.txt")),
            shutil.copy(text_files[2], resource_path("challenges/lvl3Temp.txt")),
            shutil.copy(text_files[3], resource_path("challenges/lvl4Temp.txt")),
            shutil.copy(text_files[4], resource_path("challenges/lvl5Temp.txt")),
            shutil.copy(text_files[5], resource_path("challenges/lvl6Temp.txt"))]

Img_BtnMenu = PhotoImage(file=resource_path("images/btnMenu.png"))
Img_BtnAcceptDrink = PhotoImage(file=resource_path("images/BtnAcceptDrink.png"))
Img_BtnRoll = PhotoImage(file=resource_path("images/BtnRoll.png"))
Img_Card = PhotoImage(file=resource_path("images/card.png"))
Img_ChallengeBg = PhotoImage(file=resource_path("images/ChallengeBg.png"))
Img_UsedCards = PhotoImage(file=resource_path("images/usedCards.png"))
Img_shotEmpty = PhotoImage(file=resource_path("images/shotEmpty.png")).subsample(3, 3)
ImgShotLoss = PhotoImage(file=resource_path("images/shotLoss.png"))
ImgShotWin = PhotoImage(file=resource_path("images/shotWin.png"))

# --- MAIN MENU FRAME ---
FrameMainMenu = Frame(window, bg=bg_color)
FrameMainMenu.place(relx=0, rely=0, relwidth=1, relheight=1)

Label(FrameMainMenu, text="NEPAĶER BLACKOUTU", font=(font, 50, "bold"), fg="#FFD700", bg=bg_color).place(relx=0.5, rely=0.3, anchor=CENTER)

BtnStart = Button(FrameMainMenu, text="SĀKT SPĒLI", command=startGame, font=(font, 20, "bold"), bg="#FFC7C2", fg="black", width=15)
BtnStart.place(relx=0.5, rely=0.5, anchor=CENTER)

BtnQuit = Button(FrameMainMenu, text="IZIET", command=quitGame, font=(font, 20, "bold"), bg="#FFC7C2", fg="black", width=15)
BtnQuit.place(relx=0.5, rely=0.6, anchor=CENTER)

Label(FrameMainMenu, text="Edžus Krūmiņš\nNensija Betija Aukmane", font=(font, 15, "bold"), fg="#FFD700", bg=bg_color,
                                                                    justify="right",).place(relx=0.9, rely=0.95, anchor=CENTER)

# --- RULES FRAME ---
FrameRules = Frame(window, bg=bg_color)

rules = """
Šī ir dzeršanas spēle, kurā ir tikai 2 izvēles - atbildi uz jautājumu vai arī iedzer!

6 kāršu kavas atspoguļo 6 grūtības līmeņus jautājumiem.
Respektīvi, jautājumi no 1. kavas ir vieglāki, nekā jautājumi no 6. kavas.

Lai sāktu spēli, spied pogu "Mest". Tad tev ir izvēle - atbildēt uz jautājumu ("Apstiprināt") vai arī izvēlēties uz jautājumu neatbildēt ("Iedzert").

Katru reizi, kad atbildi uz uzdoto jautājumu, tavs respekta līmenis palielinās par 10%.
Kad esi sasniedzis 100% respekta līmeni, esi spēli uzvarējis.

Katru reizi, kad izvēlies "Iedzert", tev tiek dota iespēja izvēlēties, kuru no šotiem dzersi.
Iedzerot šotu, respekta līmenis samazinās par 5%. Tāpat, tev palielinās "Dzēruma līmenis".
Ar katru nākamo šotu iespēja "Paķert Blackoutu", jeb zaudēt spēli palielinās par 5%. Tomēr, ja izdzer visus 10 šotus, tad automātiski esi zaudējis.

Pēc spēles vari apskatīt savu statistiku: Izdzertos šotus, atbildēto jautājumu skaitu, dzēruma un respekta līmeni."""
Label(FrameRules, text=rules, font=(font, 20, "bold"), fg="#ECB5B5", bg=bg_color, wraplength=1700).place(relx=0.5, rely=0.5, anchor=CENTER)

BtnBack = Button(FrameRules, text="ATPAKAĻ", command=backToGame, font=(font, 20, "bold"), bg="#FFC7C2", fg="black", width=15)
BtnBack.place(relx=0.5, rely=0.9, anchor=CENTER)

# --- GAME FRAME (Initially Hidden) ---
FrameGame = Frame(window, bg=bg_color)
FrameMenu = Frame(FrameGame, bg="#7B5B48", width=300, height=500, highlightbackground="black", highlightthickness=1)

dice_labels = [
    Label(FrameGame, image=dice_images[0], bg=bg_color),
    Label(FrameGame, image=dice_images[1], bg=bg_color),
    Label(FrameGame, image=dice_images[2], bg=bg_color),
    Label(FrameGame, image=dice_images[3], bg=bg_color),
    Label(FrameGame, image=dice_images[4], bg=bg_color),
    Label(FrameGame, image=dice_images[5], bg=bg_color)
]

BtnRules = Button(FrameMenu, text="Noteikumi", command=showRules,
                font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
BtnRules.place(relx=0.5, rely=0.2, anchor=CENTER, relwidth=0.9)

BtnReset = Button(FrameMenu, text="Jauna spēle", command=resetGame, font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
BtnReset.place(relx=0.5, rely=0.4, anchor=CENTER, relwidth=0.9)

BtnAuthors = Button(FrameMenu, text="Autori", command=showAuthors,
                    font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
BtnAuthors.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.9)

BtnQuit = Button(FrameMenu, text="Iziet", command=quitGame, font=(font, 18), fg="white", bg="#460B0C", compound=CENTER)
BtnQuit.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.9)


BtnMenu = Button(FrameGame, image=Img_BtnMenu,
                command=toggleMenu,
                bg=bg_color, relief=FLAT, bd=0).place(relx=0.01,rely=0.01)


shot_buttons = []
relx, rely = 0.27, 0.18
for i in range(10):
    btn_name = shot_names[i]
    btn = Button(FrameGame, text = shot_names[i], image=shot_images[i], fg="#ECB5B5", compound = TOP,
                command=lambda btn_name=btn_name: drinkShot(btn_name),
        font=(font, 13), bg=bg_color, relief=FLAT, bd=0, state="disabled")
    btn.place(relx=relx,rely=rely, anchor=S)
    relx += 0.05
    shot_buttons.append(btn)
relx, rely = 0, 0

Label(FrameGame, text="Dzēruma līmenis", font=(font, 18, "bold"), fg="#ECB5B5", bg=bg_color).place(relx=0.93,rely=0.05, anchor=CENTER)
drunkBar = ttk.Progressbar(FrameGame, orient=HORIZONTAL, length=200)
drunkBar.place(relx=0.9,rely=0.08)
blackoutChanceLabel = Label(FrameGame, text="0%", font=(font, 18, "bold"), fg="#ECB5B5", bg=bg_color)
blackoutChanceLabel.place(relx=0.94,rely=0.13, anchor=CENTER)

Label(FrameGame, text="Respekta līmenis", font=(font, 18, "bold"), fg="#ECB5B5", bg=bg_color).place(relx=0.93,rely=0.2, anchor=CENTER)
respectBar = ttk.Progressbar(FrameGame, orient=HORIZONTAL, length=200)
respectBar.place(relx=0.9, rely=0.23)
respectLevelLabel = Label(FrameGame, text="0%", font=(font, 18, "bold"), fg="#ECB5B5", bg=bg_color)
respectLevelLabel.place(relx=0.94,rely=0.28, anchor=CENTER)

relx, rely = 0.25, 0.4
texts=[
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI"
]
for i in range(6):
    Label(FrameGame, text=texts[i], image=Img_Card, compound=CENTER,
        font=(font, 18, "bold"), fg="#ECB5B5", bg=bg_color).place(relx=relx,rely=rely, anchor=CENTER)
    relx += 0.1
relx, rely = 0, 0

challenge = Label(FrameGame, text="Izaicinājums", image=Img_ChallengeBg, compound=CENTER,
    font=(font, 13, "bold"), fg="#ECB5B5", bg=bg_color, wraplength=Img_ChallengeBg.width()-10)
challenge.place(relx=0.5,rely=0.62, anchor=CENTER)

usedChallenge = Label(FrameGame, text="", image=Img_UsedCards, compound=CENTER,
    font=(font, 13, "bold"), fg="#ECB5B5", bg=bg_color, wraplength=Img_ChallengeBg.width()-10)
usedChallenge.place(relx=0.927,rely=0.45)

BtnAccept = Button(FrameGame, text="Atbildēt", image=Img_BtnAcceptDrink, compound=CENTER,
    command=AcceptChallenge,
    font=(font, 13, "bold"), bg=bg_color, fg="#ECB5B5", relief=FLAT, bd=0, state="disabled")
BtnAccept.place(relx=0.2,rely=0.87, anchor=CENTER)

BtnDrink = Button(FrameGame, text="Iedzert", image=Img_BtnAcceptDrink, compound=CENTER,
    command=drink,
    font=(font, 13, "bold"), bg=bg_color, fg="#ECB5B5", relief=FLAT, bd=0, state="disabled")
BtnDrink.place(relx=0.33,rely=0.87, anchor=CENTER)

BtnRoll = Button(FrameGame, text="Mest", image=Img_BtnRoll, compound=CENTER,
    command=roll,
    font=(font, 13, "bold"), bg=bg_color, fg="#ECB5B5", relief=FLAT, bd=0)
BtnRoll.place(relx=0.65,rely=0.87, anchor=CENTER)

window.mainloop()