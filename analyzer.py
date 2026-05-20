import re
import numpy as np
from collections import Counter


# ── Simple lexicon-based sentiment (no heavy dependencies) ──────────────────
POSITIVE_WORDS = {
    "great", "excellent", "amazing", "fantastic", "wonderful", "outstanding",
    "good", "best", "love", "happy", "pleased", "satisfied", "impressive",
    "efficient", "effective", "successful", "improved", "fast", "easy",
    "helpful", "reliable", "powerful", "innovative", "excited", "thrilled",
    "perfect", "brilliant", "superb", "exceptional", "delighted", "positive",
    "reduced", "increased", "boosted", "streamlined", "optimized", "enhanced",
    "intuitive", "seamless", "robust", "scalable", "accurate", "incredible"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "worst", "poor", "hate",
    "frustrated", "disappointed", "slow", "error", "broken", "failed",
    "useless", "annoying", "confusing", "difficult", "problem", "issue",
    "bug", "crash", "delay", "expensive", "unreliable", "unhappy",
    "frustrating", "disappointing", "inadequate", "lacking", "missing",
    "constant", "errors", "wrong", "ugly", "complicated", "painful"
}

INTENSIFIERS = {"very", "extremely", "incredibly", "absolutely", "really", "quite", "highly"}
NEGATORS = {"not", "no", "never", "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't"}


def analyze_sentiment(text):
    """
    Lexicon-based sentiment analysis mimicking Amazon Comprehend output.
    Returns (sentiment_label, scores_dict)
    """
    words = re.findall(r'\b\w+\b', text.lower())

    pos_score = 0
    neg_score = 0
    i = 0

    while i < len(words):
        word = words[i]
        multiplier = 1.0

        # Check for intensifier before this word
        if i > 0 and words[i-1] in INTENSIFIERS:
            multiplier = 1.5

        # Check for negator before this word
        negated = False
        if i > 0 and words[i-1] in NEGATORS:
            negated = True
        if i > 1 and words[i-2] in NEGATORS:
            negated = True

        if word in POSITIVE_WORDS:
            if negated:
                neg_score += multiplier
            else:
                pos_score += multiplier
        elif word in NEGATIVE_WORDS:
            if negated:
                pos_score += multiplier * 0.5
            else:
                neg_score += multiplier
        i += 1

    total = pos_score + neg_score + 0.5  # avoid zero division
    pos_ratio = pos_score / total
    neg_ratio = neg_score / total

    # Determine label
    if pos_ratio > 0.6:
        label = "Positive"
    elif neg_ratio > 0.6:
        label = "Negative"
    elif pos_ratio > 0.3 and neg_ratio > 0.3:
        label = "Mixed"
    else:
        label = "Neutral"

    # Build scores (must sum to 1)
    neutral_score = max(0.05, 1.0 - pos_ratio - neg_ratio)
    mixed_score = min(0.15, pos_ratio * neg_ratio)

    raw = {
        "Positive": pos_ratio,
        "Negative": neg_ratio,
        "Neutral": neutral_score,
        "Mixed": mixed_score,
    }
    total_raw = sum(raw.values())
    scores = {k: v / total_raw for k, v in raw.items()}

    return label, scores


def extract_keywords(text):
    """Extract meaningful key phrases from text."""
    # Remove common stop words
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "this", "that", "these", "those", "it", "its",
        "we", "our", "they", "their", "i", "my", "you", "your", "he", "she",
        "also", "very", "just", "so", "as", "if", "then", "than", "when",
        "what", "which", "who", "how", "all", "some", "any", "more", "most"
    }

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in stop_words]
    counts = Counter(filtered)

    # Get top keywords
    keywords = [word for word, count in counts.most_common(12)]
    return keywords


def get_entities(text):
    """Simple rule-based named entity detection."""
    entities = []

    # Capitalized words (likely proper nouns)
    capitalized = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
    # Filter out sentence starters (words after period or at start)
    sentences = text.split('.')
    first_words = set()
    for s in sentences:
        s = s.strip()
        if s:
            first_word = s.split()[0] if s.split() else ""
            first_words.add(first_word)

    for word in capitalized:
        if word not in first_words and word not in entities:
            entities.append(word)

    # Known tech entities
    tech_entities = [
        "AWS", "Azure", "Databricks", "Snowflake", "Python", "SQL",
        "SageMaker", "Bedrock", "Comprehend", "Rekognition", "Lambda",
        "Streamlit", "LangChain", "OpenAI", "Hugging", "FAISS", "Spark",
        "Amazon", "Microsoft", "Google", "IBM", "Accenture"
    ]
    for entity in tech_entities:
        if entity.lower() in text.lower() and entity not in entities:
            entities.append(entity)

    return entities[:10]


def analyze_batch(texts):
    """Analyze a list of texts and return results as list of dicts."""
    results = []
    for text in texts:
        sentiment, scores = analyze_sentiment(text)
        results.append({
            "Text": text[:80] + "..." if len(text) > 80 else text,
            "Sentiment": sentiment,
            "Positive %": f"{scores['Positive']:.1%}",
            "Negative %": f"{scores['Negative']:.1%}",
            "Neutral %": f"{scores['Neutral']:.1%}",
        })
    return results
