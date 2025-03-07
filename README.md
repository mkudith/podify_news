# 🎙️ PodifyNews: Automated News to Podcast Pipeline

**PodifyNews** transforms the latest news into concise podcasts! Fetch, rank, summarize, generate PDFs, and upload as podcasts to Spotify—all in one seamless pipeline. 🚀

---

## ✨ Features
- 📰 **Fetch**: Get the latest news on any topic.
- 📊 **Rank**: Prioritize articles based on relevance, authority, and depth.
- ✍️ **Summarize**: Extract key insights with AI.
- 📄 **PDF Report**: Generate a clickable, shareable PDF summary.
- 🎧 **Audio Podcast**: Convert summaries to audio and publish on Spotify.

---

## 🛠️ Prerequisites
Make sure you have the following installed:
- **Python 3.8+** 🐍
- **Docker** (optional for deployment) 🐳
- Python libraries (see [Dependencies](#dependencies))
- Access to:
  - 🔑 OpenAI API for summarization
  - 🎵 Spotify API for podcast uploads

---

## 🔧 Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/mkudith/PodifyNews.git
   cd PodifyNews
   ```

2.	**Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.	***Set up environment variables***:

    Create a .env file in the project root with the following:

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=your_redirect_uri

4. Run application
docker build -t my_new_project:latest .
	•	-t: Tags the image with a name (my_new_project) and version (latest).

	2.	Verify the Image:
    docker images


5. Run the Container
docker run -d -p 5000:5000 my_new_project:latest
	•	-d: Runs the container in detached mode.
	•	-p: Maps port 5000 on your machine to port 5000 in the container.

	Access the Application:
	•	Open a browser and navigate to http://localhost:8000.

6. Check logs
docker logs <container_id>

---

## 🚀 Usage
	
1.	Run the project:

python main.py


	2.	Enter a topic when prompted (e.g., AI trends in 2025).
	3.	Pipeline steps:
	•	🌐 Fetches and ranks the top 10 news articles.
	•	📝 Summarizes and generates a PDF report.
	•	🎙️ Creates an audio summary and uploads to Spotify.
	4.	Check the output:
	•	📄 PDF: Saved as output/news_report_<topic>.pdf.
	•	🎧 Podcast: Published to your Spotify account.

---

## 🎯 Example Output

PDF Report
	•	Title: AI Trends in 2025
	•	Key Points:
	1.	AI adoption in healthcare is expected to double by 2025. 🏥
	2.	Generative AI tools are becoming mainstream in education and design. ✨
	•	Clickable Links: Navigate to original articles with ease.

Spotify Podcast
	•	Title: AI Trends 2025: Key Takeaways
	•	Description: A 5-minute summary of the latest trends in AI.

## 📚 Dependencies

The project requires the following libraries:
	•	requests 🌐
	•	beautifulsoup4 🍜
	•	fpdf 📄
	•	gtts 🎤
	•	pydub 🎶
	•	spotipy 🎵
	•	openai 🤖

Install them with:

pip install -r requirements.txt

🛠️ Troubleshooting

❌ Port Conflicts

If you encounter a port conflict, try using a different port:

docker run -d -p 8000:8000 PodifyNews

📦 Missing Dependencies

Ensure all required libraries are installed:

pip install -r requirements.txt

🎵 Spotify Upload Issues
	•	Double-check your Spotify API credentials in .env.
	•	Ensure the necessary scopes are granted (ugc-image-upload).

🤝 Contributing

We ❤️ contributions! Fork the repo, make your changes, and submit a pull request. Let’s build something awesome together! 💡

📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
	•	🌟 Inspired by Google’s Bigtable for efficient data organization.
	•	🤖 Summarization powered by OpenAI.

📬 Contact

For questions or support, reach out at ukalbur@ncsu.edu
