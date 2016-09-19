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
                voters.append(Voter(self,row))
        return voters

    def initialize_poll(self):
        """
        Creates and runs a Poll instance.
        Parameters: none
        Returns: none
        """
        window = Tk()
        self.master = window
        self.read_questions()
        self.read_voters()
        print("%s voters" % len(csg_poll.voters))

    def retrieve_data(self,demographics,question,answer):
        """
        Retrieves data on a question for a specific set of voters who fit 1 or more demographic constraints

        Parameters
        ----------
        demographics: dictionary, with keys of demographic category name and values of demographic response
        question: string, which is the topic for the desired question
        answer: string, which is the answer that you want the percentage for

        Returns
        -------
        percentage: percentage of voters in the demographic category who responded to the question with the given answer
        """
        print("RETRIEVING DATA")

        # Retrieve voters whose demographics match desired
        voters_counted = []
        for voter in self.voters:
            matches = False
            for attr in demographics:
                if voter.responses[attr] == demographics[attr]:
                    matches = True
                else:
                    matches = False
            if matches:
                voters_counted.append(voter)

        # Retrieve response % from voters in target demographic
        total = len(voters_counted) * 1.0
        matching_answer = 0.0
        for voter in voters_counted:
            if voter.responses[question] == answer:
                matching_answer += 1.0
        percentage = matching_answer / total * 100
        print("%d of these voters (%d percent) answered %s with '%s'" % (matching_answer, percentage,question,answer))
        return percentage


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

questions_file = "Poll_Questions.csv"
voters_file = "CSG PoliSci Sample Poll Data.csv"
csg_poll = Poll(questions_file,voters_file)
csg_poll.initialize_poll()
csg_poll.retrieve_data({"School": "Academy"},"Party","Green")
end = raw_input("END")
