import streamlit as st
from PIL import Image
import sqlite3
import bcrypt
from datetime import datetime
import os

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
        "detailed_summary": "Belle, a bright, beautiful, and independent young woman, is taken prisoner by a beast in his castle. Despite her fears, she befriends the castle’s enchanted staff and learns to look beyond the Beast’s hideous exterior to recognize the true heart and soul of the Prince within.",
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
        "detailed_summary": "When a killer shark unleashes chaos on a beach community, it’s up to a local sheriff, a marine biologist, and an old seafarer to hunt the beast down before it kills again.",
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
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    
    # Drop existing tables to ensure clean setup
    c.execute("DROP TABLE IF EXISTS reviews")
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS movies")
    
    # Create users table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    email TEXT,
                    is_admin BOOLEAN
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
    
    # Create movies table
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
    
    conn.commit()
    conn.close()

def initialize_database():
    try:
        if os.path.exists("movies.db"):
            os.remove("movies.db")
        
        create_tables()
        return True
    except Exception as e:
        st.error(f"Error initializing database: {e}")
        return False

# User Management Functions
def add_user(username, password, email, is_admin=False):
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)", 
                 (username, hashed_password, email, is_admin))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists!")
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    c.execute("SELECT password, is_admin FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True, result[1]  # Return if user is admin
    return False, False
    

# Movie Management Functions
def add_movie(movie_data, image_file=None):
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    try:
        # Save image if uploaded
        if image_file:
            image_path = f"images/{movie_data['title'].replace(' ', '_').lower()}.jpeg"
            image = Image.open(image_file)
            image.save(image_path)
            movie_data["image_path"] = image_path

        # Insert movie data
        c.execute("""INSERT INTO movies (title, year, genre, rating, description, detailed_summary,
                                          director, cast, box_office, awards, image_path)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                  (movie_data["title"], movie_data["year"], movie_data["genre"], movie_data["rating"], 
                   movie_data["description"], movie_data["detailed_summary"], movie_data["director"], 
                   ', '.join(movie_data["cast"]), movie_data["box_office"], ', '.join(movie_data["awards"]), 
                   movie_data["image_path"]))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Movie already exists!")
        return False
    finally:
        conn.close()

# UI Components for Admin to Add Movie
def admin_add_movie():
    st.subheader("Add New Movie")
    movie_data = {
        "title": st.text_input("Title"),
        "year": st.number_input("Year", min_value=1800, max_value=2100, step=1),
        "genre": st.text_input("Genre (comma-separated)"),
        "rating": st.slider("Rating", 0.0, 10.0, step=0.1),
        "description": st.text_area("Short Description"),
        "detailed_summary": st.text_area("Detailed Summary"),
        "director": st.text_input("Director"),
        "cast": st.text_input("Cast (comma-separated)").split(","),
        "box_office": st.text_input("Box Office"),
        "awards": st.text_input("Awards (comma-separated)").split(",")
    }
    image_file = st.file_uploader("Upload Movie Poster (JPEG format)", type=["jpeg", "jpg"])

    if st.button("Add Movie"):
        if add_movie(movie_data, image_file):
            st.success(f"{movie_data['title']} has been added successfully!")

# Main Page Rendering
def render_movie_page(username, is_admin):
    st.title("IMDb Clone - Movie Dashboard")
    st.subheader("Explore Popular Movies")

    # Load movies from DB
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    conn.close()

    # Show movies
    cols = st.columns(3)
    for idx, movie in enumerate(movies):
        with cols[idx % 3]:
            card = st.container()
            with card:
                st.image(movie[10], use_column_width=True)  # Image path from DB
                st.markdown(f"**{movie[0]} ({movie[1]})**")  # Title and Year
                st.write(f"Genre: {movie[2]}")
                st.write(f"IMDb Rating: {movie[3]}")
                
                if st.button("View Details", key=movie[0]):
                    st.session_state.selected_movie = movie

    # Admin Panel
    if is_admin:
        with st.sidebar:
            st.subheader("Admin Panel")
            if st.button("Add New Movie"):
                admin_add_movie()

# Main Function
def main():
    st.set_page_config(layout="wide")

    if 'db_initialized' not in st.session_state:
        if initialize_database():
            st.session_state.db_initialized = True

    with st.sidebar:
        st.title("Login/Registration")

        if "logged_in" not in st.session_state:
            if st.checkbox("New User? Register Here"):
                new_username = st.text_input("Username", key="new_username")
                new_password = st.text_input("Password", type="password", key="new_password")
                new_email = st.text_input("Email", key="new_email")
                is_admin = st.checkbox("Register as Admin", key="is_admin")

                if st.button("Register"):
                    if new_username and new_password and new_email:
                        if add_user(new_username, new_password, new_email, is_admin):
                            st.success("User registered successfully!")
                    else:
                        st.warning("Please fill all fields.")
        
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            is_valid, is_admin = login_user(username, password)
            if is_valid:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = is_admin
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")

        if "logged_in" in st.session_state and st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.clear()

    if "logged_in" in st.session_state and st.session_state.logged_in:
        render_movie_page(st.session_state.username, st.session_state.is_admin)
    else:
        st.warning("Please log in to access the movie dashboard.")

if __name__ == "__main__":
    main()
