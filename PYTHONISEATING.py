import tkinter as tk
from tkinter import colorchooser
import random

cell_size=20
height=400
width=400
HIGH_SCORE_FILE="high_score.txt"

game={"snake":[(100, 100)],
    "direction":"Down",
    "food":None,
    "snake_color":"green",
    "current_score":0,
    "high_score":0,
    "game_running":False,
    "game_canvas":None,
    "current_score_label":None,
    "highest_score_label":None}

def PythonIsEating():
    start_frame.pack_forget()
    frame1.pack(fill="both",expand=True)
    score_frame=tk.Frame(frame1,bg="white")
    score_frame.pack(fill="x")
    highest_score_label=tk.Label(score_frame, text=f"Highest score:{game['high_score']}",bg="white")
    highest_score_label.pack(side="left", padx=10)
    current_score_label=tk.Label(score_frame,text=f"Current Score:{game['current_score']}",bg="white")
    current_score_label.pack(side="left")
    button_frame=tk.Frame(score_frame,bg="white")
    button_frame.pack(side="right",padx=10)
    tk.Button(button_frame,text="Change Color",command=change_color).pack(side="left",padx=2)
    tk.Button(button_frame,text="Pause",command=pause_game).pack(side="left",padx=2)
    tk.Button(button_frame,text="Restart",command=restart_game).pack(side="left",padx=2)
    game_canvas=tk.Canvas(frame1, bg="black", height=height, width=width)
    game_canvas.pack()
    game["current_score_label"]=current_score_label
    game["highest_score_label"]=highest_score_label
    game["game_canvas"]=game_canvas
    root.bind("<KeyPress>",change_direction)
    start_game()

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE,"r") as f:
            game["high_score"]=int(f.read())
    except (FileNotFoundError,ValueError):
        game["high_score"]=0

def update_high_score():
    game["high_score"]=game["current_score"]
    try:
        with open(HIGH_SCORE_FILE,"w") as f:
            f.write(str(game["high_score"]))
    except Exception as e:
        print(f"Error saving high score: {e}")
load_high_score()

def change_color():
    color=colorchooser.askcolor(title="Pick a Color")
    if color[1]:
        game["snake_color"]=color[1]

def pause_game():
    game["game_running"]=not game["game_running"]
    if game["game_running"]:
        move_snake()

def move_snake():
    if not game["game_running"]:
        return
    x,y = game["snake"][0]
    if game["direction"]=="Up":
        y-=cell_size
    elif game["direction"]=="Down":
        y+=cell_size
    elif game["direction"]=="Left":
        x-=cell_size
    elif game["direction"]=="Right":
        x+=cell_size
    new_head=(x,y)
    if x<0 or x>=width or y<0 or y>=height or new_head in game["snake"]:
        game_over()
        return
    game["snake"].insert(0, new_head)
    if new_head==game["food"]:
        game["current_score"] += 1
        if game["current_score"]>game["high_score"]:
            update_high_score()
        while True:
            fx=random.randint(0,width//cell_size-1)*cell_size
            fy=random.randint(0,height//cell_size-1)*cell_size
            if (fx, fy) not in game["snake"]:
                game["food"]=(fx, fy)
                break
    else:
        game["snake"].pop()
    canvas=game["game_canvas"]
    canvas.delete("all")
    game["current_score_label"].config(text=f"Score: {game['current_score']}")
    game["highest_score_label"].config(text=f"High Score: {game['high_score']}")
    for i, (x, y) in enumerate(game["snake"]):
        color="Yellow" if i==0 else game["snake_color"]
        canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color)
    fx, fy= game["food"]
    canvas.create_oval(fx, fy, fx + cell_size, fy + cell_size, fill="red")
    root.after(150, move_snake)

def start_game():
    snake_food()
    game["game_running"]=True
    move_snake()

def game_over():
    game["game_running"]=False
    x=width//2
    y=height//2
    game["game_canvas"].create_text(x,y,text="GAME OVER",fill="red",font=("Arial", 24))

def restart_game():
    game["snake"]=[(100,100)]
    game["direction"]="Down"
    game["current_score"]=0
    snake_food()
    game["game_running"]=True
    move_snake()

def snake_food():
    while True:
        x=random.randint(0,width//cell_size-1)*cell_size
        y=random.randint(0,height//cell_size-1)*cell_size
        if (x,y) not in game["snake"]:
            game["food"]=(x, y)
            break

def change_direction(event):
    new_dir=event.keysym
    opposite={"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}
    if new_dir in ["Up","Down","Left","Right"] and new_dir!=opposite[game["direction"]]:
        game["direction"]=new_dir

root=tk.Tk()
root.title("Snake Game")
root.geometry("450x450")
root.config(background="black")
start_frame=tk.Frame(root, bg="black")
start_frame.pack(fill="both",expand=True)
game_title=tk.Label(start_frame,text="PythonIsEating",font=("Algerian", 40),fg="red",bg="black",padx=20,pady=70)
game_title.pack()
play_button = tk.Button(start_frame, text="Play", font=("Arial Black", 20),fg="green",bg="black",command=PythonIsEating)
play_button.pack()
frame1 = tk.Frame(root, bg="black")
root.mainloop()