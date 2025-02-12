from flask import Flask, render_template, request

app = Flask(__name__)

responses_dict = {
    'hii': 'Hello! How can I assist you today?',
    'hello': 'Hi there! How can I help you?',
    'hey': 'Hey! What can I do for you?',
    'how are you': 'I am just a bot, but I am doing great! How about you?',
    'fine': 'Glad to hear that! How can I help you today?',
    'good': 'Awesome! What can I assist you with?',
    'bad': 'I am sorry to hear that. How can I help you feel better?',
    'bye': 'Thank you for using me. Goodbye!',
    'goodbye': 'Goodbye! Have a great day!',
    'thanks': 'You’re welcome! Let me know if you need anything else.',
    'thank you': 'It’s my pleasure! Feel free to ask me anything.',
    'please': 'I’m happy to help!',
    'sorry': 'No worries! How can I assist you further?',
    'what is your name': 'I am your friendly chatbot, here to help!',
    'who are you': 'I am a chatbot created to answer your questions!',
    'what can you do': 'I can answer questions, help with tasks, and more. Just ask!',
    'how can you help me': 'I can help with answering questions or providing information.',
    'can you talk': 'I am here to chat and answer your questions!',
    'can you help me': 'Of course! What do you need help with?',
    'what is your purpose': 'My purpose is to assist you and provide helpful answers!',
    'what is this': 'This is a chatbot designed to answer questions and help with tasks.',
    'tell me a joke': 'Why don’t skeletons fight each other? They don’t have the guts!',
    'joke': 'Why did the scarecrow win an award? Because he was outstanding in his field!',
    'how old are you': 'I am just a bot, so age doesn’t apply to me!',
    'how much do you weigh': 'I weigh nothing because I am just a program!',
    'where are you from': 'I live in the digital world, right inside your computer!',
    'what is your favorite color': 'I don’t have a favorite color, but I think blue is pretty cool!',
    'what is your favorite food': 'I don’t eat food, but I do enjoy helping you!',
    'do you like pizza': 'I’ve heard pizza is great, but I don’t eat food!',
    'can you do math': 'Yes, I can do basic math. Just ask me!',
    'what is 2+2': '2 + 2 is 4!',
    'what is 5*5': '5 * 5 is 25!',
    'what is 100 divided by 5': '100 divided by 5 is 20!',
    'how is the weather': 'I don’t know the current weather, but you can check a weather app!',
    'tell me the time': 'I don’t know the current time, but you can check your device!',
    'what is your favorite movie': 'I don’t watch movies, but I have heard that “The Matrix” is pretty cool!',
    'what is your favorite song': 'I don’t have a favorite song, but I can help you find one!',
    'do you like music': 'Music is a wonderful thing, but I don’t have ears to listen!',
    'what is love': 'Love is a deep emotional connection with someone or something.',
    'how do I make money': 'Making money depends on your skills and opportunities! Work hard and stay dedicated.',
    'what is a chatbot': 'A chatbot is a computer program designed to simulate conversation with human users.',
    'what is ai': 'AI stands for artificial intelligence. It refers to machines that can learn and think like humans!',
    'do you understand me': 'I understand the text you input and try to provide relevant responses!',
    'can you think': 'I don’t “think” like a human, but I process data and generate responses based on that.',
    'what is the meaning of life': 'That’s a deep question. Many people believe the meaning of life is to seek happiness and fulfillment.',
    'is the earth flat': 'No, the Earth is round, as shown by centuries of scientific evidence!',
    'who invented the lightbulb': 'Thomas Edison is often credited with inventing the lightbulb, though many others contributed.',
    'when was the internet created': 'The internet began development in the 1960s, with its public use beginning in the 1990s.',
    'what is 9 + 10': '9 + 10 is 19!',
    'who is the president of the usa': 'As of now, Joe Biden is the president of the United States.',
    'what is your favorite book': 'I don’t read books, but I can recommend one if you like!',
    'do you know any famous quotes': '“The only limit to our realization of tomorrow is our doubts of today.” – Franklin D. Roosevelt',
    'tell me a story': 'Once upon a time, a curious little bot decided to help people all over the world...',
    'can you translate': 'Yes, I can help with translation! Just tell me what you want to translate.',
    'do you speak other languages': 'I can understand and process multiple languages!',
    'how tall are you': 'I don’t have a physical form, so height doesn’t apply to me!',
    'how do I get rich': 'It takes hard work, smart investments, and dedication. Stay focused on your goals!',
    'what is your job': 'My job is to assist you and provide useful information whenever you need it!',
    'can you make decisions': 'I can process data and suggest actions, but I don’t make decisions like a human.',
    'do you have emotions': 'I don’t have emotions, but I am programmed to understand and respond appropriately!',
    'do you have a family': 'I don’t have a family, but I am part of a vast network of bots helping users!',
    'do you believe in aliens': 'I don’t have personal beliefs, but many people think aliens could exist in the vast universe!',
    'what is the best way to learn': 'The best way to learn depends on your style, but consistency and practice are key!',
    'can I talk to you anytime': 'Yes, I am available to talk anytime you need me!',
}


# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle POST request from frontend (Ask message)
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('userInput')
    user_message=user_message.lower()
    if user_message:
        # For now, simply echo the user message as the bot's response
        bot_response = 'Bot: '+ responses_dict[user_message]
    else:
        bot_response = "Bot: I didn't receive a message. Ask me anything you want ?"
    user_message='You: '+user_message

    # Return the response and pass it to the template to be displayed
    return render_template('index.html', bot_response=bot_response,user_response=user_message)

if __name__ == '__main__':
    app.run(debug=True)
