import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Flask App and Gemini Client
app = Flask(__name__)
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    itinerary = None
    
    if request.method == "POST":
        # Extract inputs from the HTML form
        destination = request.form.get("destination")
        days = request.form.get("days")
        budget = request.form.get("budget")
        interests = request.form.get("interests")
        
        # Craft a highly structured, student-focused prompt
        prompt = f"""
        You are an expert AI Travel Agent specializing in budget-friendly student travel. 
        Create a detailed, personalized {days}-day itinerary for a student trip to {destination}.
        
        Trip Details:
        - Total Budget: ${budget} USD (Must include rough estimates for food, transit, and activities).
        - Core Interests: {interests}
        
        Strict Guidelines:
        1. Prioritize budget-saving hacks: Mention public transportation options, free-admission days (like museums), student discounts (ISIC card tips), and cheap/local street food hubs.
        2. Keep the formatting visually organized, scannable, and engaging using Markdown headings, bullet points, and tables where applicable.
        3. Do not suggest high-end luxury activities. Suggest hostels, free parks, walking tours, and authentic, budget-friendly student spots.
        4. Organize the layout strictly into an Overview section, a Day-by-Day breakdown, and a Final Budget Breakdown table.
        """
        
        try:
            # Request generation from the recommended model
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            itinerary = response.text
        except Exception as e:
            itinerary = f"An error occurred while generating your travel plan: {str(e)}"
            
    return render_template("index.html", itinerary=itinerary)

if __name__ == "__main__":
    app.run(debug=True)