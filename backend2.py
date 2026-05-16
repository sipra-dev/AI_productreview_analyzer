from typing import TypedDict
from langgraph.graph import StateGraph, END
from huggingface_hub import InferenceClient
import json
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
HF_TOKEN = os.getenv("key")

client = InferenceClient(token=HF_TOKEN)
MODEL = "Qwen/Qwen2.5-7B-Instruct"


# ---------------- STATE ----------------
class State(TypedDict):
    review: str
    sentiment: str
    aspect: str
    tone: str
    urgency: str
    response: str


# ---------------- NODES ----------------
def detect_sentiment(state: State):
    messages = [
        {"role": "system", "content": "You are a strict sentiment classifier. Only return JSON."},
        {
            "role": "user",
            "content": f"""
Classify sentiment.

Output format:
{{"sentiment": "positive"}} OR {{"sentiment": "negative"}}

Review: {state['review']}
"""
        }
    ]

    response = client.chat_completion(
        model=MODEL,
        messages=messages,
        max_tokens=100,
        temperature=0.0
    )

    output = response.choices[0].message["content"]

    try:
        data = json.loads(output.strip())
    except:
        data = {"sentiment": "negative"}

    return {"sentiment": data["sentiment"]}


def positive_response(state: State):
    messages = [
        {"role": "system", "content": "You are a warm and friendly assistant."},
        {
            "role": "user",
            "content": f"""
Write a short thank-you message.

Review: {state['review']}
"""
        }
    ]

    response = client.chat_completion(
        model=MODEL,
        messages=messages,
        max_tokens=100,
        temperature=0.5
    )

    output = response.choices[0].message["content"]
    return {"response": output.strip()}


def analyze_negative(state: State):
    content = f"""
Analyze the review carefully.

STRICT RULES:
- Identify SPECIFIC aspects
- Do NOT write "general"
- Multiple issues → comma-separated
- Tone: disappointed, frustrated, angry, neutral
- Urgency: low, medium, high

Return ONLY JSON:
{{
    "aspect": "...",
    "tone": "...",
    "urgency": "..."
}}

Review: {state['review']}
"""

    messages = [
        {"role": "system", "content": "You are an expert review analyst. Output only JSON."},
        {"role": "user", "content": content}
    ]

    response = client.chat_completion(
        model=MODEL,
        messages=messages,
        max_tokens=150,
        temperature=0.2
    )

    output = response.choices[0].message["content"]

    try:
        data = json.loads(output.strip())

        if data.get("aspect", "").lower() == "general":
            data["aspect"] = "customer support, service quality"

    except:
        data = {
            "aspect": "customer support, service quality",
            "tone": "frustrated",
            "urgency": "high"
        }

    return data


def generate_response(state: State):
    messages = [
        {"role": "system", "content": "You are a polite customer support agent."},
        {
            "role": "user",
            "content": f"""
A user gave a negative review.

Aspect: {state['aspect']}
Tone: {state['tone']}
Urgency: {state['urgency']}

Write a professional response.
"""
        }
    ]

    response = client.chat_completion(
        model=MODEL,
        messages=messages,
        max_tokens=150,
        temperature=0.5
    )

    output = response.choices[0].message["content"]
    return {"response": output.strip()}


# ---------------- ROUTING ----------------
def route(state: State):
    return "positive" if state["sentiment"] == "positive" else "negative"


# ---------------- GRAPH ----------------
def build_graph():
    builder = StateGraph(State)

    builder.add_node("sentiment", detect_sentiment)
    builder.add_node("positive", positive_response)
    builder.add_node("negative_analysis", analyze_negative)
    builder.add_node("response", generate_response)

    builder.set_entry_point("sentiment")

    builder.add_conditional_edges(
        "sentiment",
        route,
        {
            "positive": "positive",
            "negative": "negative_analysis"
        }
    )

    builder.add_edge("positive", END)
    builder.add_edge("negative_analysis", "response")
    builder.add_edge("response", END)

    return builder.compile()


# expose function for app
graph = build_graph()

def run_review(review_text: str):
    return graph.invoke({"review": review_text})