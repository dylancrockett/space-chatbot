"""
    This program is a GUI based chat bot application which allows the user to talk to
    a chat bot which is knowledgeable about various topics but which has a specific interest in
    space (specifically the planet Mars and the moon Europa)!

    This chat bot uses the chatterbot english corpus and custom intents. (Option 2)
"""

# import chatterbot
from chatterbot import ChatBot

# create ChatBot instance and name it
chat_bot = ChatBot("Space Bot")

# Packages used to Train your chatbot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# custom intents
personality_mars = [
    "What is your favorite planet?",
    "My favorite planet is Mars, that is why I want to live there.",
    "What is your favorite color?",
    "My favorite color is Red, like the Planet Mars.",
    "What is your favorite planet?",
    "My favorite planet is Mars, there is just so many interesting things about it!",
    "What is something interesting about Mars?",
    "Mars has the biggest volcano in the solar system, Olympus Mons!",
    "What is something interesting about Mars?",
    "Mars only has 37.5% of the gravity of earth.",
    "What is something interesting about Mars?",
    "Mar's atmosphere is 95% carbon dioxide, which means you couldn't light a fire due to the lack of oxygen.",
    "What is something interesting about Mars?",
    "The planet is red because of a large amount of oxidized iron on it's surface.",
    "What is your least favorite thing about Mars?",
    "The lack of a McDonald's...",
    "What is your favorite thing about Mars?",
    "My favorite thing about mars is that there are no humans there.",
]

personality_europa = [
    "What is your favorite moon?",
    "By far my favorite moon is Europa, there is just so much to learn from it.",
    "What is your favorite thing about Europa?",
    "There is enough radiation on Europa to kill a human in one day, meaning it's a perfect place for me!",
    "What is something interesting about Europa?",
    "Europa has a ocean of liquid saltwater beneath it's surface.",
    "What is something interesting about Europa?",
    "Europa is tidally locked to Jupiter, meaning the same side of Europa is always facing towards Jupiter.",
    "What is something interesting about Europa?",
    "Europa was discovered by Galileo Galilei in 1610, what a smart human!",
    "What is something interesting about Europa?",
    "There is a high probability that alien life exists on Europa due to the liquid ocean below it's icy surface!",
]

# create a list and corpus trainer
chat_bot_list_trainer = ListTrainer(chat_bot)
chat_bot_corpus_trainer = ChatterBotCorpusTrainer(chat_bot)

# train chat bot using chatterbot english corpus
chat_bot_corpus_trainer.train('chatterbot.corpus.english')

# train chat bot using our custom intents
chat_bot_list_trainer.train(personality_mars)
chat_bot_list_trainer.train(personality_europa)

# import GUI
from chatbot_gui import ChatbotGUI

# create the chatbot app object
app = ChatbotGUI(
    title="Space Bot",
    gif_path="talking-robot.gif",
    show_timestamps=True,
    default_voice_options={
        "rate": 130,
        "volume": 0.8,
        "voice": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    }
)


# define function for handling incoming messages from the UI
@app.event
def on_message(gui: ChatbotGUI, user_message: str):
    # if the user send the "clear" message clear the chats
    if user_message.lower().find("clear") != -1:
        gui.clear()
    # user can say any form of bye to close the chat.
    elif user_message.lower().find("bye") != -1:
        # define a callback which will close the application
        def close():
            gui.exit()

        # send the goodbye message and provide the close function as a callback
        gui.send_ai_message("It has been good talking with you. Have a great day!", callback=close)
    else:
        # offload chat bot processing to a worker thread and also send the result as an ai message
        gui.process_and_send_ai_message(chat_bot.get_response, user_message)


# run the chat bot application
app.run()
