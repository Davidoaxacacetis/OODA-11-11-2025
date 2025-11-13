from flask import Flask, render_template, jsonify , request , redirect ,url_for,flash 
import requests

API = "https://pokeapi.co/api/v2/pokemon/"
app = Flask(__name__)
app.secret_key = "OODA"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/poke")
def poke():
    return render_template("pokemon.html")

@app.route("/search", methods=['GET','POST'])
def search_pokemon():
    pokemon_name = request.form.get('pokemon_name', '').strip().lower()
    if not pokemon_name:
        flash("Por favor, ingresa un nombre de Pokémon", "error")
        return redirect(url_for("index"))

    try:
        resp = requests.get(f"{API}{pokemon_name}", timeout=5)

        if resp.status_code == 200:
            pokemon_data = resp.json()

            pokemon_info = {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height']/10,
                'weight': pokemon_data['weight']/10,
                'sprites': pokemon_data['sprites']['front_default'],
                'abilities': [ability['ability']['name'] for ability in pokemon_data['abilities']],
            }

            return render_template("pokemon.html", pokemon=pokemon_info)

        else:
            flash("Pokémon no encontrado. Intenta de nuevo.", "error")
            return redirect(url_for("index"))
    except requests.RequestException:
        flash("Error al conectar con la API de Pokémon. Intenta más tarde.", "error")
        return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)