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

@app.route("/search", methods=['POST'])
def search_pokemon():
    pokemon_name = request.form.get('pokemon_name','').strip().lower()
    
    if not pokemon_name:
        flash("Por favor, ingresa un nombre de Pokémon", "error")
        return redirect(url_for("index"))

    try:
        resp = requests.get(f"{API}{pokemon_name}", timeout=5)
    except requests.RequestException:
        flash("Error al conectar con la API de Pokémon.", "error")
        return redirect(url_for("index"))

    if resp.status_code != 200:
        flash(f"Pokémon '{pokemon_name}' no encontrado.", "error")
        return redirect(url_for("index"))

    pokemon_data = resp.json()

    pokemon_info = {
        "id": pokemon_data.get("id"),
        "name": pokemon_data.get("name", "").title(),
        "sprite": pokemon_data.get("sprites", {}).get("front_default"),
        "types": [t["type"]["name"].title() for t in pokemon_data.get("types", [])],
        "abilities": [a["ability"]["name"].replace('-', ' ').title() for a in pokemon_data.get("abilities", [])],
        "stats": {s["stat"]["name"].replace('-', ' ').title(): s["base_stat"] for s in pokemon_data.get("stats", [])}
    }

    return render_template("pokemon.html", pokemon=pokemon_info)

if __name__ == '__main__':
    app.run(debug=True)