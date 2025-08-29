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
    
    # Create users table
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
    
    # Create trigger to update timestamp when review is inserted or updated
    c.execute("""
    CREATE TRIGGER IF NOT EXISTS update_timestamp
    AFTER INSERT ON reviews
    BEGIN
        UPDATE reviews SET timestamp = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """)
    
    # Create trigger to delete reviews when user is deleted
    c.execute("""
    CREATE TRIGGER IF NOT EXISTS delete_reviews_on_user_delete
    AFTER DELETE ON users
    BEGIN
        DELETE FROM reviews WHERE username = OLD.username;
    END;
    """)
    
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
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True
    return False

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

def render_movie_page(username):
    st.title("IMDb Clone - Movie Dashboard")
    st.subheader("Explore Popular Movies")

    # Create three columns
    cols = st.columns(3)
    for idx, movie in enumerate(movies):
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
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")

        if "logged_in" in st.session_state and st.session_state.logged_in:
            if st.button("Logout"):
                # Only clear login-related session state
                for key in ['logged_in', 'username', 'selected_movie']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
    
    if "logged_in" in st.session_state and st.session_state.logged_in:
        render_movie_page(st.session_state.username)

if __name__ == "__main__":
    main()
