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
        if self.is_latex_numeric(lower_bound) and self.is_latex_numeric(upper_bound):
            return Integral(equation, (symbols(variable), lower_bound, upper_bound))
        else:
            if not (self.is_latex_numeric(lower_bound)):
                lower_bound = symbols(lower_bound)
            if not (self.is_latex_numeric(upper_bound)):
                upper_bound = symbols(upper_bound)
            return Integral(equation, (symbols(variable), lower_bound, upper_bound))

    def is_latex_numeric(self, input_string):
        # checks if input string is a number
        input_string = input_string.strip()
        return input_string.isnumeric() or input_string == "oo"

    def parse_text(self, text):
        tokens = text.split()
        clean_text = "$"

        ctr = 0;
        # fix to change variables in translations
        while ctr < len(tokens):
            if tokens[ctr] in self.translations.keys():
                if tokens[ctr] == "integral":
                    if tokens[ctr + 1] == "from":
                        lower_bound = ""
                        upper_bound = ""
                        equation = ""
                        variable = ""

                        ctr += 2

                        while tokens[ctr] != "to":
                            lower_bound += tokens[ctr] + " "
                            ctr += 1
                        ctr += 1

                        while tokens[ctr] != "of":
                            upper_bound += tokens[ctr] + " "
                            ctr += 1
                        ctr += 1

                        while tokens[ctr] != "variable":
                            equation += tokens[ctr] + " "
                            ctr += 1
                        ctr += 1

                        variable = tokens[ctr]

                        integral = self.definite_integral_form(equation, variable, lower_bound, upper_bound)

                        clean_text += self.clean_text_to_latex(integral) + " "

                        ctr += 1

                    else:
                        equation = ""
                        variable = ""

                        ctr += 1

                        while tokens[ctr] != "variable":
                            equation += tokens[ctr] + " "
                            ctr += 1
                        ctr += 1

                        variable = tokens[ctr]

                        integral = self.indefinite_integral_form(equation, variable)

                        clean_text += self.clean_text_to_latex(integral) + " "

                        ctr += 1

                else:
                    clean_text += self.translations[tokens[ctr]] + " "
            else:
                clean_text += tokens[ctr] + " "
            ctr += 1

        clean_text += "$"

        return clean_text
