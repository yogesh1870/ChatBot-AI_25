from flask import Flask, render_template, request
import google.generativeai as ai
import markdown
from google.generativeai.types.generation_types import StopCandidateException  # Import exception

app = Flask(__name__)

activity_log = []
responses_dict = {
    'hii': 'Vanakkam! How can I assist you today?',
    'hello': 'Hello! Nalama?',
    'hey': 'Hey! Epdi irukinga?',
    'how are you': 'Naan nalla iruken! Neenga epdi irukeenga?',
    'fine': 'Super! Epdi help pannanum?',
    'good': 'Nalla vishayam! Enna help venum?',
    'bad': 'Kashtama iruku nu ninaikkiren. Ethachum help pannanuma?',
    'bye': 'Nandri! Marupadiyum sandhippom!',
    'goodbye': 'Poi vara vendum! Take care!',
    'thanks': 'Ungaluku nandri! Vera enna venum?',
    'thank you': 'Parava illai! Naan unga friend dhan!',
    'please': 'Sari! Enna help venum?',
    'sorry': 'Parava illa! Marakka vendam.'
}

API_KEY = 'AIzaSyALCOS1sIhzeZZW9Ol-n1kAwYNBh0quzW8'

ai.configure(api_key=API_KEY)
model = ai.GenerativeModel('gemini-pro')
chat = model.start_chat()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('userInput', '').strip()
    current_msg = f'You : a{user_message}'

    if not user_message:
        bot_response = "Please enter a valid message."
    else:
        user_message_lower = user_message.lower()

        # Check predefined responses
        bot_response = responses_dict.get(user_message_lower)

        # If not in dictionary, ask AI
        if bot_response is None:
            try:
                response = chat.send_message(user_message_lower)

                if response and response.candidates:
                    bot_response = response.candidates[0].content.parts[0].text
                    bot_response = markdown.markdown(bot_response)
                else:
                    bot_response = "Sorry, I couldn't understand that. Can you try rephrasing?"

            except StopCandidateException:
                bot_response = "Sorry, I cannot provide a response due to safety restrictions."
            except Exception as e:
                bot_response = "Oops! There was an error processing your request. Please try again later."

    activity_log.append({"s_no": len(activity_log) + 1, "message": user_message})

    return render_template('index.html', bot_response=bot_response, user_response=current_msg, activity_log=activity_log)


if __name__ == '__main__':
    app.run(debug=True)
