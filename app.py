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
    'what': 'Enna venum?',
    'who': 'Yaar neenga?',
    'when': 'Eppo?',
    'where': 'Enga?',
    'which': 'Edhu?',
    'why': 'En?',
    'today': 'Indru nal nalla iruka!',
    'tomorrow': 'Naalai nalla dhinam!',
    'yesterday': 'Netru oru nalla nal!',
    'friend': 'Ungal friend naan!',
    'family': 'Kudumbam dhan mukkiyam!',
    'love': 'Kadhal oru azhagaana feeling!',
    'happy': 'Santhosama irunga!',
    'sad': 'Kadupa padadha, ellam nallathuku dhan!',
    'angry': 'Kobama? Konjam amaidhiya irunga!',
    'bored': 'Vera ethachum pesalama?',
    'hungry': 'Pasikudha? Ethachum saapidu!',
    'thirsty': 'Thannir kudinga!',
    'sleepy': 'Thoongitu rest edunga!',
    'busy': 'Busy ah? Velai theerthu pesalam!',
    'tired': 'Relax pannunga!',
    'confused': 'Edhavadhu doubt ah?',
    'surprised': 'Aiyo! Nalla news ah?',
    'worried': 'Kavalai vendaam!',
    'excited': 'Sema santhosam!',
    'scared': 'Bayapada vendaam!',
    'joke': 'Sirikka oru joke sollava?',
    'morning': 'Kalai vanakkam!',
    'afternoon': 'Madhiya vanakkam!',
    'evening': 'Malai vanakkam!',
    'night': 'Iravu vanakkam!',
    'eat': 'Saapadu ready!',
    'drink': 'Neenga enna kudikiringa?',
    'coffee': 'Filter coffee saaptiya?',
    'tea': 'Chai venuma?',
    'water': 'Thanni kudichacha?',
    'hot': 'Sema veppa iruku!',
    'cold': 'Kulir irukku!',
    'rain': 'Mazhai adikuthu!',
    'sun': 'Sema veyil!',
    'wind': 'Kaathu adikuthu!',
    'money': 'Panam dhan mukkiyam!',
    'rich': 'Panakkaarana?',
    'poor': 'Ella vishayamum nallathaa irukkum!',
    'job': 'Enna velai pakkuringa?',
    'work': 'Vela busy ah iruka?',
    'study': 'Padikiringala?',
    'exam': 'Exam epdi panni irukeenga?',
    'mark': 'Nalla mark vanguninga?',
    'pass': 'Super! Thunai vazhthukkal!',
    'fail': 'Paravayilla, next time try pannu!',
    'school': 'Enga school padichinga?',
    'college': 'Enga college?',
    'bus': 'Enga poganum bus la?',
    'train': 'Train time pathirukinga?',
    'bike': 'Enna bike use pandringa?',
    'car': 'Enna car pudikum?',
    'road': 'Sariyaa traffic irukku!',
    'phone': 'Enna phone use pandringa?',
    'whatsapp': 'WhatsApp la pesalama?',
    'facebook': 'Facebook la active ah?',
    'instagram': 'Insta reel podriya?',
    'youtube': 'YouTube la enna pakuringa?',
    'song': 'Enna song pidikkum?',
    'dance': 'Dance panna theriyuma?',
    'movie': 'Cinema pakuringala?',
    'hero': 'Tamil cinema hero yaru pidikkum?',
    'villain': 'Villain yaru pidikkum?',
    'cricket': 'Cricket pathingala?',
    'football': 'Football vilaiyadriya?',
    'chess': 'Chess vilaiyadriya?',
    'running': 'Running exercise pannunga!',
    'gym': 'Gym poi body build panriya?',
    'health': 'Health mukkiyam!',
    'medicine': 'Marunthu saptiya?',
    'doctor': 'Doctor kita poi check-up senjirukingala?',
    'hospital': 'Hospital busy ah irukku!',
    'temple': 'Kovil ku pona?',
    'church': 'Church ku pona?',
    'mosque': 'Masjid la prarthanai senjacha?',
    'festival': 'Enna festival celebrate pandringa?',
    'pongal': 'Pongal nalla celebrate panniya?',
    'diwali': 'Diwali ku crackers vanguninga?',
    'newyear': 'Happy New Year!',
    'birthday': 'Piranthanaal nalvaazhthukkal!',
    'marriage': 'Kalyanam epdi nadandhuchu?',
    'life': 'Vaazhkai oru journey!',
    'death': 'Pirappuum maraippum sathiyam!',
    'truth': 'Unmai eppovum veliyeru!',
    'lie': 'Poi solradhu thappu!',
    'King':'Virat Kohli',
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

    activity_log.append({"s_no": len(activity_log) + 1, "message": user_message})

    return render_template('index.html', bot_response=bot_response, user_response=current_msg, activity_log=activity_log)


if __name__ == '__main__':
    app.run(debug=True)
