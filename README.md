
# 🎬 Movie Recommender

# SU Movie Recommender (Content-Based)

A comprehensive, intelligent movie recommendation system that analyzes movie metadata including genres, keywords, cast, crew, and plot overview to generate accurate recommendations using multiple similarity algorithms.
Users can search or select a movie and receive the top-5 recommended movies through a fast, web-based interface.


## Features
Advanced content-based recommendation engine
Bag of Words (CountVectorizer) on combined movie tags
Text preprocessing with stemming and normalization
Multiple recommendation algorithms
Cosine Similarity
Dot Product similarity
Euclidean Distance
Manhattan Distance
Popularity-based recommendations
Precomputed artifacts for high performance
Trained CountVectorizer
Multiple similarity matrices saved as .pkl
Fast startup and instant recommendations
Flask web application
Search or select movies from dropdown
Algorithm selection support
Displays top-5 movie recommendations with posters (TMDB API)


## Quick Start

1. Clone repo:
```bash
git clone https://github.com/YOUR-USERNAME/SU Movie Recommender.git
cd SU Movie Recommender
```


Create & activate virtualenv:
```bash
python -m venv venv
```
# Windows
```bash
venv\Scripts\activate
```
# macOS / Linux
```bash
source venv/bin/activate
```


Install dependencies:
```bash
pip install -r requirements.txt
```

(One-time) Run training pipeline to generate artifacts:

# run training pipeline script (adjust path if different)
```bash
python -m src.pipeline.training_pipeline
```

This creates artifacts like similarity.pkl and final_df.csv under SU Movie Recommender/artifacts/.

Run Flask app:

```bash
python app.py
```

🚀 App Usage & Quick Access<br><br>
Your SU Movie Recommender application should be running at the following address:

🌐 Open in Browser: http://127.0.0.1:5000

<h4>How to Get Recommendations:</h4><br>
Input: Type your favorite movie's name into the search bar (or select it from the list).<br><br>
Output: Click Recommend button to instantly view the Top 5 similar movie suggestions with posters.<br><br>

<table style="width: 100%; border-collapse: collapse;">
    <thead>
        <tr style="background-color: #333; color: white;">
            <th style="padding: 10px; border: 1px solid #555; text-align: left;">Category</th>
            <th style="padding: 10px; border: 1px solid #555; text-align: left;">Issue</th>
            <th style="padding: 10px; border: 1px solid #555; text-align: left;">Solution / Best Practice</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #555;">🚨 **Module Error**</td>
            <td style="padding: 10px; border: 1px solid #555;"><code>ModuleNotFoundError: No module named 'src'</code></td>
            <td style="padding: 10px; border: 1px solid #555;">Run modules using the **<code>-m</code> flag** from the root directory:<br><code>python -m src.pipeline.training_pipeline</code></td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #555;">⏱️ **Performance**</td>
            <td style="padding: 10px; border: 1px solid #555;">Flask app takes **too long** to start.</td>
            <td style="padding: 10px; border: 1px solid #555;">Ensure the **training pipeline** (which generates artifacts) has been completed before starting <code>app.py</code>.</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #555;">🔒 **Git Security**</td>
            <td style="padding: 10px; border: 1px solid #555;">Committing large artifacts (e.g., <code>similarity.pkl</code>).</td>
            <td style="padding: 10px; border: 1px solid #555;">Do not commit artifact files. Ensure the <code>SU Movie Recommender/artifacts/</code> folder is added to **<code>.gitignore</code>**.</td>
        </tr>
    </tbody>
</table><br><br>
<h4>⚖️ License</h4><br>
This project is provided for Learning, Exploration, and Personal Projects only. Feel free to explore and modify the code!

