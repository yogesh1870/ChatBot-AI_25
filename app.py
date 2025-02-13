from flask import Flask, render_template, request
import google.generativeai as ai
import markdown

app = Flask(__name__)

activity_log=[]
responses_dict = {
    # Basic Greetings
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

model = ai.GenerativeModel('gemini-pro')  # Ensure this is the correct model
chat = model.start_chat()



# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle POST request from frontend (Ask message)
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('userInput')
    current_msg='You : '+user_message
    user_message=user_message.lower()
    l=responses_dict.keys()
    if user_message in l :
        bot_response = 'Bot : ' + responses_dict[user_message]
    elif user_message not in l:
        response = chat.send_message(user_message)


        bot_response  = response.candidates[0].content.parts[0].text

        x=markdown.markdown(bot_response)


    else:
        bot_response= 'Bot : I cannot get it what you mean...please try again other you want ? :('
    activity_log.append({"s_no": len(activity_log) + 1, "message": user_message})

    return render_template('index.html', bot_response=x,user_response=current_msg,activity_log=activity_log)

if __name__ == '__main__':
    app.run(debug=True)
