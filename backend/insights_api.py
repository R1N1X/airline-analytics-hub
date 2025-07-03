# backend/insights_api.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_insights(flight_data: list) -> str:
    try:
        limited_data = flight_data[:20]

        system_prompt = """
        You are a data analyst specializing in airline demand and route optimization.
        Analyze the provided flight data and generate clear insights about:
        - Popular routes
        - Busy times of day
        - Any demand patterns or anomalies
        Format insights in short bullet points.
        """

        user_prompt = f"Here is flight data:\n\n{json.dumps(limited_data, indent=2)}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating insights: {str(e)}"
