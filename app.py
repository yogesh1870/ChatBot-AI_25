from flask import Flask, render_template, request

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
    'sorry': 'Parava illa! Marakka vendam.',# Tamil Nadu Cinema & Songs
    'who is the superstar of tamil cinema': 'Thalaivar Rajinikanth!',
    'who is ulaganayagan': 'Kamal Haasan is called Ulaganayagan!',
    'who is the best tamil actor': 'It depends on your taste! Rajini, Kamal, Vijay, Ajith, Suriya, Dhanush—ellam mass!',
    'best tamil movies': 'Nayakan, Baasha, Anbe Sivam, Super Deluxe, Vikram, Kaithi, Soorarai Pottru!',
    'who is the best tamil director': 'Mani Ratnam, Lokesh Kanagaraj, Vetrimaaran, Shankar—ellam top class!',
    'who is thalapathy': 'Thalapathy Vijay!',
    'who is thala': 'Thala Ajith!',
    'who is rowdy baby': 'Rowdy Baby is a famous song from Maari 2!',
    'best tamil songs': 'Enjoy Enjaami, Vaathi Coming, Why This Kolaveri, Unnale Unnale!',
    'who is music director of tamil cinema': 'Ilaiyaraaja, A. R. Rahman, Anirudh, Yuvan Shankar Raja!',
    'best bgm in tamil': 'A.R. Rahman, Anirudh, Yuvan, and G.V. Prakash ellarum mass BGM specialists!',
    'who is mass hero in tamilnadu': 'Rajinikanth, Vijay, Ajith ellarum mass!',
    'latest tamil movies': 'Leo, Jailer, Ponniyin Selvan, Vikram!',
    'latest tamil songs': 'Kaavaalaa, Hukum, Rathamaarey!',
    'who is love king': 'STR (Simbu) is called the Love King!',

    # Tamil Nadu CM Details
    'who is the cm of tamilnadu': 'M. K. Stalin is the Chief Minister of Tamil Nadu (since 2021).',
    'who was the first cm of tamilnadu': 'C. Rajagopalachari was the first Chief Minister of Tamil Nadu.',
    'how many chief ministers tamilnadu had': 'Tamil Nadu has had 15 different Chief Ministers since independence.',
    'who is the best cm of tamilnadu': 'People often consider K. Kamaraj, M. G. Ramachandran (MGR), and J. Jayalalithaa as among the best CMs.',

    # Tamil Nadu General Knowledge
    'what is the capital of tamilnadu': 'Chennai!',
    'biggest city in tamilnadu': 'Chennai!',
    'largest district in tamilnadu': 'Viluppuram is the largest district in Tamil Nadu.',
    'smallest district in tamilnadu': 'Chennai is the smallest district in terms of area.',
    'who built brihadeeswarar temple': 'Raja Raja Chola I built the Brihadeeswarar Temple in Thanjavur!',
    'which is the famous food in tamilnadu': 'Sambar, Idli, Dosa, Pongal, Biryani!',
    'best places to visit in tamilnadu': 'Mahabalipuram, Kodaikanal, Ooty, Madurai Meenakshi Temple!',
    'which festival is famous in tamilnadu': 'Pongal, Deepavali, and Tamil New Year are famous festivals!',
    'what is tamilnadu famous for': 'Temples, Kollywood cinema, Kanjivaram sarees, Classical music, and IT sector!',

    # Jokes & Fun
    'tell me a tamil joke': 'Teacher: “2+2 evlo?” Student: “Teacher, 2 illaama irundha, vera ethum add panna mudiyuma?”',
    'funny tamil movie dialogue': '“Enna koduma sir idhu?” - Chandramukhi',

    # Math & General Knowledge
    'what is 5+5': '5 + 5 is 10!',
    'who discovered zero': 'Aryabhata is credited with the concept of zero.',
    'who invented computer': 'Charles Babbage is known as the Father of the Computer!',

    # Science & Technology
    'who invented electricity': 'Benjamin Franklin experimented with electricity!',
    'who is the father of the internet': 'Vint Cerf and Bob Kahn are considered the fathers of the internet!',

    # Logical & Philosophical
    'what is tamil': 'Tamil is one of the oldest languages in the world and is known for its rich literature!',
    'who wrote thirukkural': 'Thiruvalluvar!',
    'who is the best tamil poet': 'Subramania Bharathiyar!',

    # Tamil Nadu Sports
    'who is the best tamil cricketer': 'Ravichandran Ashwin and Dinesh Karthik are top cricketers from Tamil Nadu!',
    'best kabaddi player in tamilnadu': 'Ajay Thakur and Pardeep Narwal are well-known in Pro Kabaddi!',

    # Tamil Literature & Books
    'best tamil books': 'Ponniyin Selvan, Silappathikaram, Manimekalai!',
    'who is the best tamil writer': 'Sujatha, Kalki, Jeyamohan!',

    # Random Fun Questions
    'do you watch tamil movies': 'I can’t watch, but I know all the best Tamil movies!',
    'who is better, vijay or ajith': 'Both are amazing actors with unique styles!',
    'what is kollywood': 'Kollywood is the Tamil film industry, based in Chennai!',

    # Everyday Life & Advice
    'how to improve my tamil': 'Practice reading Tamil books and watching Tamil news!',
    'how to make tamil food': 'Start with simple recipes like idli, dosa, or sambar!',

    # Miscellaneous
    'best tamil web series': 'Suzhal, Auto Shankar, Finger Tip!',
    'who is tamilnadu richest person': 'Shiv Nadar, founder of HCL!',
    'best tamil actors for comedy': 'Vadivelu, Goundamani, Senthil, Santhanam!',
    'who is the best music director in tamil': 'Ilaiyaraaja and A.R. Rahman are legends!'



}



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
    else:
        bot_response= 'Bot : I cannot get it what you mean...please try again other you want ? :('
    activity_log.append({"s_no": len(activity_log) + 1, "message": user_message})

    return render_template('index.html', bot_response=bot_response,user_response=current_msg,activity_log=activity_log)

if __name__ == '__main__':
    app.run(debug=True)
