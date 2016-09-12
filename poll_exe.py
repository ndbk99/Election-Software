from Tkinter import *

class App:

    def __init__(self,master,questions):
        self.questions = questions
        self.master = master
        self.on_question = 0
        ##### GUI elements go here #####

        # Create title label
        self.title = Label(master, text="CSG Polling Software")
        self.title.pack()

        # Create "next", "back", "submit" buttons

    def print_check(self,text):
        print(text)

    def ask_question(self,n):
        nth_question = self.questions[n]
        # Create question label
        Label(self.master, text=nth_question.question).pack()

        # Create radio buttons
        answer = IntVar()
        for x in range(len(nth_question.options)):
            option = nth_question.options[x]  # Get option
            Radiobutton(self.master, text=option, variable=answer, value=x).pack()  # Create radio button option

        # How to actually store the answer once the user has added it?
        # Maybe when the user presses "Next", we store the current value of "answer".
        # WRITE THIS NEXT!

# Class to hold the questions and their answers
class Question:
    def __init__(self,question,options):
        self.question = question
        self.options = options
        self.answers = []

    def add_answer(self,answer):
        self.answers.append(answer)

#
def initialize_poll():
    print("Started")

    test_question_0 = Question("How are you?",["good","bad","meh"])
    test_question_1 = Question("What grade are you in?",["9","10","11","12"])
    questions = [test_question_0,test_question_1]
    print("Created questions")

    # Make window, app object
    window = Tk()
    poll = App(window,questions)
    print("Made window")

    poll.ask_question(1)

    # End program on exit
    window.mainloop()
    print("Finished")

initialize_poll()
