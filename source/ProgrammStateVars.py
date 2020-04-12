import os

class ProgrammStateVars:
    lastRequest = ""
    programmDir = os.path.dirname(os.path.realpath(__file__))
    jsonDir = "var"