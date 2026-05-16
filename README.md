💬 AI Review Analyzer

An AI-powered customer review analysis system built using LangGraph, Hugging Face Inference API, LLM-based sentiment analysis, and Streamlit.

The system intelligently analyzes customer reviews, detects sentiment, identifies complaint aspects, evaluates urgency and tone, and automatically generates professional customer support responses.

🚀 Features

💬 Analyze customer reviews using AI

🧠 LLM-powered sentiment classification

📌 Automatic aspect extraction from negative reviews

🎭 Tone detection:

    Disappointed
    Frustrated
    Angry
    Neutral

⚡ Urgency detection:

    Low
    Medium
    High

🤖 Automatic AI-generated customer support responses

🔀 LangGraph-based workflow orchestration

🖥️ Interactive Streamlit frontend

🧠 Tech Stack

Python

Streamlit

LangGraph

Hugging Face Inference API

Qwen2.5-7B-Instruct

JSON-based structured prompting

dotenv

🏗️ Architecture

Customer Review → Sentiment Detection → Conditional Routing → Negative Review Analysis → AI Response Generation → Final Output

📌 How It Works

User enters a customer review

LLM classifies sentiment as:

    Positive
    Negative

If review is positive:

    AI generates a thank-you response

If review is negative:

    System analyzes complaint aspects
    Detects tone and urgency
    Generates professional support response

LangGraph manages the workflow routing automatically.

🔀 LangGraph Workflow
Review Input
      ↓
Sentiment Detection
      ↓
 ┌───────────────┐
 │               │
Positive      Negative
 │               │
Thank You    Review Analysis
Response          ↓
             Tone Detection
             Aspect Detection
             Urgency Detection
                    ↓
          AI Support Response
📊 Example Output
Positive Review
{
  "sentiment": "positive",
  "response": "Thank you so much for your wonderful feedback! We truly appreciate your support."
}
Negative Review
{
  "sentiment": "negative",
  "aspect": "customer support, delivery",
  "tone": "frustrated",
  "urgency": "high",
  "response": "We sincerely apologize for your experience. Our team will look into the delivery and support issues immediately."
}
⚡ Intelligent Routing

The application uses conditional graph routing:

Positive reviews → Thank-you generation
Negative reviews → Deep issue analysis pipeline

This creates efficient task-specific AI workflows.

🧪 Core AI Capabilities
Sentiment Analysis

Detects whether a review is:

Positive
Negative
Aspect Extraction

Identifies specific complaint areas such as:

delivery
customer support
pricing
product quality
refund issues
Tone Detection

Understands emotional intensity of reviews.

Urgency Classification

Determines escalation priority.

Response Generation

Creates professional customer support replies automatically.
