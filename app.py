from flask import Flask, render_template, request, redirect
import requests
import sqlite3

app = Flask(__name__) 
api_key = "ENTER YOUR tmdb_key HERE"

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        rating REAL,
        overview TEXT,
        poster_path TEXT,
        tmdb_id INTEGER
    )
''')
    conn.commit()
    conn.close()

init_db()

@app.route('/favorite/add', methods=['POST'])
def add_favorite():
    title = request.form.get('title')
    rating = request.form.get('rating')
    overview = request.form.get('overview')
    poster_path = request.form.get('poster_path')
    tmdb_id = request.form.get('tmdb_id')

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO favorites (title, rating, overview, poster_path, tmdb_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, rating, overview, poster_path, tmdb_id))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/favorites')
def favorites():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM favorites')
    movies = cursor.fetchall()
    conn.close()
    return render_template('favorites.html', movies=movies)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')

    if not query:
        return render_template('index.html')

    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    response = requests.get(url)
    data = response.json()

    movies = data['results']
    for movie in movies:
        movie['vote_average'] = round(movie['vote_average'], 1)

    return render_template('results.html', movies=movies, query=query)

if __name__ == '__main__':
    app.run(debug=True)