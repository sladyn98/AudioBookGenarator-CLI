from __future__ import print_function, unicode_literals
import os
import pytesseract
import sys
import tempfile
import warnings
from PIL import Image
from pdf2image import convert_from_path
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

import glob
files = glob.glob(sys.path[0] + "/projects/" + "*.pdf")
files_list = []
for i in files:
    files_list.append(i.split("/")[6])


f = Figlet(font='slant')
print(f.renderText('Audio Book Generator'))


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'list',
        'name': 'chosen_file',
        'message': 'Choose the file you want?',
        'choices': files_list,
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=style)
user_chose_file = answers['chosen_file']


warnings.simplefilter('ignore') 
filename = sys.path[0] + "/projects/" + str(user_chose_file)

 
with tempfile.TemporaryDirectory() as path:
     images_from_path = convert_from_path(filename, output_folder= sys.path[0] + "/intermediate_images/", last_page=2, first_page =0)
 
base_filename  =  os.path.splitext(os.path.basename(filename))[0] + '.JPG'     

save_dir = sys.path[0] + "/intermediate_images/"
i=1

file = open(sys.path[0] + "/projects/pdf_text.txt", "w")
for page in images_from_path:
    name = os.path.splitext(os.path.basename(filename))[0] + str(i) +'.JPG'
    name = sys.path[0] + "/intermediate_images/" + name
    page.save(os.path.join(save_dir, name), 'JPEG')
    i+=1
    file.write(pytesseract.image_to_string(Image.open(name)))
file.close()

###Audio file generating###
from gtts import gTTS
file = open(sys.path[0] + "/projects/pdf_text.txt", "r")
txt = file.read()
tts = gTTS(text = txt, lang = 'en')
tts.save(sys.path[0] + "/mp3/read.mp3")
file.close()











##Developed By Nitin Sahu github.com/globefire
