# import spacy
# from fpdf import FPDF

# import requests
# from bs4 import BeautifulSoup
# from fpdf import FPDF
# from gtts import gTTS
# from pydub import AudioSegment
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import openai
# import os
# from urllib.parse import urlparse


# # Step 1: Fetch Latest News
# def fetch_latest_news(query, num_results=10):
#     search_url = f"https://www.google.com/search?q={query}&tbm=nws"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(search_url, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     articles = []
#     for result in soup.find_all("div", class_="BVG0Nb")[:num_results]:
#         title = result.find("div", class_="BNeawe vvjwJb AP7Wnd").text
#         link = result.find("a")["href"]
#         snippet = result.find("div", class_="BNeawe s3v9rd AP7Wnd").text
#         articles.append({"title": title, "link": link, "snippet": snippet})
#     return articles

# # Step 2: Create PDF from News
# def create_pdf(articles, query):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Latest News on {query}", ln=True, align='C')
    
#     for article in articles:
#         pdf.set_font("Arial", style="B", size=12)
#         pdf.multi_cell(0, 10, article["title"])
#         pdf.set_font("Arial", size=12)
#         pdf.multi_cell(0, 10, article["snippet"])
#         pdf.multi_cell(0, 10, article["link"])
#         pdf.ln()
    
#     pdf_filename = f"{query.replace(' ', '_')}_news.pdf"
#     pdf.output(pdf_filename)
#     return pdf_filename

# # Step 3: Summarize News Using GPT
# # def summarize_news(articles):
# #     openai.api_key = "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"
# #     news_text = "\n\n".join([f"{a['title']}: {a['snippet']}" for a in articles])
# #     # Use the latest GPT-4 model for better summarization
# #     prompt = f"Summarize the following news articles into a short podcast script:\n{news_text}"
# #     response = openai.ChatCompletion.create(
# #         model="gpt-4",
# #         messages=[
# #             {"role": "system", "content": "You are an expert news summarizer."},
# #             {"role": "user", "content": prompt}
# #         ],
# #         max_tokens=500
# #     )
# #     return response['choices'][0]['message']['content'].strip()

# # Step 4: Convert Summary to Audio
# def create_audio(summary, filename="podcast.mp3"):
#     tts = gTTS(summary, lang="en")
#     tts.save(filename)
#     return filename

# # Step 5: Upload to Spotify
# def upload_to_spotify(audio_file, podcast_title, podcast_description):
#     # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     #     client_id="your_spotify_client_id",
#     #     client_secret="your_spotify_client_secret",
#     #     redirect_uri="your_redirect_uri",
#     #     scope="ugc-image-upload,user-library-modify,user-library-read"
#     # ))
    
#     # # Create a new playlist (to mimic podcast functionality)
#     # user_id = sp.current_user()["id"]
#     # playlist = sp.user_playlist_create(user_id, podcast_title, description=podcast_description)
    
#     # # Convert audio to required format (if needed)
#     # audio = AudioSegment.from_mp3(audio_file)
#     # audio.export("output.wav", format="wav")
    
#     # Upload to Spotify (via workaround like playlist description or third-party hosting)
#     # You may need to explore third-party hosting to fully automate podcast uploads.
#     # print(f"Podcast uploaded to Spotify playlist: {playlist['external_urls']['spotify']}")
#     print(f"Podcast uploaded to Spotify playlist")

# def notebook_lm_step(pdf_file):
#     print(f"Upload the PDF '{pdf_file}' to Google Notebook LM.")
#     print("After getting the summary, copy and paste it here.")
#     summary = input("Paste the summary from Notebook LM: ")
#     return summary

# # Step 1: Define a ranking function
# def rank_results(articles, query):
#     """
#     Rank articles based on relevance, authority, and snippet length.
#     Assign higher scores to more relevant and authoritative pages.
#     """
#     rankings = []
#     trusted_domains = ["bbc.com", "reuters.com", "nytimes.com", "cnn.com", "forbes.com"]
    
#     for article in articles:
#         score = 0
        
#         # Relevance: Check if query terms appear in the title/snippet
#         if query.lower() in article["title"].lower():
#             score += 3
#         if query.lower() in article["snippet"].lower():
#             score += 2
        
#         # Authority: Check if the link belongs to a trusted domain
#         domain = urlparse(article["link"]).netloc
#         if any(trusted_domain in domain for trusted_domain in trusted_domains):
#             score += 5
        
#         # Depth: Longer snippets may indicate richer content
#         if len(article["snippet"]) > 100:
#             score += 1
        
#         # Add final score to the article
#         article["score"] = score
#         rankings.append(article)
    
#     # Sort articles by score in descending order
#     ranked_articles = sorted(rankings, key=lambda x: x["score"], reverse=True)
#     return ranked_articles


# # Step 1: Add a function to extract key points using NLP
# def extract_key_points(snippet):
#     """
#     Use NLP to extract key points from a snippet.
#     Alternatively, use OpenAI GPT or any summarization model.
#     """
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(snippet)
#     sentences = [sent.text for sent in doc.sents]
#     # Return the top 2 sentences as key points (you can adjust this)
#     return sentences[:2]

# # Step 2: Create a PDF with Key Points and Hyperlinks
# def create_pdf_with_links_and_keypoints(articles, query):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Latest News on {query}", ln=True, align='C')

#     for article in articles:
#         pdf.set_font("Arial", style="B", size=12)
#         pdf.multi_cell(0, 10, article["title"])
        
#         # Add the hyperlink
#         pdf.set_text_color(0, 0, 255)
#         pdf.set_font("Arial", size=12)
#         pdf.cell(0, 10, article["link"], ln=True, link=article["link"])
        
#         # Add the snippet and key points
#         pdf.set_text_color(0, 0, 0)  # Reset text color to black
#         pdf.set_font("Arial", size=12)
#         pdf.multi_cell(0, 10, f"Snippet: {article['snippet']}")
        
#         # Extract and add key points
#         key_points = extract_key_points(article["snippet"])
#         pdf.set_font("Arial", style="I", size=11)
#         pdf.multi_cell(0, 10, "Key Points:")
#         for i, point in enumerate(key_points, start=1):
#             pdf.multi_cell(0, 10, f"  {i}. {point}")
        
#         pdf.ln()

#     pdf_filename = f"{query.replace(' ', '_')}_news_with_keypoints.pdf"
#     pdf.output(pdf_filename)
#     return pdf_filename

# # Step 3: Use the updated PDF function in the main script
# # def main():
# #     query = input("Enter a topic (e.g., Indian news or stock market trends of TSMC): ")
# #     print("Fetching latest news...")
# #     articles = fetch_latest_news(query)
    
# #     print("Ranking articles...")
# #     ranked_articles = rank_results(articles, query)
# #     print("Top-ranked articles:")
# #     for i, article in enumerate(ranked_articles[:5], start=1):
# #         print(f"{i}. {article['title']} (Score: {article['score']})")
    
# #     print("Creating PDF with links and key points...")
# #     pdf_file = create_pdf_with_links_and_keypoints(ranked_articles[:10], query)
# #     print(f"PDF created: {pdf_file}")
    
# #     print("Summarizing with Notebook LM...")
# #     summary = notebook_lm_step(pdf_file)
# #     print("Summary:\n", summary)
    
# #     print("Creating audio...")
# #     audio_file = create_audio(summary)
# #     print(f"Audio created: {audio_file}")
    
# #     print("Uploading to Spotify...")
# #     upload_to_spotify(audio_file, f"Podcast on {query}", summary)


# # def main():
# #     query = input("Enter a topic (e.g., Indian news or stock market trends of TSMC): ")
# #     print("Fetching latest news...")
# #     articles = fetch_latest_news(query)
    
# #     print("Ranking articles...")
# #     ranked_articles = rank_results(articles, query)
# #     print("Top-ranked articles:")
# #     for i, article in enumerate(ranked_articles[:5], start=1):
# #         print(f"{i}. {article['title']} (Score: {article['score']})")
    
# #     print("Creating PDF with links and key points...")
# #     pdf_file = create_pdf_with_links_and_keypoints(ranked_articles[:10], query)
# #     print(f"PDF created: {pdf_file}")
    
# #     print("Summarizing news articles...")
# #     summary = summarize_news(ranked_articles[:10])
# #     print("Summary:\n", summary)
    
# #     print("Creating audio...")
# #     audio_file = create_audio(summary)
# #     print(f"Audio created: {audio_file}")
    
# #     print("Uploading to Spotify...")
# #     upload_to_spotify(audio_file, f"Podcast on {query}", summary)


# # if __name__ == "__main__":
#     # main()