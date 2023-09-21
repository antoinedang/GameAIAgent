from utils.Agent import GameClient
try:
    while True:
        color_selection = input("Enter the color you wish to play: (0) White (1) Black     ")
        if color_selection not in ["1","0"]:
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

    agent = GameClient(color=int(color_selection), gameID=gameID)

    agent.start()
except KeyboardInterrupt:
    exit()