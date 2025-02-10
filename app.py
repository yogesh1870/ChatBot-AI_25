from flask import Flask, render_template, request,url_for


app = Flask(__name__)


responses_dict={'hii':'Hello..How can i Help you ?','bye':'Thank you for using me...Good bye'}

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = None
    bot_response = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        temp_input=user_input.lower()
        bot_response=responses_dict[temp_input]


    return render_template("index.html", user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
