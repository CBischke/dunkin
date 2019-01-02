from model.axiom import Axiom

class Idea(Axiom):
    """
    Represents a core idea made up of assumptions
    """
    def __init__(self, string_idea, score):
        super(Idea, self).__init__(string_idea, score)

    def __str__(self):
        return super(Idea, self).__str__()
