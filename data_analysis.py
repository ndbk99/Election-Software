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

    Methods
    -------
        read_questions(questions_file): reads in questions from questions_file CSV, creates Question object for each
        read_voters(voters_file): reads in voters from voters_file CSV, creates Voter object for each
        generate_window(): creates Tk GUI window with options for data analysis
    """

    def __init__(self,master,questions_file,voters_file):
        self.master = master
        self.questions_file = questions_file
        self.voters_file = voters_file
        self.questions = self.read_questions()
        self.voters = self.read_voters()

    def read_questions(self):
        questions = []
        with open(self.questions_file) as csvfile:
            doc = csv.reader(csvfile)
            for row in doc:
                questions.append(Question(self,row))
        return questions

    def read_voters(self):
        voters = []
        with open(self.voters_file) as csvfile:
            doc = csv.reader(csvfile)
            header = next(doc,None)
            for row in doc:
                voters.append(Voter(self,row))
        return voters

    def generate_window(self):
        pass

    def retrieve_data(self):
        pass


class Voter:
    """
    Class to hold information about a voter who responded to the poll.

    Parameters
    ----------
        row: line of data from voter_file with correct format

    Attributes
    ----------
        demographics: array of responses to questions about voter demographics
        responses: array of responses to poll questions

    Methods
    -------
    """

    def __init__(self,poll,responses):
        self.Poll = poll
        questions = [q.topic for q in self.Poll.questions]
        self.responses = dict(zip(questions, responses))

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

def run_analysis():
    window = Tk()
    questions_file = "Poll_Questions.csv"
    voters_file = "CSG PoliSci Sample Poll Data.csv"
    csg_poll = Poll(window,questions_file,voters_file)
    csg_poll.read_questions()
    csg_poll.read_voters()
    print("%s voters" % len(csg_poll.voters))
    end = raw_input("END")

run_analysis()
