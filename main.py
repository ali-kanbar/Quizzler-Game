import requests,random,html
from tkinter import *

THEME_COLOR = "#375362"
number_of_questions = 50
score = 0

window = Tk()
window.resizable(width=False, height=False)
window.config(bg = THEME_COLOR,padx = 35,pady = 35)
window.title("Quizzler")
# ---------------------------- QUESTION GENERATION ------------------------------- #

def generate_new_question():
    global number_of_questions,score
    if number_of_questions > 0:
        index = random.randint(0,number_of_questions-1)
        question,answer = html.unescape(result[index]["question"]),result[index]["correct_answer"]
        number_of_questions -= 1
        result.pop(index)
        canvas.itemconfig(canvas_text,text = question)
        return answer
    
def set_background_to_white():
    global answer
    canvas.config(bg = "white")
    right_button.config(state = "active")
    false_button.config(state = "active")
    answer = generate_new_question()

# ---------------------------- BUTTONS COMMANDS ------------------------------- #

def right():
    global score,answer
    right_button.config(state = "disabled")
    false_button.config(state = "disabled")
    if answer == "True":
        canvas.config(bg = "green")
        score += 1
        score_label.config(text = f"Score : {score}")
    else:
        canvas.config(bg = "red")
    if number_of_questions == 0:window.after(500,end_quiz)
    else:window.after(500,set_background_to_white)
          
def false():
    global score,answer
    right_button.config(state = "disabled")
    false_button.config(state = "disabled")
    if answer == "False":
        canvas.config(bg = "green")
        score += 1
        score_label.config(text = f"Score : {score}")
    else:
        canvas.config(bg = "red")
    if number_of_questions == 0:window.after(500,end_quiz)
    else:window.after(500,set_background_to_white)

def end_quiz():
    canvas.config(bg = "white")
    canvas.itemconfig(canvas_text,text = f"You've reached the end of this quiz and you scored {score} points\nThank you for playing")
    window.after(2500,quit)

# ---------------------------- API REQUEST ------------------------------- #

parameters = {
    "amount" : number_of_questions,
    "type" : "boolean",
}
request = requests.get(url = "https://opentdb.com/api.php",params = parameters)
request.raise_for_status()
data = request.json()
result = data["results"]

# ---------------------------- UI SETUP ------------------------------- #

score_label = Label(text = "Score : 0",bg = THEME_COLOR,fg = "white",font = ("Courier",15,"bold"))
score_label.grid(column = 1,row = 0)
canvas = Canvas(width = 350,height = 350,bg = "white")
canvas_text = canvas.create_text(175,175,text = "",width = 300,font = ("Arial",20,"italic"))
canvas.grid(column = 0,row = 1,columnspan = 2,pady = 30)
right_photo = PhotoImage(file = "images/true.png")
right_button = Button(image = right_photo,highlightthickness = 0,command=right)
right_button.grid(column = 0,row = 2)

false_photo = PhotoImage(file = "images/false.png")
false_button = Button(image = false_photo,highlightthickness = 0,command = false)
false_button.grid(column = 1,row = 2)

end_button = Button(text = "End Quiz",highlightthickness=0,command = end_quiz,font = ("Arial",20,"italic"))
end_button.grid(column = 0,row = 0)

answer = generate_new_question()

window.mainloop()