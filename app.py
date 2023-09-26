from flask import Flask , render_template , request , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

    
class User(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        username = db.Column(db.String(200), nullable = False)
        email = db.Column(db.String(200), nullable = False)
        password = db.Column(db.String(200), nullable = False)
        user_decks = relationship('Deck')
        def __repr__(self):
            return '<User %r>' % self.username

class Deck(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_score = db.Column(db.Integer, nullable = False)
        cards = relationship('Card' , cascade="all, delete-orphan")  
        # delete orphan cards when deck is deleted
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        deck_user = relationship('User', overlaps="user_decks")

class Card(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        front = db.Column(db.String(200), nullable = False)
        back = db.Column(db.String(200), nullable = False)
        card_score = db.Column(db.Integer, nullable = False , default = 0)
        last_reviewed = db.Column(db.DateTime , default = datetime.now())
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
        #card_deck = relationship('Deck', overlaps="cards" )

if not os.path.exists("./instance/flashcard.db"):
    with app.app_context():
            db.create_all()
            Users = User.query.all()
            print(Users)
            if not Users:
                print("No Users")
                U1 = User(username = "demo", email = "demo@demo.com", password = "demo")
                db.session.add(U1)
                D1 = Deck(name = "demo_deck1", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                D2 = Deck(name = "demo_deck2", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                D3 = Deck(name = "demo_deck3", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                D4 = Deck(name = "demo_deck4", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                D5 = Deck(name = "demo_deck5", last_reviewed = datetime.now(), deck_score = 0, user_id = 1)
                C1 = Card(front = "demo_front1", back = "demo_back1", card_score = 0, last_reviewed = datetime.now(), deck_id = 1)
                C2 = Card(front = "demo_front2", back = "demo_back2", card_score = 0, last_reviewed = datetime.now(), deck_id = 1)
                C3 = Card(front = "demo_front3", back = "demo_back3", card_score = 0, last_reviewed = datetime.now(), deck_id = 1)
                C4 = Card(front = "demo_front4", back = "demo_back4", card_score = 0, last_reviewed = datetime.now(), deck_id = 1)
                C5 = Card(front = "demo_front5", back = "demo_back5", card_score = 0, last_reviewed = datetime.now(), deck_id = 2)
                C6 = Card(front = "demo_front6", back = "demo_back6", card_score = 0, last_reviewed = datetime.now(), deck_id = 2)
                C7 = Card(front = "demo_front7", back = "demo_back7", card_score = 0, last_reviewed = datetime.now(), deck_id = 2)
                C8 = Card(front = "demo_front8", back = "demo_back8", card_score = 0, last_reviewed = datetime.now(), deck_id = 2)
                db.session.add(D1)
                db.session.add(D2)
                db.session.add(D3)
                db.session.add(D4)
                db.session.add(D5)
                db.session.add(C1)
                db.session.add(C2)
                db.session.add(C3)
                db.session.add(C3)
                db.session.add(C4)
                db.session.add(C5)
                db.session.add(C6)
                db.session.add(C7) 
                db.session.add(C8)
                db.session.commit()            

@app.route('/signup',methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username,email=email,password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding new user'

    return render_template('signup.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        users=User.query.all()
        for user in users:
            if user.email == email and user.password == password :
                print("inside if condition")
                return redirect(f'/user_dashboard/{user.id}')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/user_dashboard/<int:user_id>', methods=['GET'])
def user_dashboard(user_id):
     user = User.query.get_or_404(user_id)
     print(user.user_decks)
     return render_template('user_dashboard.html', user = user)

@app.route('/update_deck/<int:deck_id>', methods=['GET', 'POST'])
def update_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if request.method == 'POST':
        deck.name = request.form['deck_name']
        deck.last_reviewed = datetime.now()
        try:
            db.session.add(deck)
            db.session.commit()
            return redirect(f'/user_dashboard/{deck.deck_user.id}')
        except:
            return 'There was an issue updating deck'
    return render_template('update_deck.html', deck = deck)

@app.route('/add_deck/<int:user_id>', methods=['GET', 'POST'])
def add_deck(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        print(request.form)
        print("gokul")
        deck_name = request.form['deck_name']
        deck = Deck(name = deck_name, last_reviewed = datetime.now(), deck_score = 0, user_id = user_id)
        try:
            db.session.add(deck)
            db.session.commit()
            return redirect(f'/user_dashboard/{user_id}')
        except:
            return 'There was an issue adding new deck'
        
    return render_template('add_deck.html', user = user )

@app.route('/delete_deck/<int:deck_id>' )
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    user_id = deck.deck_user.id
    print(user_id)
    try:
        db.session.delete(deck)
        db.session.commit()
        return redirect(f'/user_dashboard/{deck.deck_user.id}')
    except Exception as e:
        print(e)
        return 'There was an issue deleting deck'

@app.route('/add_card/<int:deck_id>', methods=['GET', 'POST'])
def add_card(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    
    if request.method == 'POST':
        front = request.form['front']
        back = request.form['back']
        card = Card(front=front, back=back, deck_id=deck.id)
        
        try:
            db.session.add(card)
            db.session.commit()
            return redirect(f'/user_dashboard/{deck.deck_user.id}')
        except:
            return 'There was an issue adding the card'
    
    return render_template('add_card.html', deck=deck)

@app.route('/review_cards/<int:deck_id>/<int:card_id>', methods=['GET'])
def review_cards(deck_id, card_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = deck.cards

    # Find the index of the current card by matching card_id
    current_card_index = None
    for i, card in enumerate(cards):
        if card.id == card_id:
            current_card_index = i
            break

    # Check if the current card is the last card in the deck
    is_last_card = current_card_index == len(cards) - 1

    # Get the current card and the next card (if not the last card)
    current_card = cards[current_card_index]
    next_card = cards[current_card_index + 1] if not is_last_card else None

    return render_template('review_cards.html', deck=deck, current_card=current_card, next_card=next_card, is_last_card=is_last_card)



if __name__ == '__main__':
    
    app.run(debug=True)

