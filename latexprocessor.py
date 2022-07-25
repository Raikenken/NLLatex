import json

from sympy import *
import csv

class LatexProcessor:
    def __init__(self):
        with open('keywords.csv', 'r') as f:
            reader = csv.reader(f)
            self.keywords = set(row[0] for row in reader)

            # load translation.json into a dictionary called translations
            with open('translation.json') as json_file:
                self.translations = json.load(json_file)
                json_file.close()

    def latex_to_image(self, input_string):
        # convert latex string to image using preview
        preview(input_string, viewer='file', output='png', filename="temp.png")

    def clean_text_to_latex(self, input_string):
        # convert text string to latex string
        return latex(input_string)

    def clean_text(self, input_string):
        # cleans user input string to be used in latex
        pass

    def indefinite_integral_form(self, equation, variable):
        return Integral(equation, symbols(variable))

    def definite_integral_form(self, equation, variable, lower_bound, upper_bound):
        if self.islatexnumeric(lower_bound) and self.islatexnumeric(upper_bound):
            return Integral(equation, (symbols(variable), lower_bound, upper_bound))
        else:
            if not(self.islatexnumeric(lower_bound)):
                lower_bound = symbols(lower_bound)
            if not(self.islatexnumeric(upper_bound)):
                upper_bound = symbols(upper_bound)
            return Integral(equation, (symbols(variable), lower_bound, upper_bound))

    def islatexnumeric(self, input_string):
        # checks if input string is a number
        return input_string.isnumeric() or input_string == "oo"