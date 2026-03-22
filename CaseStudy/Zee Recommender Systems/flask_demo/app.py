"""
Simple Flask Demo Application
Demonstrates GET and POST methods
"""

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Sample data storage (in-memory)
movies = [
    {"id": 1, "title": "Toy Story", "rating": 4.5},
    {"id": 2, "title": "Star Wars", "rating": 4.8},
    {"id": 3, "title": "Titanic", "rating": 4.2}
]

# HTML Template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Demo - Movie API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .endpoint { background: #f4f4f4; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #e0e0e0; padding: 2px 6px; border-radius: 3px; }
        form { background: #e8f4e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
        input, button { padding: 10px; margin: 5px; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <h1>🎬 Flask Demo - Movie API</h1>
    
    <h2>Available Endpoints:</h2>
    
    <div class="endpoint">
        <strong>GET /</strong> - Home page (this page)
    </div>
    
    <div class="endpoint">
        <strong>GET /movies</strong> - Get all movies
    </div>
    
    <div class="endpoint">
        <strong>GET /movies/&lt;id&gt;</strong> - Get movie by ID
    </div>
    
    <div class="endpoint">
        <strong>POST /movies</strong> - Add a new movie (JSON body: title, rating)
    </div>
    
    <h2>Add a New Movie:</h2>
    <form action="/movies" method="post">
        <input type="text" name="title" placeholder="Movie Title" required>
        <input type="number" name="rating" placeholder="Rating (1-5)" step="0.1" min="1" max="5" required>
        <button type="submit">Add Movie</button>
    </form>
    
    <h2>Current Movies:</h2>
    <ul>
    {% for movie in movies %}
        <li><strong>{{ movie.title }}</strong> - Rating: {{ movie.rating }} ⭐</li>
    {% endfor %}
    </ul>
</body>
</html>
"""


# ============================================================
# GET METHODS
# ============================================================

@app.route('/')
def home():
    """Home page - GET method"""
    return render_template_string(HOME_TEMPLATE, movies=movies)


@app.route('/movies', methods=['GET'])
def get_movies():
    """Get all movies - GET method"""
    return jsonify({
        "status": "success",
        "count": len(movies),
        "movies": movies
    })


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie by ID - GET method"""
    movie = next((m for m in movies if m['id'] == movie_id), None)
    
    if movie:
        return jsonify({"status": "success", "movie": movie})
    else:
        return jsonify({"status": "error", "message": "Movie not found"}), 404


# ============================================================
# POST METHODS
# ============================================================

@app.route('/movies', methods=['POST'])
def add_movie():
    """Add a new movie - POST method"""
    
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    title = data.get('title')
    rating = data.get('rating')
    
    if not title or not rating:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: title and rating"
        }), 400
    
    # Create new movie
    new_movie = {
        "id": max(m['id'] for m in movies) + 1 if movies else 1,
        "title": title,
        "rating": float(rating)
    }
    
    movies.append(new_movie)
    
    # If form submission, redirect to home
    if not request.is_json:
        return render_template_string(HOME_TEMPLATE, movies=movies)
    
    return jsonify({
        "status": "success",
        "message": "Movie added successfully",
        "movie": new_movie
    }), 201


@app.route('/recommend', methods=['POST'])
def get_recommendation():
    """Get movie recommendation based on genre - POST method"""
    
    data = request.get_json()
    genre = data.get('genre', 'action')
    
    # Demo recommendation logic
    recommendations = {
        "action": ["Star Wars", "Die Hard", "Mad Max"],
        "comedy": ["Toy Story", "The Mask", "Liar Liar"],
        "drama": ["Titanic", "Forrest Gump", "Shawshank Redemption"]
    }
    
    return jsonify({
        "status": "success",
        "genre": genre,
        "recommendations": recommendations.get(genre.lower(), ["No recommendations found"])
    })


# ============================================================
# RUN THE APP
# ============================================================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Flask Demo Server Starting...")
    print("=" * 50)
    print("Open http://127.0.0.1:5000 in your browser")
    print("=" * 50)
    
    # Use host='0.0.0.0' for Docker compatibility
    app.run(debug=True, host='0.0.0.0', port=5000)
