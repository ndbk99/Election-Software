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
        next_button = Button(master, text="Next")
        next_button.callback = self.next_question
        next_button.pack()

        back_button = Button(master, text="Back")
        back_button.pack()
        callback=self.previous_question()

        submit_button = Button(master, text="Submit", callback=self.submit_answer())
        submit_button.pack()

        # For some reason, the button functions are being called automatically - why?

    def ask_question(self,n):
        self.on_question = n
        nth_question = self.questions[n]
        # Create question label
        Label(self.master, text=nth_question.question).pack()

        # Create radio buttons
        choice = IntVar()
        for x in range(len(nth_question.options)):
            option = nth_question.options[x]  # Get option
            button = Radiobutton(self.master, text=option, variable=choice, value=x)  # Create radio button for option
            button.pack()
            self.questions[n].radio_buttons.append(button)

    def next_question(self):
        print("next_question called")
        for button in self.questions[self.on_question].radio_buttons:
            button.pack_forget()  # Delete previous question's options
        # self.questions[self.on_question].answers.append(choice)  # Add previous answer to list ?? HOW
        self.ask_question(self.on_question + 1)

    def previous_question(self):
        print("previous_question called")
        for button in self.questions[self.on_question].radio_buttons:
            button.pack_forget()  # Delete previous question's options
        # self.questions[self.on_question].answers.append(choice)
        if self.on_question > 0:
            self.ask_question(self.on_question - 1)
        else:
            print("This is the first question; cannot go back")

    def submit_answer(self):
        print("Submitted")

# Class to hold the questions and their answers
class Question:
    def __init__(self,question,options):
        self.question = question
        self.options = options
        self.answers = []
        self.radio_buttons = []

    def submit_answer(self,text):
        print("submitted")

# Run the poll
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

    # poll.ask_question(0)

    # End program on exit
    window.mainloop()
    print("Finished")

initialize_poll()
