from flask import Flask, request, jsonify, render_template
import openai
import os

from openai import OpenAI

app = Flask(__name__)

# Set your OpenAI API key
openai_key = "<your_key_here>"
client = OpenAI(
    api_key=openai_key,  # This is the default and can be omitted
)

# Predefined travel packages
travel_packages = {
    "New York": {
        "description": "Experience the city that never sleeps with landmarks like Times Square, the Statue of Liberty, and Broadway.",
        "url": "https://example.com/new-york-package"
    },
    "Paris": {
        "description": "Discover the charm of the City of Light, from the Eiffel Tower to world-class art at the Louvre.",
        "url": "https://example.com/paris-package"
    },
    "Tokyo": {
        "description": "Explore Japan's bustling capital with its neon-lit streets, historic temples, and sushi delicacies.",
        "url": "https://example.com/tokyo-package"
    },
    "Sydney": {
        "description": "Enjoy the beauty of Sydney's harbor, its iconic Opera House, and sunny beaches like Bondi.",
        "url": "https://example.com/sydney-package"
    },
    "Cape Town": {
        "description": "Marvel at South Africa's Table Mountain, stunning coastline, and vibrant cultural scene.",
        "url": "https://example.com/cape-town-package"
    },
    "Rio de Janeiro": {
        "description": "Dance to the rhythms of Rio with its famous beaches, Christ the Redeemer statue, and carnival festivities.",
        "url": "https://example.com/rio-package"
    },
    "Dubai": {
        "description": "Experience luxury in Dubai with its skyscrapers, desert safaris, and world-class shopping.",
        "url": "https://example.com/dubai-package"
    },
    "London": {
        "description": "Discover London's rich history, from Buckingham Palace to the British Museum and the River Thames.",
        "url": "https://example.com/london-package"
    },
    "Singapore": {
        "description": "Visit the Lion City with its stunning Marina Bay Sands, diverse cuisine, and lush Gardens by the Bay.",
        "url": "https://example.com/singapore-package"
    },
    "Istanbul": {
        "description": "Walk through history in Istanbul, a city that bridges Europe and Asia with its bazaars and mosques.",
        "url": "https://example.com/istanbul-package"
    },
    "Los Angeles": {
        "description": "Explore Hollywood, sunny beaches, and the glamor of the entertainment capital of the world.",
        "url": "https://example.com/los-angeles-package"
    },
    "Hong Kong": {
        "description": "Immerse yourself in the vibrant energy of Hong Kong with its skyline, harbor, and unique culture.",
        "url": "https://example.com/hong-kong-package"
    },
    "Rome": {
        "description": "Step back in time in Rome, with ancient landmarks like the Colosseum, Vatican City, and Roman Forum.",
        "url": "https://example.com/rome-package"
    },
    "Cairo": {
        "description": "Discover the wonders of ancient Egypt with the Pyramids of Giza and the Nile River in Cairo.",
        "url": "https://example.com/cairo-package"
    },
    "Toronto": {
        "description": "Enjoy the multicultural charm of Toronto, featuring the CN Tower, diverse neighborhoods, and waterfront views.",
        "url": "https://example.com/toronto-package"
    }
}


def get_travel_package_response(user_input):
    # Simple keyword matching for predefined travel packages
    for destination, details in travel_packages.items():
        if destination.lower() in user_input.lower():
            return f"We recommend our {destination} package! {details['description']} More details: {details['url']}"

    # Use ChatGPT if no match is found
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel assistant. Suggest packages based on user input. In case you don't have a match with the user input, you can recomment the city the user has been input first and get back with a mocked package url, if there is no city found in the user input, just ask is there a city the user would love to travel. "},
                {"role": "user", "content": user_input},
            ]
        )

        print(str(response))
        return response.choices[0].message.content
    except Exception as e:
        print(str(e))
        return "Sorry, I couldn't process your request at the moment."

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"reply": "Please provide a message."})
    
    # Generate a response
    reply = get_travel_package_response(user_input)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
