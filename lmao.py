import streamlit as st
from PIL import Image
import sqlite3
import bcrypt
from datetime import datetime
import os
import base64
from io import BytesIO

movies = [
    {
        "title": "Assassin",
        "year": 2023,
        "genre": "Action, Thriller",
        "rating": 7.4,
        "description": "An elite assassin embarks on a high-stakes mission, navigating a web of deception.",
        "detailed_summary": "In the high-stakes world of international espionage, an elite assassin faces unexpected challenges and must outsmart his enemies. With pulse-pounding action and a tightly woven plot, 'Assassin' takes viewers on a rollercoaster ride across the globe.",
        "director": "John Smith",
        "cast": ["Chris Evans", "Scarlett Johansson"],
        "box_office": "$350 million",
        "awards": ["Best Action Choreography"],
        "image": "images/assasin.jpeg"
    },
    {
        "title": "Black Panther",
        "year": 2018,
        "genre": "Action, Adventure, Sci-Fi",
        "rating": 7.3,
        "description": "The Black Panther must step up to lead his people and protect Wakanda from new threats.",
        "detailed_summary": "After the death of his father, T'Challa returns to Wakanda to assume the throne. But when a powerful enemy appears, the Black Panther must team up with allies to protect his kingdom and preserve his people's way of life.",
        "director": "Ryan Coogler",
        "cast": ["Chadwick Boseman", "Michael B. Jordan", "Lupita Nyong'o"],
        "box_office": "$1.34 billion",
        "awards": ["Academy Award for Best Original Score"],
        "image": "images/blackpanther.jpeg"
    },
    {
        "title": "Lord of War",
        "year": 2005,
        "genre": "Crime, Drama, Thriller",
        "rating": 7.6,
        "description": "A war arms dealer faces moral dilemmas as he builds a career in global arms trafficking.",
        "detailed_summary": "Yuri Orlov, an arms dealer, navigates the violent world of international arms sales. As he profits from global conflicts, he faces moral and personal conflicts that threaten his career and life.",
        "director": "Andrew Niccol",
        "cast": ["Nicolas Cage", "Ethan Hawke", "Jared Leto"],
        "box_office": "$72.6 million",
        "awards": ["Nominated for Best Screenplay"],
        "image": "images/lordofwar.jpeg"
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genre": "Comedy, Drama, Thriller",
        "rating": 8.6,
        "description": "A poor family schemes to infiltrate a wealthy household with unexpected consequences.",
        "detailed_summary": "The Kim family, struggling to make ends meet, infiltrates a wealthy household by posing as qualified professionals. A dark comedy ensues as secrets unravel, leading to unforeseen consequences in this social satire.",
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "box_office": "$266.9 million",
        "awards": ["Academy Awards for Best Picture, Best Director"],
        "image": "images/parasite.jpeg"
    },
    {
        "title": "Star Wars",
        "year": 1977,
        "genre": "Action, Adventure, Fantasy",
        "rating": 8.6,
        "description": "Luke Skywalker joins forces to rescue Princess Leia and defeat the evil Galactic Empire.",
        "detailed_summary": "Young farm boy Luke Skywalker embarks on a journey to become a Jedi and bring down the oppressive Galactic Empire. Alongside a band of rebels, he faces off against Darth Vader in an epic battle of good versus evil.",
        "director": "George Lucas",
        "cast": ["Mark Hamill", "Harrison Ford", "Carrie Fisher"],
        "box_office": "$775.4 million",
        "awards": ["Academy Award for Best Art Direction"],
        "image": "images/starwars.jpeg"
    },
    {
        "title": "Tesla",
        "year": 2020,
        "genre": "Biography, Drama",
        "rating": 5.0,
        "description": "A look at the life of Nikola Tesla, his inventions, and his visionary ideas.",
        "detailed_summary": "This biographical drama explores the visionary mind of Nikola Tesla, his struggles, his eccentricities, and his groundbreaking innovations. It also delves into his tumultuous relationships with Thomas Edison and J.P. Morgan.",
        "director": "Michael Almereyda",
        "cast": ["Ethan Hawke", "Kyle MacLachlan", "Eve Hewson"],
        "box_office": "$3.2 million",
        "awards": ["Nominated for Independent Spirit Award"],
        "image": "images/tesla.jpeg"
    },
    {
        "title": "Beauty and the Beast",
        "year": 2017,
        "genre": "Fantasy, Romance, Musical",
        "rating": 7.1,
        "description": "A young woman falls in love with a prince cursed to live as a beast.",
        "detailed_summary": "Belle, a bright, beautiful, and independent young woman, is taken prisoner by a beast in his castle. Despite her fears, she befriends the castle's enchanted staff and learns to look beyond the Beast's hideous exterior to recognize the true heart and soul of the Prince within.",
        "director": "Bill Condon",
        "cast": ["Emma Watson", "Dan Stevens", "Luke Evans"],
        "box_office": "$1.26 billion",
        "awards": ["Academy Award Nominee for Best Production Design"],
        "image": "images/beautyandthebeast.jpeg"
    },
    {
        "title": "Barbie",
        "year": 2023,
        "genre": "Comedy, Fantasy",
        "rating": 7.2,
        "description": "A doll living in 'Barbieland' is expelled for being less than perfect.",
        "detailed_summary": "In a colorful world where every day is perfect, Barbie finds herself facing an existential crisis that sends her on a journey of self-discovery in the real world.",
        "director": "Greta Gerwig",
        "cast": ["Margot Robbie", "Ryan Gosling", "Simu Liu"],
        "box_office": "$1.4 billion",
        "awards": ["Nominated for Golden Globe"],
        "image": "images/barbie.jpeg"
    },
    {
        "title": "Avatar",
        "year": 2009,
        "genre": "Sci-Fi, Adventure",
        "rating": 7.8,
        "description": "A paraplegic Marine is sent to the moon Pandora on a unique mission.",
        "detailed_summary": "On Pandora, a lush alien world filled with unique life forms, Jake Sully, a former Marine, finds himself torn between following orders and protecting the world he feels is his new home.",
        "director": "James Cameron",
        "cast": ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver"],
        "box_office": "$2.92 billion",
        "awards": ["Academy Awards for Best Art Direction, Best Cinematography, and Best Visual Effects"],
        "image": "images/avatar.jpeg"
    },
    {
        "title": "Her",
        "year": 2013,
        "genre": "Drama, Romance, Sci-Fi",
        "rating": 8.0,
        "description": "A lonely writer develops an unlikely relationship with an operating system.",
        "detailed_summary": "In a not-so-distant future, Theodore, a writer dealing with a recent breakup, purchases an AI assistant that grows to become a companion. Their relationship explores the complexities of love and technology.",
        "director": "Spike Jonze",
        "cast": ["Joaquin Phoenix", "Scarlett Johansson"],
        "box_office": "$48.3 million",
        "awards": ["Academy Award for Best Original Screenplay"],
        "image": "images/her.jpeg"
    },
    {
        "title": "Jaws",
        "year": 1975,
        "genre": "Adventure, Thriller",
        "rating": 8.1,
        "description": "A giant great white shark terrorizes a small resort town.",
        "detailed_summary": "When a killer shark unleashes chaos on a beach community, it's up to a local sheriff, a marine biologist, and an old seafarer to hunt the beast down before it kills again.",
        "director": "Steven Spielberg",
        "cast": ["Roy Scheider", "Robert Shaw", "Richard Dreyfuss"],
        "box_office": "$470 million",
        "awards": ["Academy Award for Best Film Editing"],
        "image": "images/jaws.jpeg"
    },
    {
        "title": "Suicide Squad",
        "year": 2016,
        "genre": "Action, Adventure, Fantasy",
        "rating": 6.0,
        "description": "A group of dangerous criminals are recruited by the government to carry out black ops missions.",
        "detailed_summary": "A group of dangerous criminals are recruited by the government to carry out black ops missions in exchange for reduced sentences. Together, they form an unlikely and volatile team in an attempt to save the world.",
        "director": "David Ayer",
        "cast": ["Will Smith", "Margot Robbie", "Jared Leto"],
        "box_office": "$746 million",
        "awards": ["Academy Award for Best Makeup"],
        "image": "images/suicidesquad.jpeg"
    }
]

# Database Setup Functions
def create_tables():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Create users table (without admin flag initially to ensure compatibility)
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    email TEXT
                )""")
    
    # Create reviews table
    c.execute("""CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    movie_title TEXT,
                    rating INTEGER,
                    review_text TEXT,
                    timestamp DATETIME,
                    FOREIGN KEY (username) REFERENCES users(username),
                    UNIQUE(username, movie_title)
                )""")
    
    conn.commit()
    conn.close()
    
    # Now migrate the schema if needed
    migrate_schema()
    
    # Then create admin user if needed
    create_admin_user()

def migrate_schema():
    """Add any missing columns to the database tables"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if is_admin column exists in users table
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    
    if "is_admin" not in columns:
        try:
            # Add is_admin column to users table
            c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            conn.commit()
            st.success("Database schema updated successfully")
        except Exception as e:
            st.error(f"Error updating database schema: {e}")
    
    conn.close()

def create_admin_user():
    """Create admin user if it doesn't exist"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if admin user exists
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        hashed_password = bcrypt.hashpw("admin".encode(), bcrypt.gensalt())
        try:
            c.execute("INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                     ("admin", hashed_password, "admin@example.com", 1))
            conn.commit()
        except Exception as e:
            st.error(f"Error creating admin user: {e}")
    else:
        # Make sure the admin user has admin privileges
        c.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
        conn.commit()
    
    conn.close()

def initialize_database():
    try:
        # Only create tables if they don't exist
        create_tables()
        return True
    except Exception as e:
        st.error(f"Error initializing database: {e}")
        return False

# User Management Functions
def add_user(username, password, email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                 (username, hashed_password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists!")
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # First check if the is_admin column exists
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    
    if "is_admin" in columns:
        c.execute("SELECT password, is_admin FROM users WHERE username = ?", (username,))
    else:
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        
    result = c.fetchone()
    conn.close()
    
    if result and bcrypt.checkpw(password.encode(), result[0]):
        # If is_admin column exists, use its value, otherwise default to 0
        is_admin = result[1] if "is_admin" in columns and len(result) > 1 else 0
        return True, is_admin
    return False, 0

# Review Management Functions
def get_user_review(username, movie_title):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT rating, review_text, timestamp FROM reviews WHERE username = ? AND movie_title = ?", 
              (username, movie_title))
    result = c.fetchone()
    conn.close()
    return result

def save_review(username, movie_title, rating, review_text):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO reviews (username, movie_title, rating, review_text, timestamp)
                     VALUES (?, ?, ?, ?, ?)""", 
                     (username, movie_title, rating, review_text, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        c.execute("""UPDATE reviews SET rating = ?, review_text = ?, timestamp = ? 
                     WHERE username = ? AND movie_title = ?""", 
                     (rating, review_text, datetime.now(), username, movie_title))
        conn.commit()
        return True
    finally:
        conn.close()

# Movie Management Functions
def save_movie_to_database(movie_data):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Create movies table if it doesn't exist
    c.execute("""CREATE TABLE IF NOT EXISTS movies (
                    title TEXT PRIMARY KEY,
                    year INTEGER,
                    genre TEXT,
                    rating REAL,
                    description TEXT,
                    detailed_summary TEXT,
                    director TEXT,
                    cast TEXT,
                    box_office TEXT,
                    awards TEXT,
                    image_path TEXT
                )""")
    
    try:
        c.execute("""INSERT INTO movies 
                    (title, year, genre, rating, description, detailed_summary, 
                    director, cast, box_office, awards, image_path) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (movie_data["title"], movie_data["year"], movie_data["genre"],
                    movie_data["rating"], movie_data["description"], movie_data["detailed_summary"],
                    movie_data["director"], str(movie_data["cast"]), movie_data["box_office"],
                    str(movie_data["awards"]), movie_data["image"]))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Movie with this title already exists!")
        return False
    finally:
        conn.close()

def delete_movie_from_database(title):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    try:
        # Delete movie
        c.execute("DELETE FROM movies WHERE title = ?", (title,))
        # Delete associated reviews
        c.execute("DELETE FROM reviews WHERE movie_title = ?", (title,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error deleting movie: {e}")
        return False
    finally:
        conn.close()

def get_all_movies():
    # First get the hardcoded movies
    all_movies = movies.copy()
    
    # Then get movies from database
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        
        # Check if the movies table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
        if c.fetchone():
            c.execute("SELECT * FROM movies")
            db_movies = c.fetchall()
            
            for movie in db_movies:
                movie_dict = {
                    "title": movie[0],
                    "year": movie[1],
                    "genre": movie[2],
                    "rating": movie[3],
                    "description": movie[4],
                    "detailed_summary": movie[5],
                    "director": movie[6],
                    "cast": eval(movie[7]),
                    "box_office": movie[8],
                    "awards": eval(movie[9]),
                    "image": movie[10]
                }
                all_movies.append(movie_dict)
        
        conn.close()
    except Exception as e:
        st.error(f"Error loading movies from database: {e}")
    
    return all_movies

def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        # Create images directory if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")
        
        # Save the uploaded file
        file_path = os.path.join("images", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

# UI Components
def show_movie_dialog(movie, username):
    with st.expander(f"Movie Details: {movie['title']}", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(movie["image"], use_column_width=True)
        
        with col2:
            st.markdown(f"### {movie['title']} ({movie['year']})")
            st.markdown(f"**Genre:** {movie['genre']}")
            st.markdown(f"**IMDb Rating:** {movie['rating']}")
            st.markdown(f"**Description:** {movie['description']}")
            st.markdown("---")
            st.markdown(f"**Detailed Summary:** {movie['detailed_summary']}")
        
        st.markdown("---")
        st.subheader("Your Review")
        
        existing_review = get_user_review(username, movie['title'])
        
        if existing_review:
            rating, review_text, timestamp = existing_review
            st.markdown(f"**Your Rating:** {'⭐' * rating}")
            st.markdown(f"**Your Review:** {review_text}")
            st.markdown(f"*Reviewed on: {timestamp}*")
            
            if st.button("Update Review"):
                st.session_state.updating_review = True
        
        if not existing_review or 'updating_review' in st.session_state:
            rating = st.slider("Rate this movie", 1, 5, 
                             value=rating if existing_review else 3)
            review_text = st.text_area("Write your review", 
                                     value=review_text if existing_review else "")
            
            if st.button("Submit Review"):
                if save_review(username, movie['title'], rating, review_text):
                    st.success("Review saved successfully!")
                    if 'updating_review' in st.session_state:
                        del st.session_state.updating_review
                    st.session_state["needs_rerun"] = True

def admin_panel():
    st.title("Admin Panel")
    
    tab1, tab2 = st.tabs(["Add Movie", "Delete Movie"])
    
    with tab1:
        st.header("Add New Movie")
        
        title = st.text_input("Movie Title")
        year = st.number_input("Release Year", min_value=1900, max_value=2100, value=2023)
        genre = st.text_input("Genre (comma-separated)", "Action, Drama")
        rating = st.slider("IMDb Rating", 0.0, 10.0, 7.0, 0.1)
        description = st.text_area("Short Description", "A brief summary of the movie.")
        detailed_summary = st.text_area("Detailed Summary", "A more detailed plot summary.")
        director = st.text_input("Director")
        cast = st.text_input("Cast (comma-separated)")
        box_office = st.text_input("Box Office", "$0 million")
        awards = st.text_input("Awards (comma-separated)")
        
        uploaded_file = st.file_uploader("Upload Movie Poster", type=["jpg", "jpeg", "png"])
        image_path = None
        
        if uploaded_file:
            st.image(uploaded_file, width=200)
            image_path = save_uploaded_image(uploaded_file)
        
        if st.button("Add Movie"):
            if title and description and image_path:
                movie_data = {
                    "title": title,
                    "year": year,
                    "genre": genre,
                    "rating": rating,
                    "description": description,
                    "detailed_summary": detailed_summary,
                    "director": director,
                    "cast": [x.strip() for x in cast.split(",") if x.strip()],
                    "box_office": box_office,
                    "awards": [x.strip() for x in awards.split(",") if x.strip()],
                    "image": image_path
                }
                
                if save_movie_to_database(movie_data):
                    st.success("Movie added successfully!")
                    st.session_state["needs_rerun"] = True
            else:
                st.warning("Title, description, and image are required.")
    
    with tab2:
        st.header("Delete Movie")
        
        all_movies = get_all_movies()
        movie_titles = [movie["title"] for movie in all_movies]
        
        selected_movie = st.selectbox("Select Movie to Delete", movie_titles)
        
        if selected_movie:
            # Find the movie to display its info
            movie_to_display = next((movie for movie in all_movies if movie["title"] == selected_movie), None)
            
            if movie_to_display:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(movie_to_display["image"], width=200)
                
                with col2:
                    st.markdown(f"### {movie_to_display['title']} ({movie_to_display['year']})")
                    st.markdown(f"**Genre:** {movie_to_display['genre']}")
                    st.markdown(f"**IMDb Rating:** {movie_to_display['rating']}")
                    st.markdown(f"**Description:** {movie_to_display['description']}")
        
        if st.button("Delete Movie", type="primary", help="This action cannot be undone!"):
            if delete_movie_from_database(selected_movie):
                st.success(f"Movie '{selected_movie}' deleted successfully!")
                st.session_state["needs_rerun"] = True
            else:
                st.error("Failed to delete movie.")

def render_movie_page(username, is_admin=False):
    st.title("IMDb Clone - Movie Dashboard")
    
    if is_admin:
        st.success(f"Hello admin! You have special privileges.")
        if st.button("Go to Admin Panel"):
            st.session_state.show_admin_panel = True
            return
    
    st.subheader("Explore Popular Movies")

    # Get all movies (hardcoded + from database)
    all_movies = get_all_movies()

    # Create three columns
    cols = st.columns(3)
    for idx, movie in enumerate(all_movies):
        with cols[idx % 3]:
            card = st.container()
            with card:
                st.image(movie["image"], use_column_width=True)
                st.markdown(f"**{movie['title']} ({movie['year']})**")
                st.write(f"Genre: {movie['genre']}")
                st.write(f"IMDb Rating: {movie['rating']}")
                
                user_review = get_user_review(username, movie['title'])
                if user_review:
                    st.markdown(f"Your Rating: {'⭐' * user_review[0]}")
                
                if st.button("View Details", key=movie["title"]):
                    st.session_state.selected_movie = movie

    if "selected_movie" in st.session_state:
        show_movie_dialog(st.session_state.selected_movie, username)

def main():
    st.set_page_config(layout="wide")
    
    # Initialize database only if it doesn't exist
    if not os.path.exists("users.db"):
        if initialize_database():
            st.session_state.db_initialized = True
    else:
        # Make sure tables exist and admin user exists
        create_tables()

    if st.session_state.get("needs_rerun"):
        st.session_state["needs_rerun"] = False
        st.experimental_set_query_params()

    with st.sidebar:
        st.title("Login/Registration")

        if "logged_in" not in st.session_state:
            if st.checkbox("New User? Register Here"):
                new_username = st.text_input("Username", key="new_username")
                new_password = st.text_input("Password", type="password", key="new_password")
                new_email = st.text_input("Email", key="new_email")
                if st.button("Register"):
                    if new_username and new_password and new_email:
                        if add_user(new_username, new_password, new_email):
                            st.success("User registered successfully!")
                    else:
                        st.warning("Please fill all fields.")
        
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            login_success, is_admin = login_user(username, password)
            if login_success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = is_admin
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")

        if "logged_in" in st.session_state and st.session_state.logged_in:
            if st.button("Logout"):
                # Only clear login-related session state
                for key in ['logged_in', 'username', 'selected_movie', 'is_admin', 'show_admin_panel']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()  # Changed from st.experimental_rerun()

    if "logged_in" in st.session_state and st.session_state.logged_in:
        if st.session_state.get("show_admin_panel") and st.session_state.is_admin:
            admin_panel()
        else:
            render_movie_page(st.session_state.username, st.session_state.is_admin)
    else:
        st.warning("Please log in to access the movie dashboard.")

if __name__ == "__main__":
    main()