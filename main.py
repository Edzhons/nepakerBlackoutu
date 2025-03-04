from tkinter import *
import tkinter.ttk as ttk
from functions import *
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

bg_color = "#FFE8A3"
font = "Georgia"

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

cardBack = PhotoImage(file=resource_path("images/card.png"))

dice_labels = [
    Label(window, image=dice_images[0]),
    Label(window, image=dice_images[1]),
    Label(window, image=dice_images[2]),
    Label(window, image=dice_images[3]),
    Label(window, image=dice_images[4]),
    Label(window, image=dice_images[5]),
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

Img_BtnMenu = PhotoImage(file=resource_path("images/BtnMenu.png")).subsample(5, 5)
Img_BtnAccept = PhotoImage(file=resource_path("images/BtnAccept.png"))
Img_BtnDrink = PhotoImage(file=resource_path("images/BtnDrink.png"))
Img_BtnRoll = PhotoImage(file=resource_path("images/BtnRoll.png"))
Img_Card = PhotoImage(file=resource_path("images/card.png"))
Img_Menu = PhotoImage(file=resource_path("images/menu.png"))
Img_ChallengeBg = PhotoImage(file=resource_path("images/ChallengeBg.png"))
Img_UsedCards = PhotoImage(file=resource_path("images/UsedCards.png"))
Img_shotEmpty = PhotoImage(file=resource_path("images/shotEmpty.png")).subsample(3, 3)

FrameMenu = Frame(window, bg="#FFC7C2", width=315, height=500, highlightbackground="black", highlightthickness=1)

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


BtnMenu = Button(window, image=Img_BtnMenu,
                 command=lambda: toggleMenu(FrameMenu),
                 bg=bg_color, relief=FLAT, bd=0).place(relx=0.01,rely=0.01)


shot_buttons = []
relx, rely = 0.27, 0.18
for i in range(10):
    btn_name = shot_names[i]
    btn = Button(window, text = shot_names[i], image=shot_images[i], compound = TOP,
                 command=lambda btn_name=btn_name: drinkShot(drunkBar, blackoutChanceLabel, respectBar, respectLevelLabel, window,
                                           Img_shotEmpty, shot_buttons, btn_name, BtnAccept, BtnDrink, BtnRoll),
           font=(font, 13), bg=bg_color, relief=FLAT, bd=0, state="disabled")
    btn.place(relx=relx,rely=rely, anchor=S)
    relx += 0.05
    shot_buttons.append(btn)
relx, rely = 0, 0

Label(window, text="Dzēruma līmenis", font=(font, 18, "bold"), bg=bg_color).place(relx=0.93,rely=0.05, anchor=CENTER)
drunkBar = ttk.Progressbar(window, orient=HORIZONTAL, length=200)
drunkBar.place(relx=0.9,rely=0.08)
blackoutChanceLabel = Label(window, text="0%", font=(font, 18, "bold"), bg=bg_color)
blackoutChanceLabel.place(relx=0.94,rely=0.13, anchor=CENTER)

Label(window, text="Respekta līmenis", font=(font, 18, "bold"), bg=bg_color).place(relx=0.93,rely=0.2, anchor=CENTER)
respectBar = ttk.Progressbar(window, orient=HORIZONTAL, length=200)
respectBar.place(relx=0.9, rely=0.23)
respectLevelLabel = Label(window, text="0%", font=(font, 18, "bold"), bg=bg_color)
respectLevelLabel.place(relx=0.94,rely=0.28, anchor=CENTER)

relx, rely = 0.25, 0.4
for i in range(6):
    Label(window, text=f"{i+1}", image=Img_Card, compound=CENTER,
          font=(font, 18, "bold"), fg="white", bg=bg_color).place(relx=relx,rely=rely, anchor=CENTER)
    relx += 0.1
relx, rely = 0, 0

challenge = Label(window, text="Izaicinājums", image=Img_ChallengeBg, compound=CENTER,
      font=(font, 13, "bold"), fg="white", bg=bg_color, wraplength=Img_ChallengeBg.width()-10)
challenge.place(relx=0.5,rely=0.62, anchor=CENTER)

usedChallenge = Label(window, text="", image=Img_UsedCards, compound=CENTER,
      font=(font, 13, "bold"), fg="white", bg=bg_color, wraplength=Img_ChallengeBg.width()-10)
usedChallenge.place(relx=0.927,rely=0.45)

BtnAccept = Button(window, text="Apstiprināt", image=Img_BtnAccept, compound=CENTER,
       command=lambda: AcceptChallenge(drunkBar, blackoutChanceLabel, respectBar, respectLevelLabel, window,
                                       BtnAccept, BtnDrink, BtnRoll),
       font=(font, 13, "bold"), bg=bg_color, relief=FLAT, bd=0, state="disabled")
BtnAccept.place(relx=0.2,rely=0.87, anchor=CENTER)

BtnDrink = Button(window, text="Iedzert", image=Img_BtnDrink, compound=CENTER,
       command=lambda: drink(shot_buttons, Img_shotEmpty, BtnAccept, BtnDrink, BtnRoll),
       font=(font, 13, "bold"), bg=bg_color, relief=FLAT, bd=0, state="disabled")
BtnDrink.place(relx=0.33,rely=0.87, anchor=CENTER)

BtnRoll = Button(window, text="Mest", image=Img_BtnRoll, compound=CENTER,
       command=lambda: roll(dice_labels, text_files, text_filesTemp, challenge, usedChallenge, Img_ChallengeBg,
                            BtnAccept, BtnDrink, BtnRoll),
       font=(font, 13, "bold"), bg=bg_color, relief=FLAT, bd=0)
BtnRoll.place(relx=0.65,rely=0.87, anchor=CENTER)

window.mainloop()
