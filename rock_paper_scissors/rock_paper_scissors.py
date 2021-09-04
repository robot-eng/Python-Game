from tkinter import *
import random
from datetime import datetime
curtime = datetime.now().time()
time = curtime.strftime('%H:%M:%S:%p')
def game():
    player_stat = {'wins': 0, 'losses': 0, 'ties': 0}

    def rule(player_shape, AI_shape):
        if player_shape == AI_shape:
            player_stat['ties'] += 1
            return "tied"
        elif (player_shape == 'rock' and AI_shape == 'scissors') or (
                player_shape == 'paper' and AI_shape == 'rock') or (
                player_shape == 'scissors' and AI_shape == 'paper'):
            player_stat['wins'] += 1
            return "player won"
        else:
            player_stat['losses'] += 1
            return "player lost"

    def on_click(e):
        player_shape = e.widget["text"]
        # print(p1_shape)
        AI_shape = random.choice(shapes)
        # print(p2_shape)
        result = rule(player_shape, AI_shape)
        # print(f'result = {result}')
        tv_result.set(f'player:{player_shape} - AI:{AI_shape} -> {result}')
        tv_stat.set(
            f'{player_stat["wins"]} wins, {player_stat["ties"]} ties, {player_stat["losses"]} losses')
    gamer = Tk()
    gamer.title('Rock-Paper-Scissors Game (เกมเป่ายิงฉุบ) \t'+ time)
    gamer.option_add("*Font", "consolas 20")
    shapes = ['rock', 'paper', 'scissors']
    player_shapes = [PhotoImage(file=f'{img}.png') for img in shapes]
    f1 = Frame(gamer)
    f1.grid(row=0, column=0)
    f2 = Frame(gamer)
    f2.grid(row=1, column=0)
    tv_result = StringVar()
    tv_stat = StringVar()

    for i in range(len(player_shapes)):
        w = Button(f1, image=player_shapes[i], text=shapes[i], borderwidth=0)
        w.pack(side=LEFT, padx=15)
        w.bind('<Button-1>', on_click)
    Label(f2, textvariable=tv_result, width=45).pack()
    Label(f2, textvariable=tv_stat, width=45, bg="gold").pack()
    gamer.mainloop()


if __name__ == '__main__':
    # print(rule('rock', 'paper'))
    # print(rule('rock', 'scissors'))
    # print(rule('rock', 'rock'))

    game()


