issues = ["President","Senator"]

class Voter:
    def __init__(self,school,grade,age,gender,race):
        self.school = school
        self.grade = grade
        self.age = age
        self.gender = gender
        self.race = race
        self.responses = (dict(issue,0) for issue in issues)

    def add_vote(self,issue,answer):
        self.responses[issue] = answer
