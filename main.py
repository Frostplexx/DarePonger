import textwrap
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
from win32.win32api import GetSystemMetrics
import pickle
import os



# --------------------------------------------------------------------Draw---------------------------------------------------------------------------------#

# Choose font, in array, 0 is first font
font = os.listdir("fonts/")[0]
 
    	

def drawImage(text_en, text_de, text_it, difficulty, maxtxtsize, name, save_location):
    # image size
    size = 1000
    # border size, the smaller, the bigger the border is??
    border = 40
    # 1000 : 50 = x : 2 -> some funky calculation, actual bordersoze is not 40 but 50
    relBorder = (size * 2) / border
    # defines border colors as black ; see line 34 
    border_color = (0, 0, 0)
    # creates image with alpha 255  = transaprent
    img = Image.new('RGBA', (size, size), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    # Text Size = max Text size, max Text size is passed to this function (normally 70)
    txtSize = maxtxtsize
    #TODO fix this
    fnt = ImageFont.truetype('fonts/' +  font, txtSize)
    # sets  border color for difficulty
    # 0 = easy (green), 1 = medium(orange), 2 = hard (red)
    if difficulty == 'Easy':
        border_color = (143, 153, 205)
    elif difficulty == 'Normal':
        border_color = (107, 115, 50)
    elif difficulty == 'Extreme':
        border_color = (122, 7, 39)

    # draws an ellipse with the border color, the size of the image. The it draws a smaller withe ellipse over the first
    # one. The difference between the two is the border width
    draw.ellipse((0, 0, size, size), fill=border_color)
    draw.ellipse((relBorder, relBorder, size - relBorder, size - relBorder), fill=(255, 255, 255))

    # reduces text size, if text is too long. scaling factor found by trial and error
    #switch statemnts in python are dumb so i am using elif
    if len(text_en) >= 50:
        txtSize = int(150 / len(text_en) * 25)
    elif len(text_de) >= 50:
        txtSize = int(150 / len(text_de) * 25)
    elif len(text_it) >= 50:
        txtSize = int(150 / len(text_it) * 25)

    # clamps max text size to 70, otherwise some text will become larger
    if txtSize > maxtxtsize:
        txtSize = maxtxtsize


    # after a set length, add a linebreak. how many word per line depends on text size
    text_en = "\n".join(textwrap.wrap(text_en, width=int(100 / txtSize * 18)))
    text_de = "\n".join(textwrap.wrap(text_de, width=int(100 / txtSize * 18)))
    text_it = "\n".join(textwrap.wrap(text_it, width=int(100 / txtSize * 18)))

    # defines height and width of string, taking into account the font
    w_en, h_en = draw.textsize(text_en, font=fnt)
    w_de, h_de = draw.textsize(text_de, font=fnt)
    w_it, h_it = draw.textsize(text_it, font=fnt)
    # draws the 3 texts. x position is the image size - half of the text size / 2.
    # y positon for german text is centered, other text have a offset from the middle text
    draw.multiline_text(((size - w_en) / 2, (size - h_en) / 2 - h_de - 50), text_en, fill=(0, 0, 0), font=fnt,
                        align="center")
    draw.multiline_text(((size - w_de) / 2, (size - h_de) / 2), text_de, fill=(0, 0, 0), font=fnt, align="center")
    draw.multiline_text(((size - w_it) / 2, (size - h_it) / 2 + h_de + 50), text_it, fill=(0, 0, 0), font=fnt,
                        align="center")

    # tries to apply antialiasing, but it doesnt seem to work
    # TODO revisit antialiasing
    img = img.resize((size, size), Image.ANTIALIAS)
    #saves image at defined location, with choosen name
    img.save(save_location + '/' + name + '.png')
    #creates a thumbnail image for preview in the gui with 200x200
    img = img.resize((200, 200), Image.ANTIALIAS)
    img.save('files/thumbnail.png')

    # debug code
    print("text length en: " + str(len(text_en)))
    print("text length de: " + str(len(text_de)))
    print("text length iz: " + str(len(text_it)))

    print("Text Size: " + str(txtSize))
    print("relativ Border thickness: " + str(relBorder))
    print("relativ max Text size: " + str(maxtxtsize))
    print("Save Location: " + save_location + '/' + name + '.png')
    print("Installed Fonts: " + str(os.listdir("fonts/")))
    print(pickle.load(open( "save.p", "rb" )))
    

#function to refresh preview image
def refreshPreview():
    sg.popup_animated(image_source=None)
    sg.popup_animated(image_source='files/thumbnail.png', title="Preview",
                      location=(GetSystemMetrics(0) / 5, GetSystemMetrics(1) / 2))
                      
# --------------------------------------------------------------------------------------------------------------------------------------------------------#


# -----------------------------------------------------------------------GUI------------------------------------------------------------------------------#

# define theme
sg.theme('SystemDefault1')
#array of all aviable difficulties
diff = ('Easy', 'Normal', 'Extreme')
#creates layout for the GUI
layout = [

    [sg.Text('Create Card')],
    [sg.Text('Select Difficulty', size=(15, 1)), sg.Combo(diff, size=(15, 1), readonly=True, default_value='Easy'), sg.Text("Font"), 
        sg.Combo(os.listdir("fonts/"), size=(15, 1), readonly=True, default_value=os.listdir("fonts/")[0])],
    [sg.Text('German', size=(15, 1)), sg.InputText()],
    [sg.Text('English', size=(15, 1)), sg.InputText()],
    [sg.Text('Italian', size=(15, 1)), sg.InputText()],
    [sg.Text('Choose Filename', size=(15, 1)), sg.InputText(default_text="Filename")],
    [sg.Text('Save Location',  size=(15,1)), sg.Input(default_text=pickle.load(open( "save.p", "rb" ))) ,sg.FolderBrowse()],
    [sg.Save(), sg.Button('Refresh'), sg.Quit()]

]

# Create the window
window = sg.Window("DarePonger", layout)
#drawImage("", "", "", 'Easy', 70, "default", "files/")
#creates the perview image for the first time
sg.popup_animated(image_source='files/thumbnail.png', title="Preview",
                  location=(GetSystemMetrics(0) / 5, GetSystemMetrics(1) / 2), keep_on_top=False)
while True:  # The Event Loop
    event, values = window.read()
    save = values[6]
    pickle.dump(save, open("save.p", "wb"))
    if event == 'Save':
        font = values[1]
        print(event, values)
        drawImage(values[2], values[3], values[4], values[0], 70, values[5], values[6])
        refreshPreview()
        

    if event == 'Refresh':
        font = values[1]
        print(event, values)
        drawImage(values[2], values[3], values[4], values[0], 70, values[5], values[6])
        refreshPreview()
        

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Quit':       
        break

window.close()

 
# --------------------------------------------------------------------------------------------------------------------------------------------------------#

#TODO new font and make font choosable. Implement settings, that can be saved
