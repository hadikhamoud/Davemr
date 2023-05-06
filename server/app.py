from flask import Flask, jsonify, send_from_directory, session
from flask import request
from flask_cors import CORS
import os
from flask_talisman import Talisman
from flask_session import Session
from uuid import uuid4

from manager import GraphManager


#initializing FLASK variables
app = Flask(__name__, static_url_path='', static_folder='Dave-frontend/buildMe')
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


#for development, we use flask_cors, and for production on Heroku, we use
#flask Talisman to enforce https on the app level
CORS(app)
#Talisman(app, content_security_policy=None)


@app.before_request
def load_manager():
    if 'manager_id' not in session:
        session['manager_id'] = str(uuid4())
    if 'managers' not in session:
        session['managers'] = {}
    if session['manager_id'] not in session['managers']:
        session['managers'][session['manager_id']] = GraphManager()


def get_manager():
    return session['managers'][session['manager_id']]





#change the given book
@app.route('/ChangeBook',methods=["POST"])
def change_book():
    chosen_book_number = int(request.json["Book"])
    get_manager().set_book(choice = chosen_book_number)

    return jsonify({
        "Book": "Book Changed"
    })




@app.route('/Addnote', methods=['POST'])
def add_note():
    text = request.json["text"]
    response_data = get_manager().get_graphs_and_scores(text = text, start_rank= 1, num_graphs = 3)
    return jsonify(response_data)



#same approach as above but for 4,5, and 6th graphs
@app.route('/RestOfNotes',methods=['POST'])
def get_rest_of_notes():
    response_data = get_manager().get_graphs_and_scores(start_rank= 4, num_graphs = 3)
    return jsonify(response_data)



#reset all elements for scoring
@app.route('/reset', methods=['POST'])
def reset_all():
    get_manager().clear_all()
    return jsonify({
        "reset": "Reset Successful"
    })


#serve main page
@app.route('/')
def serve():
    return send_from_directory(app.static_folder,'index.html')




if __name__ == "__main__": 
     app.run(host = '0.0.0.0',debug=False, port=os.environ.get('PORT', 5000))


