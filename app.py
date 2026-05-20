import streamlit as st
from analyzer import analyze_sentiment, analyze_batch, extract_keywords, get_entities

st.set_page_config(
    page_title="AWS-Style Sentiment & NLP Analyzer",
    page_icon="🔍",
    layout="wide",
)

st.markdown("""
<style>
    .positive { background:#e6f4ea; border-left:4px solid #34a853; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .negative { background:#fce8e6; border-left:4px solid #ea4335; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .neutral  { background:#f0f7ff; border-left:4px solid #2d7dd2; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .mixed    { background:#fff8e1; border-left:4px solid #fbbc04; border-radius:8px; padding:14px 18px; margin:8px 0; }
    .chip { display:inline-block; background:#e8eef8; border:1px solid #c0d0e8; border-radius:20px; padding:3px 12px; font-size:13px; margin:3px; color:#1a3a6b; }
    .entity-chip { display:inline-block; background:#f0fff4; border:1px solid #a8d5b5; border-radius:20px; padding:3px 12px; font-size:13px; margin:3px; color:#1a7340; }
    .score-bar { height:12px; border-radius:6px; background:linear-gradient(90deg,#34a853,#fbbc04,#ea4335); }
</style>
""", unsafe_allow_html=True)

st.title("🔍 AWS-Style Sentiment & NLP Analyzer")
st.markdown("**Analyze sentiment, extract keywords, and detect entities from any text — mimicking Amazon Comprehend AI services.**")
st.markdown("*Built with Hugging Face Transformers · Inspired by AWS Amazon Comprehend · No API key needed*")
st.divider()

tab1, tab2 = st.tabs(["📝 Single Text Analysis", "📊 Batch Analysis"])

with tab1:
    st.subheader("Analyze a single piece of text")
    sample_texts = [
        "The new data pipeline we deployed reduced processing time by 60% and the team is thrilled with the results.",
        "I'm extremely frustrated with the slow response times and constant errors in the system.",
        "The product has some good features but also several areas that need improvement.",
        "Amazon Bedrock makes it incredibly easy to build generative AI applications at scale.",
    ]
    selected_sample = st.selectbox("Try a sample text or type your own below:", ["-- Type your own --"] + sample_texts)
    text_input = st.text_area(
        "Enter text to analyze:",
        value=selected_sample if selected_sample != "-- Type your own --" else "",
        height=140,
        placeholder="Paste any text here — customer review, feedback, article, email..."
    )

    if st.button("🔍 Analyze", type="primary", use_container_width=True):
        if not text_input.strip():
            st.error("Please enter some text to analyze.")
        else:
            with st.spinner("Running NLP analysis..."):
                sentiment, scores = analyze_sentiment(text_input)
                keywords = extract_keywords(text_input)
                entities = get_entities(text_input)

            st.divider()
            col1, col2 = st.columns([1, 2])

            with col1:
                css_class = sentiment.lower()
                emoji = {"positive": "😊", "negative": "😟", "neutral": "😐", "mixed": "🤔"}.get(sentiment.lower(), "😐")
                st.markdown(f"""
                <div class="{css_class}">
                    <div style="font-size:32px">{emoji}</div>
                    <div style="font-size:22px;font-weight:800;margin-top:4px">{sentiment.upper()}</div>
                    <div style="font-size:13px;color:#555;margin-top:4px">Overall Sentiment</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Confidence Scores:**")
                for label, score in scores.items():
                    st.markdown(f"`{label}` — **{score:.1%}**")
                    st.progress(score)

            with col2:
                st.markdown("**🔑 Key Phrases Extracted:**")
                if keywords:
                    chips = "".join([f'<span class="chip">{kw}</span>' for kw in keywords])
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.markdown("*No key phrases detected.*")

                st.markdown("")
                st.markdown("**🏷️ Entities Detected:**")
                if entities:
                    chips = "".join([f'<span class="entity-chip">{e}</span>' for e in entities])
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.markdown("*No named entities detected.*")

                st.markdown("")
                st.markdown("**📊 AWS Comprehend Equivalent Output:**")
                st.json({
                    "Sentiment": sentiment.upper(),
                    "SentimentScore": {k: round(v, 4) for k, v in scores.items()},
                    "KeyPhrases": keywords[:5],
                    "Entities": entities[:5]
                })

with tab2:
    st.subheader("Analyze multiple texts at once")
    st.markdown("*Enter one text per line*")
    batch_input = st.text_area(
        "Batch input:",
        height=200,
        placeholder="Enter one sentence or review per line...\nLine 1\nLine 2\nLine 3"
    )

    if st.button("🔍 Analyze Batch", type="primary", use_container_width=True):
        lines = [l.strip() for l in batch_input.strip().split("\n") if l.strip()]
        if not lines:
            st.error("Please enter at least one line of text.")
        elif len(lines) > 20:
            st.warning("Maximum 20 lines for batch analysis.")
            lines = lines[:20]
        else:
            with st.spinner(f"Analyzing {len(lines)} texts..."):
                results = analyze_batch(lines)

            st.divider()
            import pandas as pd
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)

            counts = df["Sentiment"].value_counts()
            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(counts)

st.divider()
st.markdown(
    "Built by [Madhavi Akella](https://linkedin.com/in/madhavi-akella-2b8213114) · "
    "[GitHub](https://github.com/madhavi-akella-lab) · "
    "Inspired by AWS Amazon Comprehend"
)
