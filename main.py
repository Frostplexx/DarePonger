import textwrap
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
from win32.win32api import GetSystemMetrics
import pickle
import os



# --------------------------------------------------------------------Draw---------------------------------------------------------------------------------#

# Choose font, in array, 0 is first font
font = os.listdir("fonts/")[0]

    	

def drawImage(text_en, text_de, difficulty, maxtxtsize, name, save_location):
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
        border_color = (107, 115, 50)
    elif difficulty == 'Normal':
        border_color = (143, 153, 205)
    elif difficulty == 'Extreme':
        border_color = (122, 7, 39)

    # draws an ellipse with the border color, the size of the image. The it draws a smaller white ellipse over the first
    # one. The difference between the two is the border width
    draw.ellipse((0, 0, size, size), fill=border_color)
    draw.ellipse((relBorder, relBorder, size - relBorder, size - relBorder), fill=(255, 255, 255))

    # reduces text size, if text is too long. scaling factor found by trial and error
    #switch statemnts in python are dumb so i am using elif


    # clamps max text size to 70, otherwise some text will become larger
    if txtSize > maxtxtsize:
        txtSize = maxtxtsize



        

    text_en = "\n".join(textwrap.wrap(text_en, width=int(100 / txtSize * 12)))
    text_de = "\n".join(textwrap.wrap(text_de, width=int(100 / txtSize * 12)))

    # defines height and width of string, taking into account the font
    w_de, h_de = draw.textsize(text_de, font=fnt)
    w_en, h_en = draw.textsize(text_en, font=fnt)
    # draws the 2 texts. x position is the image size - half of the text size / 2.
    # moves the two texts apart by their respective text length - some offset: 
    #wrong formula but correct answer
    #21
    #text height = ~50
    #(size / 2)  + (h_en*)
    yOffSet = 25
    yOffSetGerText = (size / 2)  - h_de - yOffSet
    yOffSetEngText = (size / 2) + yOffSet

    draw.multiline_text(((size - w_de) / 2, yOffSetGerText), text_de, fill=(0, 0, 0), font=fnt, 
                        align="center")
    draw.multiline_text(((size - w_en) / 2, yOffSetEngText), text_en, fill=(0, 0, 0), font=fnt,
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
    print(h_en)
    print(h_de)
    


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
    [sg.Text('Language 1', size=(15, 1)), sg.InputText()],
    [sg.Text('Language 2', size=(15, 1)), sg.InputText()],
    [sg.Text('Choose Filename', size=(15, 1)), sg.InputText(default_text="Filename")],
    [sg.Text('Save Location',  size=(15,1)), sg.Input(default_text=pickle.load(open( "save.p", "rb" ))) ,sg.FolderBrowse()],
    [sg.Save(), sg.Button('Refresh'), sg.Quit()]

]

# Create the window
window = sg.Window("DarePonger", layout)
#creates the perview image for the first time
sg.popup_animated(image_source='files/thumbnail.png', title="Preview",
                  location=(GetSystemMetrics(0) / 5, GetSystemMetrics(1) / 2), keep_on_top=False)
while True:  # The Event Loop
    event, values = window.read()
    save = values[5]
    pickle.dump(save, open("save.p", "wb"))
    if event == 'Save':
        font = values[1]
        print(event, values)
        drawImage(values[2], values[3], values[0], 50, values[4], values[5])
        refreshPreview()
        
    if event == 'Refresh':
        font = values[1]
        print(event, values)
        drawImage(values[2], values[3], values[0], 50, values[4], values[5])
        refreshPreview()
        

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Quit':       
        break

window.close()

 
# --------------------------------------------------------------------------------------------------------------------------------------------------------#

#TODO new font and make font choosable. Implement settings, that can be saved
