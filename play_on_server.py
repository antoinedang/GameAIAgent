from utils.GameClasses import Color
from utils.Agent import GameClient
try:
    while True:
        color_selection = input("Enter the color you wish to play: (1) White (2) Black     ")
        if color_selection not in ["1","2"]:
            print("Not a valid selection.")
            continue
        break

    while True:
        try:
            gameID = int(input("Enter the gameID you want to join:     "))
            break
        except:
            print("Not a valid gameID.")
            continue

    if color_selection == 1: color = Color.white
    else: color = Color.black

    agent = GameClient(color=color, gameID=gameID, maxSearchDepth=4, fractionalDepth=0.5, fractionDepthLimit=2)

    agent.start()
except KeyboardInterrupt:
    exit()