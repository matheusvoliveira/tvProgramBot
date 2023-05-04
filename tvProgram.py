from telegram.ext import *
import keys
import requests
import json

# info api IMDB
url = "https://online-movie-database.p.rapidapi.com/auto-complete"


search_term = ''

print('Starting up bot ...')

def start_command(update, context):
    update.message.reply_text("Hello there! I'm a tvProgram bot. Find your programs with me!")


def help_command(update, context):
    update.message.reply_text("Type 'search' + name of the tv program, and i will find it for you")

def custom_command(update, context):
    update.message.reply_text('This is a custom command!')

def handle_response(text: str) -> str:

    split = text.split()
    search_term = ''
    for i in range(1, len(split)):
        search_term += split[i] + ' '
    search_term = search_term.rstrip()
    if split[0] == 'search':
        response = requests.get(url, headers=keys.headers, params={"q": search_term})
        data = json.loads(response.text)
        formatted_data = json.dumps(data, indent=4)
        data_dict = json.loads(formatted_data)
        responses = data_dict["d"]
        movies_info = []

        if response.status_code == 200:
            for movie in responses:
                try:

                    if movie["qid"] == 'tvSeries':
                        info = "Title: " + movie["l"] + "\n" + 'kind: ' + movie["qid"] + "\n" + "Year: "\
                               + movie["yr"] + "\n" + 'Starring: ' + movie["s"] + "\n" + movie["i"]["imageUrl"]
                    else:
                        info = "Title: " + movie["l"] + "\n" + 'kind: ' + movie["qid"] +  "\n" + 'Starring: ' +  movie["s"] \
                               + "\n" \
                               + movie["i"]["imageUrl"]
                    movies_info.append(info)

                except:
                    pass

            if movies_info:
                for x in range(len(movies_info)):

                    return movies_info[x]
            else:
                return 'No movies found.'
        else:
            return "The bot can't call the API"

def handle_message(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    if message_type == 'group':
        if '@mrxangbot' in text:
            new_text = text.replacec('@searchProgramBot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    update.message.reply_text(response)

def error(update, context):
    print(f'Update {update} caused error: {context.error}')

if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    #Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))


    #Messages
    dp.add_handler(MessageHandler(Filters.text,handle_message))

    #Errors
    dp.add_error_handler(error)

    #Run bot
    updater.start_polling(1.0)
    updater.idle()