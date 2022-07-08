import sympy

def convert_to_image(string):
    # convert latex string to image using preview
    sympy.preview(string, viewer='file', output='png', filename="temp.png")


