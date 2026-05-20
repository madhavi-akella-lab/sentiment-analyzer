# 🔍 AWS-Style Sentiment & NLP Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![NLP](https://img.shields.io/badge/NLP-Sentiment_Analysis-yellow)
![AWS](https://img.shields.io/badge/Inspired_by-Amazon_Comprehend-FF9900?logo=amazonaws)
![Streamlit](https://img.shields.io/badge/Deployed-Streamlit_Cloud-FF4B4B?logo=streamlit)

> **Analyze sentiment, extract key phrases, and detect entities from any text — mimicking Amazon Comprehend AI services. No API key needed.**

---

## 📌 What This Project Does

This project replicates the core functionality of **Amazon Comprehend** — AWS's managed NLP service — using a lightweight, free implementation. It demonstrates understanding of AWS AI/ML services and NLP fundamentals without requiring cloud credentials.

**Capabilities:**
- 🎭 **Sentiment Analysis** — Positive, Negative, Neutral, Mixed with confidence scores
- 🔑 **Key Phrase Extraction** — Identifies the most meaningful terms in text
- 🏷️ **Entity Detection** — Recognizes people, organizations, and tech terms
- 📊 **Batch Analysis** — Process multiple texts at once with distribution charts
- 🖥️ **AWS Comprehend-style JSON output** — mirrors real API response format

---

## 🏗️ Architecture

```
Input Text
    │
    ▼
Text Preprocessing (tokenization, lowercasing)
    │
    ├──► Sentiment Engine
    │         • Lexicon-based scoring
    │         • Negation handling
    │         • Intensifier detection
    │         • Confidence score generation
    │
    ├──► Key Phrase Extractor
    │         • Stop word removal
    │         • Frequency-based ranking
    │         • Top-K phrase selection
    │
    └──► Entity Detector
              • Capitalization patterns
              • Tech entity dictionary
              • Named entity recognition
                   │
                   ▼
          AWS Comprehend-style JSON Output
          + Streamlit Visual Dashboard
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| NLP Engine | Custom lexicon-based (mirrors Amazon Comprehend) |
| Batch Processing | Pandas |
| Frontend | Streamlit |
| Language | Python 3.10+ |
| Deployment | Streamlit Cloud / GitHub |

---

## ☁️ AWS Connection

This project is directly inspired by **Amazon Comprehend** — AWS's fully managed NLP service. The output format mirrors the real Comprehend API response:

```json
{
  "Sentiment": "POSITIVE",
  "SentimentScore": {
    "Positive": 0.9876,
    "Negative": 0.0021,
    "Neutral": 0.0089,
    "Mixed": 0.0014
  },
  "KeyPhrases": ["data pipeline", "processing time", "team"],
  "Entities": ["AWS", "Databricks", "Python"]
}
```

In production, this would be replaced with direct `boto3` calls to Amazon Comprehend:
```python
import boto3
comprehend = boto3.client('comprehend', region_name='us-east-1')
response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
```

---

## ✨ Key Features

- 🎭 **4-class sentiment** — Positive, Negative, Neutral, Mixed (same as AWS Comprehend)
- 📊 **Confidence scores** — probability distribution across all sentiment classes
- 🔑 **Key phrase extraction** — top meaningful terms ranked by frequency
- 🏷️ **Entity recognition** — detects tech companies, tools, and proper nouns
- 📋 **Batch mode** — analyze up to 20 texts simultaneously with distribution chart
- 🖥️ **JSON output panel** — shows AWS Comprehend-equivalent response format

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/madhavi-akella-lab/sentiment-analyzer
cd sentiment-analyzer
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
sentiment-analyzer/
├── app.py          # Streamlit UI — single and batch analysis
├── analyzer.py     # NLP engine — sentiment, keywords, entities
├── requirements.txt
└── README.md
```

---

## 🔮 Production Enhancement Path

| Current (Free) | Production (AWS) |
|---|---|
| Lexicon-based sentiment | Amazon Comprehend API |
| Rule-based entities | Amazon Comprehend Entities API |
| Keyword frequency | Amazon Comprehend Key Phrases API |
| Local processing | AWS Lambda + API Gateway |
| Streamlit UI | React frontend on AWS Amplify |

---

## 👩‍💻 About

**Madhavi Akella** — Data & AI Engineer | Databricks Generative AI Engineer Associate

🔗 [LinkedIn](https://linkedin.com/in/madhavi-akella-2b8213114) · 🌐 [Portfolio](https://madhavi-akella.netlify.app) · ⬡ [GitHub](https://github.com/madhavi-akella-lab)
