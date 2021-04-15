# Repo -> https://github.com/NoOneLuvMe/theimagebot
# Dev -> t.me/no_one_luv_me
# channel -> https://t.me/theostrich
# support -> https://t.me/ostrichdiscussion

import requests
import logging
import pytesseract
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
import carbonsh
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def imagetotext(update, context):
    context.bot.get_file(update.message.reply_to_message.photo[-1]).download(custom_path="./downloads/PictoText.jpg")
    username = update.message.chat.username
    print("started By : ", username)

    messa = '''<b>
Please Wait For Few Minutes 🧘‍♂️

Generating 🍧 Text From The Image 🌠

Please Don't Spam 🥺
    </b>'''
    update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='html')
    pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"

    # Method to process the blue band
    def pixelProcBlue(intensity):
        return intensity

    imageObject = Image.open('downloads/PictoText.jpg')
    multiBands = imageObject.split()
    blueBand = multiBands[2].point(pixelProcBlue)

    image_to_text = pytesseract.image_to_string(blueBand, lang='eng')
    image_to_text += '''

Text from Image By @theimagebot ❤
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=image_to_text)


def addwatermark(update, context):
    text_watermark_from_user = context.args
    username = update.message.chat.username
    print("addwatermark By : ", username)

    watermark_text = str(text_watermark_from_user).split(":")[0].strip().replace("'", "").replace(",", "").replace("[",
                                                                                                                   "").replace(
        "]", "")
    size_ = int(
        str(text_watermark_from_user).split(":")[1].strip().replace("'", "").replace(",", "").replace("[", "").replace(
            "]", ""))

    if size_ < 100:

        context.bot.get_file(update.message.reply_to_message.photo[-1]).download(
            custom_path="./downloads/@theimagebot.png")
        messa = '''<b>
Please Wait For Few Seconds 🧘‍♂️

Adding Watermark 🍃 to the image 🌠

Please Don't Spam 🥺
                </b>'''
        update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='html')

        photo = Image.open("./downloads/@theimagebot.png")
        # make the image editable
        width, height = photo.size

        draw = ImageDraw.Draw(photo)
        text = watermark_text
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', int(size_))
        textwidth, textheight = draw.textsize(text, font)

        # calculate the x,y coordinates of the text
        margin = 5
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=font)
        photo.save('./downloads/@theimagebot.png')

        caption = "<b>Watermark Added By <a herf=\"http://t.me/theimagebot\">@theimagebot</a></b>❤️"
        context.bot.send_document(chat_id=update.effective_chat.id,
                                  document=open('./downloads/@theimagebot.png', 'rb'),
                                  caption=caption, parse_mode="html")

    else:
        messa = '''
*Size Must Be < 100 😇

Use /help If U don't Know How to Use Me*
    '''
        update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='markdown')


def blur(update, context):
    username = update.message.chat.username
    print("Blured By : ", username)
    context.bot.get_file(update.message.reply_to_message.photo[-1]).download(
        custom_path="./downloads/@theimagebot.png")
    blur_radious = int(context.args[0])

    if blur_radious < 100:

        messa = '''<b>
Please Wait For Few Seconds 🧘‍♂️

Start Bluring 🧖‍♂️ the image 🌠

Please Don't Spam 🥺
                            </b>'''

        update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='html')

        Photo = Image.open("./downloads/@theimagebot.png")
        photo = Photo.filter(ImageFilter.GaussianBlur(radius=blur_radious))
        photo.save('./downloads/@theimagebot.png')

        caption = "<b>Blured  By <a herf=\"http://t.me/theimagebot\">@theimagebot</a></b> ❤️"
        context.bot.send_document(chat_id=update.effective_chat.id,
                                  document=open('./downloads/@theimagebot.png', 'rb'),
                                  caption=caption, parse_mode="html")

    else:
        messa = '''
*Blur Value Must Be < 100 😇

Use /help If U don't Know How to Use Me*    '''
        update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='markdown')


def reverse(update, context):
    username = update.message.chat.username
    print("Reverse By : ", username)
    context.bot.get_file(update.message.reply_to_message.photo[-1]).download(
        custom_path="./downloads/@theimagebot.png")
    messa = '''<b>
Please Wait For Few Seconds 🧘‍♂️

Reversing 🔍 the image

Please Don't Spam 🥺
                                    </b>'''

    update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='html')

    filePath = "./downloads/@theimagebot.png"
    searchUrl = 'http://www.google.hr/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    link = f'''
<b>Your Search Result 👇 </b>

{fetchUrl}

<b>Reversed By️
   <a herf=\"http://t.me/theimagebot\">@theimagebot</a></b> ❤
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=link, parse_mode='html')


@run_async
def start(update, context):
    username = update.message.chat.username
    print("started By : ", username)
    welcome = f'''
<b>Hey {username} 👋

I'm <a herf=\"http://t.me/theimagebot\">theimagebot</a> 

I'm a Open Source Bot 
/source_code to Get Repo Link 😌

I Can Do Many Things

💫 ➠ I Can Carbonized A Code 
💫 ➠ I Can Extract Text From An Image
💫 ➠ I Can Reverse Search An Image
💫 ➠ I Can Add Watermark to An Image
💫 ➠ I Can Blur A Image

Hit /help If You Don't Know How to Use Me 

Developer : <a href=\"t.me/no_one_luv_me\"> ෴ 乂(≧▽≦) 乂 ෴ </a>🧑‍💻

Support Group : <a href=\"https://t.me/ostrichdiscussion\">Ostrich Discussion</a> 🦸‍♂️

Made By <a href=\"https://t.me/theostrich\"> Ostrich </a> ❤️

</b>
'''
    update.message.reply_text(reply_to_message_id=update.message.message_id, text=welcome, parse_mode='html',
                              disable_web_page_preview=True)

@run_async
def help(update, context):
    help_ = '''
*You Don't Know How to Use Me ? ok

To Get text from that image 🏃‍♂️

replay to an image with /imagetotext  

To Reverse search a image 🔍

replay to an image with /reverse

To Carbonized a Code 🌱

replay to a Message with /carbon

To Add watermark to an image 🏋️‍♂
️
replay to an image with /addwatermark {text to be watermark}:{watermark size}

example: /addwatermark @ostrichdiscussion:30

To Blur A Image 🚵‍♀️

replay to an image with /blur {blur value}

example: /blur 40

I'm a Open Source Bot 
/source_code to Get Repo Link 😌
*
    '''
    update.message.reply_text(reply_to_message_id=update.message.message_id, text=help_, parse_mode='markdown')


def carbon(update, context):
    username = update.message.chat.username
    print("Carbon By : ", username)
    messa = '''<b>
Please Wait For Few Seconds 🧘‍♂️

Carbonizing 🌿 the Your Code 👨‍💻

Please Don't Spam 🥺
                                        </b>'''

    update.message.reply_text(reply_to_message_id=update.message.message_id, text=messa, parse_mode='html')

    code = update.message.reply_to_message.text

    config = carbonsh.Config(language=carbonsh.languages.AUTO)

    # returns >>> 'https://carbon.now.sh/?bg=rgba(...'
    carbon_url = carbonsh.code_to_url(code, config)

    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": "./downloads/",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }

    options.add_experimental_option('prefs', prefs)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.get(carbon_url)
    time.sleep(5)
    button = driver.find_element_by_xpath("//button[@class='jsx-1730877631 ']")
    button.click()
    time.sleep(5)
    caption = "<b>Carbonized By <a herf=\"http://t.me/theimagebot\">@theimagebot</a></b>❤️"
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=open('./downloads/carbon.png', 'rb'),
                              caption=caption, parse_mode="html")
    driver.close()


@run_async
def source_code(update, context):
    username = update.message.chat.username
    print("Source  : ", username)
    source = '''

Developer : <a href=\"t.me/no_one_luv_me\"> ෴ 乂(≧▽≦) 乂 ෴ </a>🧑‍💻
    
Repository Link : https://github.com/NoOneLuvMe/theimagebot
    
<b>Give a 🌟 if you liked the repo ❤️</b>

Support Group : <a href=\"https://t.me/ostrichdiscussion\">Ostrich Discussion</a> 🦸‍♂️

Made By <a href=\"https://t.me/theostrich\"> Ostrich </a> ❤️  


 
    '''
    update.message.reply_text(reply_to_message_id=update.message.message_id, text=source, parse_mode='html',
                              disable_web_page_preview=True)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start, run_async=True)
    help_handler = CommandHandler('help', help, run_async=True)
    source_code_handeler = CommandHandler('source_code', source_code, run_async=True)
    addwatermark_handeler = CommandHandler('addwatermark', addwatermark, run_async=True)
    imagetotext_handeler = CommandHandler('imagetotext', imagetotext)
    reverse_handeler = CommandHandler('reverse', reverse)
    blur_handeler = CommandHandler('blur', blur)
    carbon_handeler = CommandHandler('carbon', carbon)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(carbon_handeler)
    dispatcher.add_handler(reverse_handeler)
    dispatcher.add_handler(blur_handeler)
    dispatcher.add_handler(addwatermark_handeler)
    dispatcher.add_handler(imagetotext_handeler)
    dispatcher.add_handler(source_code_handeler)

    updater.start_polling()

if __name__ == '__main__':
    main()
# Dev -> t.me/no_one_luv_me
# channel -> https://t.me/theostrich
# support -> https://t.me/ostrichdiscussion
