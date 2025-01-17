import requests
from flask import Flask, request
import spacy
from fpdf import FPDF

from bs4 import BeautifulSoup
from fpdf import FPDF
from gtts import gTTS
from pydub import AudioSegment
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import feedparser

def fetch_latest_news(query, num_results=10):
    """
    Fetch the latest news using Google News RSS.
    """
    query = query.replace(" ", "+")  # Format query for the URL
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:num_results]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "snippet": entry.summary
        })
    return articles

# Step 2: Create PDF from News
def create_pdf(articles, query):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Latest News on {query}", ln=True, align='C')
    
    for article in articles:
        pdf.set_font("Arial", style="B", size=12)
        pdf.multi_cell(200, 10, article["title"])
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, article["snippet"])
        pdf.multi_cell(200, 10, article["link"])
        pdf.ln()
    
    pdf_filename = f"{query.replace(' ', '_')}_news.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

# Step 4: Convert Summary to Audio
def create_audio(summary, filename="podcast.mp3"):
    tts = gTTS(summary, lang="en")
    tts.save(filename)
    return filename

# Step 5: Upload to Spotify
def upload_to_spotify(audio_file, podcast_title, podcast_description):
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret="your_spotify_client_secret",
        redirect_uri="your_redirect_uri",
        scope="ugc-image-upload,user-library-modify,user-library-read"
    ))
    
    # Create a new playlist
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, podcast_title, description=podcast_description)
    
    # Convert audio to required format (if needed)
    audio = AudioSegment.from_mp3(audio_file)
    audio.export("output.wav", format="wav")
    print(f"Podcast uploaded to Spotify playlist: {playlist['external_urls']['spotify']}")

def notebook_lm_step(pdf_file):
    print(f"Upload the PDF '{pdf_file}' to Google Notebook LM.")
    print("After getting the summary, copy and paste it here.")
    print("Paste the summary from Notebook LM: ")
    return "this step is manual currently"

# Step 1: Define a ranking function
def rank_results(articles, query):
    """
    Rank articles based on relevance, authority, and snippet length.
    Assign higher scores to more relevant and authoritative pages.
    """
    rankings = []
    trusted_domains = ["bbc.com", "reuters.com", "nytimes.com", "cnn.com", "forbes.com"]
    
    for article in articles:
        score = 0
        
        # Relevance: Check if query terms appear in the title/snippet
        if query.lower() in article["title"].lower():
            score += 3
        if query.lower() in article["snippet"].lower():
            score += 2
        
        # Authority: Check if the link belongs to a trusted domain
        domain = urlparse(article["link"]).netloc
        if any(trusted_domain in domain for trusted_domain in trusted_domains):
            score += 5
        
        # Depth: Longer snippets may indicate richer content
        if len(article["snippet"]) > 100:
            score += 1
        
        # Add final score to the article
        article["score"] = score
        rankings.append(article)
    
    # Sort articles by score in descending order
    ranked_articles = sorted(rankings, key=lambda x: x["score"], reverse=True)
    return ranked_articles


# Step 1: Add a function to extract key points using NLP
def extract_key_points(snippet):
    """
    Use NLP to extract key points from a snippet.
    Alternatively, use OpenAI GPT or any summarization model.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(snippet)
    sentences = [sent.text for sent in doc.sents]
    # Return the top 2 sentences as key points (you can adjust this)
    return sentences[:2]

# Step 2: Create a PDF with Key Points and Hyperlinks
def create_pdf_with_links_and_keypoints(articles, query):
    """
    Create a PDF with article titles, links, snippets, and key points.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Latest News on {query}", ln=True, align='C')
    pdf.ln(10)  # Add a little space after the header

    for article in articles:
        # Title
        pdf.set_text_color(0, 0, 0)  # Reset text color to black
        pdf.set_font("Arial", style="B", size=12)
        pdf.multi_cell(200, 10, article["title"])
        pdf.ln(2)  # Add a little spacing after the title

        # Hyperlink
        pdf.set_text_color(0, 0, 255)  # Set text color to blue for hyperlinks
        pdf.set_font("Arial", size=12)
        link = article["link"]
        if len(link) > 0:  # Check if link is not empty
            pdf.cell(0, 10, link, ln=True, link=link)
        else:
            pdf.cell(0, 10, "No link available", ln=True)

        pdf.ln(2)  # Add spacing after the link

        # Snippet
        pdf.set_text_color(0, 0, 0)  # Reset text color to black
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, f"Snippet: {article['snippet']}")
        pdf.ln(2)

        # Key Points
        key_points = extract_key_points(article["snippet"])
        pdf.set_font("Arial", style="I", size=11)
        pdf.multi_cell(200, 10, "Key Points:")
        for i, point in enumerate(key_points, start=1):
            pdf.multi_cell(200, 10, f"  {i}. {point}")
        pdf.ln(5)  # Add extra space between articles

    # Save the PDF in the 'static' folder
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    pdf_filename = f"{query.replace(' ', '_')}_news_with_keypoints.pdf"
    pdf_path = os.path.join(static_dir, pdf_filename)
    pdf.output(pdf_path)
    return pdf_filename


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        query = request.form.get("topic")
        if not query:
            return "Please enter a topic."

        response_html = ""
        response_html += f"<h2>Topic: {query}</h2>"

        # Fetch latest news
        response_html += "<h3>Fetching latest news...</h3>"
        articles = fetch_latest_news(query)
        response_html += f"<p>Found {len(articles)} articles.</p>"

        # Rank articles
        response_html += "<h3>Ranking articles...</h3>"
        ranked_articles = rank_results(articles, query)
        response_html += "<h4>Top-ranked articles:</h4><ul>"
        for i, article in enumerate(ranked_articles[:5], start=1):
            response_html += f"<li>{article['title']} (Score: {article['score']})</li>"
        response_html += "</ul>"

        # Create PDF with links and key points
        response_html += "<h3>Creating PDF with links and key points...</h3>"
        pdf_file = create_pdf_with_links_and_keypoints(ranked_articles[:10], query)
         # Serve the PDF link for user to download and process
        pdf_url = f"/static/{pdf_file}"
        response_html += f"<p>PDF created: <a href='{pdf_url}' target='_blank'>{pdf_file}</a></p>"
        # Summarize with Notebook LM or AI
        response_html += "<h3>Summarizing news...</h3>"
        summary = notebook_lm_step(pdf_file)  # Replace with summarize_news if fully automated
        response_html += f"<h4>Summary:</h4><p>{summary}</p>"

        # Create audio
        response_html += "<h3>Creating audio...</h3>"
        audio_file = create_audio(pdf_file)
        response_html += f"<p>Audio created: {audio_file}</p>"

        # Upload to Spotify
        response_html += "<h3>Uploading to Spotify...</h3>"
        upload_to_spotify(audio_file, f"Podcast on {query}", summary)
        response_html += "<p>Podcast uploaded to Spotify.</p>"

        return response_html

    # Render the HTML form for input
    return '''
    <h1>PodifyNews: Automated News to Podcast</h1>
    <form method="POST">
        <label for="topic">Enter a topic of interest:</label>
        <input type="text" id="topic" name="topic" required>
        <button type="submit">Submit</button>
    </form>
    '''


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    nlp = spacy.load("en_core_web_sm")
    print("Model loaded successfully!")
    app.run(host='0.0.0.0', port=8000)