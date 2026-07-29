from flask import Flask, render_template, request
import requests

app = Flask(__name__) #telling flask that my app lives in this file

api_key = "YOUR_TMDB_KEY"

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