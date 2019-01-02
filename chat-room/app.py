from flask import Flask, render_template, request
from conversation_manager import ConversationManager

app = Flask(__name__)

cm = ConversationManager()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/")
def get_bot_response():
    userText = request.args.get('msg')
    u_id = request.args.get('u_id')
    return str(cm.get_response(userText, u_id))


if __name__ == "__main__":
    app.run(port=8080, threaded=True, debug=False, host='0.0.0.0')