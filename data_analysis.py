from Tkinter import *
import csv

class Poll:
    """
    Class to organize and analyze data from a poll.

    Parameters
    ----------
        questions_file: CSV file holding poll questions
            format - question topic, question statement, answer 1, answer 2, ..., answer n
        voters_file: CSV file holding voter responses
            format - timestamp, demographic info ... [1-10], question responses ... [11-q]

    Attributes
    ----------
        master: Tk GUI window to hold the analysis interface
        questions: list of questions asked in the poll
        voters: list of voters who responded to the poll
        questions_file: CSV file holding poll questions (see parameter of same name)
        voters_file: CSV file holding voters (see parameter of same name)

    Methods
    -------
        read_questions(questions_file): reads in questions from questions_file CSV, creates Question object for each
        read_voters(voters_file): reads in voters from voters_file CSV, creates Voter object for each
        generate_window(): creates Tk GUI window with options for data analysis
    """

    def __init__(self,questions_file,voters_file):
        self.master = 0
        self.questions_file = questions_file
        self.voters_file = voters_file
        self.questions = self.read_questions()
        self.voters = self.read_voters()

    def read_questions(self):
        """
        Reads in info (topic, statement, answers) for each question asked in the poll.
        """
        questions = []
        with open(self.questions_file) as csvfile:
            doc = csv.reader(csvfile)
            for row in doc:
                questions.append(Question(self,row))
        return questions

    def read_voters(self):
        """
        Reads in voter response data from CSV file.
        """
        voters = []
        with open(self.voters_file) as csvfile:
            doc = csv.reader(csvfile)
            header = next(doc,None)
            for row in doc:
                # print(row)
                voters.append(Voter(self,row))
        return voters

    def initialize_poll(self):
        """
        Creates GUI window, reads questions and voter responses from files, adds all GUI elements (dropdowns, button, etc.)
        Parameters: none
        Returns: none
        """
        # Initialze GUI window
        window = Tk()
        self.master = window

        # Read data, print info about questions and voters
        self.read_questions()
        self.read_voters()
        # print("%s voters, %s questions" % (len(csg_poll.voters), len(csg_poll.questions)))

        ########################### GUI elements ###############################

        # Add labels and dropdowns for demographic attributes
        self.dropdowns = {}
        for n in range(6):
            self.add_demographic_dropdown(n)

        # Add label and dropdown for question topic
        Label(self.master,text="Question").pack()
        question_topics = [q.topic for q in self.questions]
        question_topics.insert(0,"------")
        question = StringVar(self.master)
        question.set("------")
        self.dropdown_question = question
        self.question_dropdown = OptionMenu(self.master,question,*question_topics[7:])
        self.question_dropdown.pack()

        # Add button to submit query
        submit_button = Button(self.master,text="Submit Query")
        submit_button.bind("<Button-1>",self.query_data)  # Binding works; now just need to reformat retrieve_data for automated call
        submit_button.pack()

    def query_data(self,event):
        self.retrieve_data()

    def add_demographic_dropdown(self,question_number):
        """
        Adds GUI dropdown element for a demographic question.

        Parameters
        ----------
        question_number: integer, 0 < question_number < n - 1

        Returns
        -------
        none; just adds GUI elements
        """
        # Retrieve desired question and options
        question = self.questions[question_number]
        question_responses = question.responses
        question_responses.insert(0,"------")

        # Demographic label
        label = Label(self.master,text=question.topic)
        label.pack()

        # Demographic dropdown
        variable = StringVar(self.master)
        variable.set("------") # default value
        dropdown = OptionMenu(self.master,variable,*question_responses)
        dropdown.pack()

        # Add dropdown value variable to array
        self.dropdowns[self.questions[question_number].topic] = variable

    def retrieve_data(self):
        """
        Retrieves data on a question for a specific set of voters who fit 1 or more demographic constraints

        Parameters
        ----------
        none; automatically retrieves demographics, question, and answer from GUI dropdowns!

        Returns
        -------
        percentage: percentage of voters in the demographic category who responded to the question with the given answer
        """

        ###### Retrieve query data from dropdowns ######

        # Get demographics dictionary; MAPS TO "demographics" PARAMETER RIGHT NOW
        demographics = {}
        for key in self.dropdowns:
            if self.dropdowns[key].get() != "------":
                # this_question = self.questions[key].topic  # PROBLEM HERE... self.questions is not a dictionary
                demographics[key] = self.dropdowns[key].get()

        # Get question topic
        question = self.dropdown_question.get()


        ###### Select voters and retrieve desired response data from them ######

        # Search through dropdowns and see if any have been set
        demographics_set = False
        for variable in self.dropdowns:
            if self.dropdowns[variable].get() != "------":
                demographics_set = True

        # If at least one demographic field has been set, cull voters from that demographic
        if demographics_set:
            # Retrieve voters whose demographics match desired
            voters = []
            for voter in self.voters:
                matches = False
                for attr in demographics:
                    # If the voter's response is the same as or within the demographics attribute
                    if voter.responses[attr] == demographics[attr] or str(voter.responses[attr]).find(str(demographics[attr])) == 0:
                        matches = True
                    else:
                        matches = False
                        break
                if matches:
                    voters.append(voter)
        # If no demographic fields have been set, look at all voters
        else:
            voters = self.voters

        if len(voters) == 0:
            print("No voters matched your query. Please change your parameters and try again.")
        else:
            # Find the correct question
            for q in self.questions:
                if q.topic == question:
                    this_question = q

            # Create empty dictionary to hold counts for each asnwer
            counts = {}
            for r in this_question.responses:
                counts[r] = 0

            # Look through voters and add counts to correct answer bins
            for voter in voters:
                for key in counts:  # Iterate through each answer for each voter and see which they picked
                    if voter.responses[question] == key:
                        counts[key] += 1

            # Create dictionary holding percentages for each answer
            percentages = {}
            n = len(voters)  # Find total number of voters

            # Print all info (calculate percentages as you go also)
            print(" ")
            print("Question: %s, n = %d" % (question,n))
            print(" ")
            for key in counts:
                percentages[key] = (counts[key]*100.00) / (n*1.00)
                print("%s: %.2f%%" % (key,percentages[key]))
            print(" ")
            print("----------------")

class Voter:
    """
    Class to hold information about a voter who responded to the poll.

    Parameters
    ----------
        row: line of data from voter_file with correct format

    Attributes
    ----------
        Poll: poll object with which the voter is associated
        responses: dictionary of responses to poll questions

    Methods
    -------
    """

    def __init__(self,poll,row):
        self.Poll = poll
        questions = [q.topic for q in self.Poll.questions]
        self.timestamp = row[0]
        self.responses = dict(zip(questions, row[1:]))

class Question:
    """
    Class to hold information about a question asked in the poll.

    Parameters
    ----------
    poll: Poll object with which the question is associated
    row: row of data being read in as a question
        format - question topic, question statement, question answers ...

    Attributes
    ----------
    Poll: Poll object with which the question is associated
    topic: topic/label of the question
    statement: the actual quesiton

    Methods
    -------
    """
    def __init__(self,poll,row):
        self.Poll = poll
        self.topic = row[0]
        self.statement = row[1]
        self.responses = row[2:]

questions_file = "Poll_Questions.csv"  # Link to file holding questions
voters_file = "CSG PoliSci Sample Poll Data.csv"  # Link to file holding voters
csg_poll = Poll(questions_file,voters_file)  # Create poll object
csg_poll.initialize_poll()  # Initialize analysis window
# Also, right now the retrieve_data is returning stats out of all voters, since it runs automatically before the user can select
end = input("")
