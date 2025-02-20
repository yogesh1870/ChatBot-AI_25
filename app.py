from flask import Flask, render_template, request, session 
import google.generativeai as ai
import markdown
from google.generativeai.types.generation_types import StopCandidateException  # Import exception
from langdetect import detect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Samsung@753'

responses_dict = {
    'hii': 'Vanakkam! How can I assist you today?',
    'hello': 'Hello! Nalama?',
    'hey': 'Hey! Epdi irukinga?',
    'how': 'Epdi?',
    'fine': 'Super! Epdi help pannanum?',
    'good': 'Nalla vishayam! Enna help venum?',
    'bad': 'Kashtama iruku nu ninaikkiren. Ethachum help pannanuma?',
    'bye': 'Nandri! Marupadiyum sandhippom!',
    'goodbye': 'Poi vara vendum! Take care!',
    'thanks': 'Ungaluku nandri! Vera enna venum?',
    'thank': 'Nandri! Vera enna venum?',
    'thank you':'paravalla, ithu en kadamai !',
    'please': 'Sari! Enna help venum?',
    'sorry': 'Parava illa! Marakka vendam.',
    'yes': 'Amaam! Enna venum?',
    'no': 'Sari, vera ethachum kelvi iruka?',
    'ok': 'Sari! Vera edhavadhu help venuma?',
    'okay': 'Seri! Enna seiyalaam?',
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
    current_msg = f'You : {user_message}'

    if not user_message:
        bot_response = "Edhavathu venumnaa kelunga  ?"
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
                    bot_response = "Sorry, neenga soldrathu puriyala....:("

            except StopCandidateException:
                bot_response = "Sorry, I cannot provide a response due to safety restrictions."
            except Exception as e:
                bot_response = "Sorry puriyala !...Konjam simple ah pesunga...Adha enakku theriyala ! :("

        try:
            detected_lang = detect(bot_response)
            bot_response_language = "ta-IN" if detected_lang == "ta" else "en-US"
        except:
            bot_response_language = "Unknown"

    if 'activity_log' not in session:
        session['activity_log'] = []
    
    session['activity_log'].append({"s_no": len(session['activity_log']) + 1, "message": user_message})
    session.modified = True
    
    return render_template('index.html', bot_response=bot_response, user_response=current_msg, 
                           activity_log=session['activity_log'], bot_response_language=bot_response_language)

    
if __name__ == '__main__':
    app.run(debug=True)
