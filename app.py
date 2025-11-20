from flask import Flask, render_template, request, redirect, url_for, session, flash
from textblob import TextBlob
import requests, sqlite3, os

app = Flask(__name__)
app.secret_key = "learnify_secret_key"

DB_PATH = "learnify.db"
YOUTUBE_API_KEY = "AIzaSyC-G8AaOVXnPKtrT4mM4ND1CMA4whCLELo"

# -------------------- INITIALIZE DATABASE --------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')

        # Feedback table
        c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_query TEXT,
                        topic TEXT,
                        mood TEXT,
                        sentiment REAL,
                        feedback TEXT
                    )''')

        conn.commit()

init_db()

# -------------------- FETCH YOUTUBE VIDEOS --------------------
def fetch_youtube_videos(query):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&maxResults=3&q={query}&type=video&key={YOUTUBE_API_KEY}"
    )
    try:
        data = requests.get(url).json()
        videos = [
            {
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            for item in data.get("items", [])
        ]
        return videos
    except Exception as e:
        print("YouTube error:", e)
        return []

# -------------------- AUTH ROUTES --------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                          (username, email, password))
                conn.commit()
                flash("✅ Account created successfully! Please login.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("⚠️ Username or Email already exists!", "error")
                return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()

        if user:
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid username or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first!", "info")
        return redirect(url_for("login"))

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_query, topic, mood, feedback FROM feedback")
        history = c.fetchall()

        # Analytics
        c.execute("SELECT topic, COUNT(*) FROM feedback GROUP BY topic")
        topic_counts = dict(c.fetchall())

        c.execute("SELECT mood, COUNT(*) FROM feedback GROUP BY mood")
        mood_counts = dict(c.fetchall())

    return render_template(
        "dashboard.html",
        user=session["user"],
        history=history,
        topic_data=topic_counts,
        mood_data=mood_counts,
    )

# -------------------- MAIN PAGES --------------------
@app.route("/")
def home():
    print("✅ Rendering index.html ...")
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.form.get("user_input", "")
    sentiment = TextBlob(user_input).sentiment.polarity

    if sentiment < -0.1:
        mood = "confused"
    elif sentiment < 0.3:
        mood = "neutral"
    else:
        mood = "excited"

    topic = "general"
    for key in ["ai", "ml", "python", "cloud", "programming"]:
        if key in user_input.lower():
            topic = key
            break

    videos = fetch_youtube_videos(user_input + " tutorial")

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO feedback (user_query, topic, mood, sentiment) VALUES (?, ?, ?, ?)",
                  (user_input, topic, mood, sentiment))
        conn.commit()

    return render_template(
        "recommend.html",
        query=user_input,
        mood=mood,
        sentiment=round(sentiment, 2),
        topic=topic.title(),
        videos=videos
    )

# -------------------- FEEDBACK ROUTE --------------------
@app.route("/feedback", methods=["POST"])
def save_feedback():
    feedback_value = request.form.get("feedback")
    user_query = request.form.get("query")
    feedback_text = request.form.get("feedback_text", "")

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM feedback WHERE user_query = ? ORDER BY id DESC LIMIT 1", (user_query,))
        last = c.fetchone()
        if last:
            c.execute("UPDATE feedback SET feedback = ? WHERE id = ?", (f"{feedback_value}: {feedback_text}", last[0]))
            conn.commit()

    flash("✅ Thank you for your feedback!", "success")
    return redirect(url_for("dashboard"))

# -------------------- TEST ROUTE --------------------
@app.route("/test")
def test():
    return "<h3>✅ Flask route working!</h3>"

# -------------------- MAIN APP --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5050)
