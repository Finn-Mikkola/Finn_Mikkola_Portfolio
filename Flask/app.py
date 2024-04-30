from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import pandas as pd
from random import randrange
import random
import requests
import json

#Loading in data from pokemocard api
api_key = '7e3525e3-aae9-475a-9572-7bc8eaa0f725'
base_url = 'https://api.pokemontcg.io/v2/cards/'

params = {
    'apiKey': api_key,
}

response = requests.get(base_url, params = params)
if response.status_code == 200:
    # Print the JSON response
    data = response.json()
    with open('pokemon_cards.json', 'w') as json_file:
        json.dump(data,json_file, indent = 4)
    print('json updated')
else:
    print("Error:", response.status_code)
    
cards_list = data['data']
#Turn data in pandas dataframe
df = pd.DataFrame(cards_list)

#Drop columns that are not needed / dont know what they do
drop_columns = ['supertype', 'subtypes', 'legalities','images','tcgplayer','rules','regulationMark']
df.drop(drop_columns, axis = 1, inplace = True)
df.columns


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)  # Corrected method name
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Create the table schemas
class PokemonCards(db.Model):
    __tablename__ = 'PokemonCards'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    level = db.Column(db.String(50))
    hp = db.Column(db.String(50))
    types = db.Column(db.TEXT)
    evolvesFrom = db.Column(db.String(50))
    abilities = db.Column(db.TEXT)
    attacks = db.Column(db.TEXT)
    weaknesses = db.Column(db.TEXT)
    resistances = db.Column(db.TEXT)
    retreatCost = db.Column(db.TEXT)
    convertedRetreatCost = db.Column(db.TEXT)
    set = db.Column(db.TEXT)
    number = db.Column(db.TEXT)
    artist = db.Column(db.TEXT)
    rarity = db.Column(db.TEXT)
    flavorText = db.Column(db.TEXT)
    nationalPokedexNumbers = db.Column(db.String(50))
    cardmarket = db.Column(db.TEXT)
    evolvesTo = db.Column(db.String(50))
    number_in_stock = db.Column(db.Integer)
    price = db.Column(db.Float)


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_name = User.query.filter_by(username=username.data).first()

        if existing_user_name:
            raise ValidationError("That username already exists. Please choose a different one.")
        
class Purchases(db.Model):
    __tablename__ = 'Purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    card_id = db.Column(db.String(50), db.ForeignKey('PokemonCards.id'))
    card_name = db.Column(db.String(50))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

# Create all database tables within an application context
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print("An error occurred:", e)
    
#Load data into PokemonCards table
with app.app_context():
    for index, row in df.iterrows():
        # Access the values of each column in the current row
        id = str(row['id'])
        name = str(row['name'])
        level = str(row['level'])
        hp = str(row['hp'])
        types = str(row['types'])
        evolvesFrom = str(row['evolvesFrom'])
        abilities = str(row['abilities'])
        attacks = str(row['attacks'])
        weaknesses = str(row['weaknesses'])
        resistances = str(row['resistances'])
        retreatCost = str(row['retreatCost'])
        convertedRetreatCost = str(row['convertedRetreatCost'])
        set = str(row['set'])
        number = str(row['number'])
        artist = str(row['artist'])
        rarity = str(row['rarity'])
        flavorText = str(row['flavorText'])
        nationalPokedexNumbers = str(row['nationalPokedexNumbers'])
        cardmarket = str(row['cardmarket'])
        evolvesTo = str(row['evolvesTo'])
        number_in_stock = randrange(10)
        price = round(random.uniform(1,100), 2)
    
    
        # Create a new PokemonCards instance
        new_pokemon = PokemonCards(id=id, name=name, level=level, hp=hp, types=types, evolvesFrom=evolvesFrom, abilities=abilities,
                            attacks=attacks, weaknesses=weaknesses, resistances=resistances, retreatCost=retreatCost,
                            convertedRetreatCost=convertedRetreatCost, set=set, number=number, artist=artist, rarity=rarity,
                            flavorText=flavorText,
                            nationalPokedexNumbers=nationalPokedexNumbers, cardmarket=cardmarket,
                            evolvesTo=evolvesTo, number_in_stock=number_in_stock, price=price)

        # Add the instance to the database session
        db.session.add(new_pokemon)
        try:
            db.session.commit()
        except:
            continue
        # print(count)

    # Commit the changes to the database
    
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form = form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/directory')
def directory():
    return render_template('directory.html')



@app.route('/directory/pokemon_id', methods=['GET', 'POST'])
@login_required
def get_pokemon_by_id():
    if request.method == 'POST':
        pokemon_id = request.form.get('pokemon_id')
        try:
            pokemon = PokemonCards.query.filter_by(id=pokemon_id).first()
            if pokemon:
                pokemon_info = {
                    'pokemon_id': pokemon.id,
                    'name': pokemon.name,
                    'rarity': pokemon.rarity,
                    '# in stock': pokemon.number_in_stock,
                    'type': pokemon.types,
                    'price': pokemon.price
                }
                return jsonify(pokemon_info)
            else:
                return jsonify({'error': 'Pokémon not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('pokemon_id.html')
    

@app.route('/directory/pokemon_name', methods=['GET', 'POST'])
@login_required
def get_pokemon_by_name():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        try:
            pokemons = PokemonCards.query.filter_by(name=pokemon_name).all()
            if pokemons:
                pokemon_info = []
                for pokemon in pokemons:
                    pokemon_info.append({
                        'pokemon_id': pokemon.id,
                        'name': pokemon.name,
                        'rarity': pokemon.rarity,
                        '# in stock': pokemon.number_in_stock,
                        'type': pokemon.types,
                        'price': pokemon.price
                    })
                return jsonify(pokemon_info)
            else:
                return jsonify({'error': 'Pokémon not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('pokemon_name.html')
    
    
@app.route('/directory/pokemon_rarity', methods=['GET', 'POST'])
@login_required
def get_pokemon_by_rarity():
    if request.method == 'POST':
        rarity = request.form.get('rarity')
        try:
            pokemons = PokemonCards.query.filter_by(rarity=rarity).all()
            if pokemons:
                pokemon_info = []
                for pokemon in pokemons:
                    pokemon_info.append({
                        'pokemon_id': pokemon.id,
                        'name': pokemon.name,
                        'rarity': pokemon.rarity,
                        '# in stock': pokemon.number_in_stock,
                        'type': pokemon.types,
                        'price': pokemon.price
                    })
                return jsonify(pokemon_info)
            else:
                return jsonify({'error': 'No Pokémon found with the selected rarity'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('pokemon_rarity.html')
    
@app.route('/directory/pokemon_price', methods=['GET', 'POST'])
@login_required
def get_pokemon_by_price():
    if request.method == 'POST':
        min_price = float(request.form.get('min_price'))
        max_price = float(request.form.get('max_price'))
        try:
            pokemons = PokemonCards.query.filter(PokemonCards.price.between(min_price, max_price)).all()
            if pokemons:
                pokemon_info = []
                for pokemon in pokemons:
                    pokemon_info.append({
                        'pokemon_id': pokemon.id,
                        'name': pokemon.name,
                        'rarity': pokemon.rarity,
                        '# in stock': pokemon.number_in_stock,
                        'type': pokemon.types,
                        'price': pokemon.price
                    })
                return jsonify(pokemon_info)
            else:
                return jsonify({'error': 'No Pokémon found within the specified price range'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('pokemon_price.html')
    

@app.route('/search_by_type', methods=['GET', 'POST'])
@login_required
def search_by_type():
    if request.method == 'POST':
        search_type = request.form.get('type')
        
        # Query the PokemonCards table to find Pokémon by type
        pokemons = PokemonCards.query.filter(PokemonCards.types.ilike(f'%{search_type}%')).all()
        
        # Convert the results to JSON format
        results = []
        for pokemon in pokemons:
            results.append({
                'pokemon_id': pokemon.id,
                'name': pokemon.name,
                'rarity': pokemon.rarity,
                '# in stock': pokemon.number_in_stock,
                'type': pokemon.types
            })
        
        return jsonify(results)
    else:
        # Fetch all unique Pokémon types from the database
        pokemon_types = db.session.query(PokemonCards.types).distinct().all()
        
        # Flatten the list of tuples into a list of strings
        pokemon_types = [type[0] for type in pokemon_types]
        
        return render_template('search_by_type.html', pokemon_types=pokemon_types)


    

@app.route('/purchase_page')
@login_required
def purchase_page():
    return render_template('purchase.html')


@app.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase_pokemon_card():
    pokemon_id = request.form.get('pokemon_id')
    
    # Find the Pokémon card by ID
    pokemon_card = PokemonCards.query.get(pokemon_id)
    if pokemon_card is None:
        return jsonify({'error': 'Pokémon card not found'}), 404
    
    try:
        # Create a new purchase row in the Purchases table
        purchase = Purchases(user_id=current_user.id, card_id=pokemon_card.id, card_name=pokemon_card.name)
        db.session.add(purchase)
        db.session.commit()
        
        # Pass the directory link to the template
        directory_link = url_for('directory')
        
        # Render the purchase confirmation template
        return render_template('purchase_confirmation.html', success_message=f'You have successfully purchased the Pokémon card {pokemon_card.name} ID: {pokemon_card.id}', directory_link=directory_link)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/user_purchases', methods=['GET'])
@login_required
def user_purchases():
    user_id = current_user.id
    
    # Fetch the user's username
    username = current_user.username
    
    # Fetch the user's purchases from the Purchases table
    user_purchases = Purchases.query.filter_by(user_id=user_id).all()
    
    # Convert purchases to JSON format
    purchases_json = []
    for purchase in user_purchases:
        purchase_info = {
            'purchase_id': purchase.id,
            'pokemon_id': purchase.card_id,
            'card_name': purchase.card_name,
            'user_id': purchase.user_id
        }
        purchases_json.append(purchase_info)
    
    # Combine username and purchases into a dictionary
    user_data = {
        'username': username,
        'purchases': purchases_json
    }
    
    return jsonify(user_data)

    

if __name__ == '__main__':
    app.run(debug=True)
