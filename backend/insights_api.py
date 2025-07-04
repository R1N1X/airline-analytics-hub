import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(flights):
    try:
        summary_data = f"Total flights: {len(flights)}\n"
        airlines = list(set(f["airline"] for f in flights if f["airline"] != "N/A"))
        summary_data += f"Airlines involved: {', '.join(airlines)}\n"

        prompt = (
            "You are a market analyst for the aviation industry. "
            "Analyze the following flight data and provide key trends, insights on airline activity, pricing strategies, and popular routes.\n\n"
            f"{summary_data}\n\n"
            "Give a concise summary with insights (max 100 words)."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an aviation industry expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return response.choices[0].message["content"]
    except Exception as e:
        return f"AI Insight error: {e}"
