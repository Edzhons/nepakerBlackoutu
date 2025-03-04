from tkinter import *
import random
import os
import sys
import shutil

font = "Georgia"

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # Running as a bundled executable
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller unpacks files
    else:
        base_path = os.path.abspath(".")  # Running as a script

    return os.path.join(base_path, relative_path)

FrameMenu_visible = False
def toggleMenu(FrameMenu):
    global FrameMenu_visible

    if FrameMenu_visible:
        FrameMenu.place_forget()
    else:
        FrameMenu.place(relx=0.01,rely=0.15)

    FrameMenu_visible = not FrameMenu_visible

def showMenu(FrameMenu, window):
    for widget in FrameMenu.winfo_children():
        widget.place_forget()

    BtnRules = Button(FrameMenu, text="Noteikumi", command=lambda: showRules(FrameMenu, window),
                    font=(font, 18), compound=CENTER)
    BtnRules.place(relx=0.5, rely=0.2, anchor=CENTER, relwidth=0.9)

    BtnReset = Button(FrameMenu, text="Jauna spēle", command=resetGame, font=(font, 18), compound=CENTER)
    BtnReset.place(relx=0.5, rely=0.4, anchor=CENTER, relwidth=0.9)

    BtnAuthors = Button(FrameMenu, text="Autori", command=lambda: showAuthors(FrameMenu, window),
                        font=(font, 18), compound=CENTER)
    BtnAuthors.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.9)

    BtnQuit = Button(FrameMenu, text="Iziet", command=lambda: quitGame(window), font=(font, 18), compound=CENTER)
    BtnQuit.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.9)

def showRules(FrameMenu, window):
    for widget in FrameMenu.winfo_children():
        widget.place_forget()

    rulesLabel = Label(FrameMenu, text="Šeit ir spēles noteikumi:\n1. ...\n2. ...\n3. ...",
                        font=(font, 15), bg="#FFC7C2", wraplength=300)
    rulesLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    BtnBack = Button(FrameMenu, text="Atpakaļ", command=lambda: showMenu(FrameMenu, window), font=(font, 18))
    BtnBack.place(relx=0.5, rely=0.8, anchor=CENTER)


def showAuthors(FrameMenu, window):
    for widget in FrameMenu.winfo_children():
        widget.place_forget()

    AuthorsLabel = Label(FrameMenu, text="""SPĒLES AUTORI\n
Nensija Betija Aukmane - Vizuālais noformējums FIGMA
Edžus Krūmiņš - Dizaina implementācija, spēles izstrāde""",
                        font=(font, 15), bg="#FFC7C2", wraplength=300)
    AuthorsLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    BtnBack = Button(FrameMenu, text="Atpakaļ", command=lambda: showMenu(FrameMenu, window), font=(font, 18))
    BtnBack.place(relx=0.5, rely=0.9, anchor=CENTER)

lastChallenge = ""
def roll(dice_labels, text_files, text_filesTemp, challenge, usedChallenge, Img_ChallengeBg,
         BtnAccept, BtnDrink, BtnRoll):
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

def drink(shot_buttons, Img_shotEmpty, BtnAccept, BtnDrink, BtnRoll):
    # Shot pogas ir enabled, pārējais ir disabled.
    for btn in shot_buttons:
        if btn["image"] != str(Img_shotEmpty):
            btn.config(state="normal")

    BtnAccept.config(state="disabled")
    BtnDrink.config(state="disabled")
    BtnRoll.config(state="disabled")

blackoutChance = 0
respectLevel = 0
def drinkShot(drunkBar, blackoutChanceLabel, respectBar, respectLevelLabel, window,
              Img_shotEmpty, shot_buttons, btn_name, BtnAccept, BtnDrink, BtnRoll):
    for btn in shot_buttons:
        if btn.cget("text") == btn_name:  # Pārbauda, vai pogas teksts sakrīt
            btn.config(image=Img_shotEmpty)  # Pogas image ir "shotEmpty"

    for btn in shot_buttons:
        btn.config(state="disabled")

    BtnRoll.config(state="normal")

    global blackoutChance
    global respectLevel

    if (respectLevel - 5) >= 0:
        respectLevel -= 5
        
    if blackoutChance != 45:
        blackoutChance += 5
    else:
        blackoutChance = 100

    if random.randint(1,100) <= blackoutChance:
        gameOver("loss", window)

    drunkBar["value"] = blackoutChance*2
    blackoutChanceLabel.config(text=f"{blackoutChance*2}%")

    respectBar["value"] = respectLevel
    respectLevelLabel.config(text=f"{respectLevel}%")
def AcceptChallenge(drunkBar, blackoutChanceLabel, respectBar, respectLevelLabel, window, BtnAccept, BtnDrink, BtnRoll):
    global blackoutChance
    global respectLevel

    if (respectLevel + 10) <= 100:
        respectLevel += 10
    else:
        respectLevel = 100

    if (blackoutChance - 5) >= 0:
        blackoutChance -= 5

    if respectLevel == 100:
        gameOver("win", window)

    drunkBar["value"] = blackoutChance*2
    blackoutChanceLabel.config(text=f"{blackoutChance*2}%")

    respectBar["value"] = respectLevel
    respectLevelLabel.config(text=f"{respectLevel}%")
    
    BtnAccept.config(state="disabled")
    BtnDrink.config(state="disabled")
    BtnRoll.config(state="normal")

def gameOver(type, window):
    FrameGameOver = Frame(window, bg="black")
    FrameGameOver.pack(expand=True, fill=BOTH)

    if type == "loss":
        GAME_OVER = Label(FrameGameOver, text="TU ZAUDĒJI! \nSpēle beigusies!", font=("Consolas", 120), fg="gold", bg="black")
        GAME_OVER.place(relx=0.5, rely=0.4, anchor=CENTER)
    elif type == "win":
        GAME_OVER = Label(FrameGameOver, text="TU UZVARĒJI! \nSpēle beigusies!", font=("Consolas", 120), fg="gold", bg="black")
        GAME_OVER.place(relx=0.5, rely=0.4, anchor=CENTER)

    Button(FrameGameOver, text="Iziet", command=lambda: quitGame(window),
           font=("Consolas", 30), fg="white", bg="black").pack(side=BOTTOM)
    
    Button(FrameGameOver, text="Tava statistika", font=("Consolas", 30), fg="white", bg="black").pack(side=BOTTOM)
    
    Button(FrameGameOver, text="Jauna spēle", command=resetGame,
        font=("Consolas", 30), fg="white", bg="black").pack(side=BOTTOM)

def resetGame():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def getStatistics():
    pass

def quitGame(window):
    window.destroy()
