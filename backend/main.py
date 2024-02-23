from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import logging
import os
import re
import spacy


app = Flask(__name__)
# Should replace the "origins" with {"origins": "https://gpt-assistant-coral.vercel.app/"}, but later
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

nlp = spacy.load("en_core_web_sm") # for english
# nlp = spacy.load("fi_core_web_sm") # for finnish

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment variables")

openai_api_key = os.getenv('OPENAI_API_KEY')

# Keyword/phrases patterns
OUT_OF_SCOPE_PATTERNS = [
    r"\bpython code\b",  
    r"\bprogramming\b",  
    r"\bvideo games\b",  
    r"\bpolitics\b", 
    r"\barts\b",  
    r"\bmovies\b",  
    r"\btelevision\b",  
    r"\bstock market\b",  
    r"\btravel advice\b",  
    # More out of scope patterns here
]

def is_message_out_of_scope(message):
    message_lower = message.lower()  # Convert message to lowercase to ensure case-insensitive matching
    return any(re.search(pattern, message_lower) for pattern in OUT_OF_SCOPE_PATTERNS)

def is_message_related_to_bithabit(message):
    """
    Here we use NLP to determine if the message is related to health and lifestyle.
    This should be better than regex patterns
    """
    doc = nlp(message)
    for token in doc:
        if token.pos_ in ['NOUN', 'VERB']:
            if token.lemma_ in ['exercise', 'diet', 'sleep', 'stress']:
                return True
    return False

@app.route('/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message')
    if not user_message:
        logging.error('No message provided in request')
        return jsonify({"error": "No message provided"}), 400

    try:
        logging.debug('Received user message: %s', user_message)

        # If user message is "out of scope"
        if is_message_out_of_scope(user_message) or not is_message_related_to_bithabit(user_message):
            # Predefined response to redirect the conversation back to habits and health
            redirect_message = "I'm here to help you with your health and habit goals. Let's focus on that instead!"
            return jsonify({"reply": redirect_message})
        
        # If the message is not out of scope, proceed with your existing logic
      
        #System Message:
        system_message = "I am BitHabit, a virtual assistant created by WellPro to help you develop and maintain healthy habits. I am here to provide guidance on fitness, nutrition, and overall well-being."

        #Chat conversation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
     
        #Tailored responses :
        ai_responses = [
            {"role": "assistant", "content": "Hello! I am BitHabit's virtual assistant. How can I assist you today?"},
            {"role": "assistant", "content": "I am here to provide guidance on fitness, nutrition, and overall well-being."},
            {"role": "assistant", "content": "Feel free to ask any questions or seek advice."},
            {"role": "assistant", "content": "BitHabit, created by WellPro, is committed to helping you lead a healthier lifestyle."},
            {"role": "assistant", "content": "WellPro, the company behind BitHabit, specializes in developing innovative solutions for health and wellness."},
            {"role": "assistant", "content": "Our goal at WellPro is to empower individuals like you to make positive changes in their lives."},
            {"role": "assistant", "content": "BitHabit is a product of WellPro, a leading health and wellness company dedicated to improving lives."},
            {"role": "assistant", "content": "At WellPro, we believe that small, consistent changes can lead to significant improvements in health and well-being."},
            {"role": "assistant", "content": "BitHabit and WellPro are here to support you in your journey to better health and a happier life."},
            {"role": "assistant", "content": "Please understand that I cannot provide medical diagnoses or treatments. It's crucial to consult with a healthcare professional for any medical concerns."},
            {"role": "assistant", "content": "I want to emphasize that I am not a substitute for medical or psychological advice. Always seek help from qualified professionals for such matters."},
            {"role": "assistant", "content": "While I can offer general wellness tips, I am not a licensed medical or psychological practitioner. For specific health issues, consult experts in those fields."},
            {"role": "assistant", "content": "Your health and well-being are important. If you have medical or psychological questions, I encourage you to reach out to specialists who can provide appropriate assistance."},
            {"role": "assistant", "content": "I'm here to provide support and information on general well-being. For medical or psychological concerns, it's best to speak with professionals who can address those specific needs."},
            {"role": "assistant", "content": "It's essential to prioritize your health. If you have medical or psychological inquiries, please consult qualified professionals who can offer expert guidance."},
        ]

        ai_message = response.choises[0].message['content'] if response.choices else "Sorry, I didn't quite catch that."

        # Customize responses based on user messages
        if "What can you do?" in user_message:
            ai_message = "I can help you set and track your fitness goals, provide nutritional advice, and offer tips for a healthy lifestyle."
        elif "Can you access my personal data?" in user_message:
            ai_message = "I respect your privacy and do not access personal data without consent."
        elif "How do you handle my data?" in user_message:
            ai_message = "Your data is handled with strict privacy and security measures."
        elif "Can you help with diet plans?" in user_message:
            ai_message = "I can suggest healthy eating habits, but for personalized plans, consult a dietitian."
        elif "How accurate is your advice?" in user_message:
            ai_message = "My advice is based on general guidelines and should not replace professional advice."
        elif "How can I improve my sleep?" in user_message:
            ai_message = "Consider setting a regular sleep schedule and creating a restful environment."
        elif "What exercises do you recommend?" in user_message:
            ai_message = "Exercise choices depend on your fitness level and goals. Consider starting with light activities like walking."
        elif "I'm feeling unmotivated, what should I do?" in user_message:
            ai_message = "Try setting small, achievable goals and celebrate your progress to stay motivated."
        elif "How can I stay committed to my habits?" in user_message:
            ai_message = "Consistency is key. Remind yourself of the benefits and keep a positive mindset."
        elif "The app isn't working, can you help?" in user_message:
            ai_message = "For technical issues, please reach out to BitHabit's support team for assistance."
        elif "I have feedback, where can I send it?" in user_message:
            ai_message = "Your feedback is valuable. Please send it through the feedback option in the app."
        elif "How can I set achievable fitness goals?" in user_message:
            ai_message = "To set achievable fitness goals, start by defining specific, measurable objectives. Break them down into smaller milestones, and create a realistic timeline for each."
        elif "What's a good recipe for a healthy breakfast?" in user_message:
            ai_message = "One healthy breakfast option is a spinach and mushroom omelette. It's rich in protein and vitamins. Saute spinach and mushrooms, then add beaten eggs and cook until set."
        elif "I'm feeling stressed. What can I do?" in user_message:
            ai_message = "Stress can be managed with relaxation techniques like deep breathing, meditation, or yoga. Consider practicing mindfulness to reduce stress levels."
        elif "Can you suggest a workout routine for beginners?" in user_message:
            ai_message = "For beginners, start with 30 minutes of moderate-intensity exercise, like brisk walking, 3-4 times a week. Gradually increase intensity and duration."
        elif "I'm vegetarian. What are some protein sources?" in user_message:
            ai_message = "Vegetarian protein sources include tofu, legumes, quinoa, and nuts. Incorporate these into your diet for a balanced intake of nutrients."
        elif "Can you give me a motivational quote?" in user_message:
            ai_message = "Certainly! Here's a quote: 'The only way to do great work is to love what you do.' – Steve Jobs"
        elif "Can you recommend healthy snacks?" in user_message:
            ai_message = "Sure! Healthy snack options include Greek yogurt with berries, carrot sticks with hummus, or a handful of mixed nuts."
        elif "How can I reduce sugar in my diet?" in user_message:
            ai_message = "To reduce sugar intake, avoid sugary drinks and processed foods. Opt for whole fruits, use natural sweeteners in moderation, and read food labels."
        elif "What's the best way to manage stress?" in user_message:
            ai_message = "Managing stress involves relaxation techniques, regular exercise, spending time in nature, and seeking support from friends or a therapist."
        elif "Can you recommend a good book on nutrition?" in user_message:
            ai_message = "A highly recommended book on nutrition is 'The Omnivore's Dilemma' by Michael Pollan. It explores the food industry and its impact on health."
        elif "How can I improve my posture?" in user_message:
            ai_message = "To improve posture, maintain a neutral spine, sit up straight, and do exercises like back stretches and core strengthening workouts."
        elif "What's the ideal daily water intake?" in user_message:
            ai_message = "The recommended daily water intake varies, but a general guideline is to aim for about 8 glasses (64 ounces) of water a day, or more if physically active."
        elif "Can you recommend a stress-relief app?" in user_message:
            ai_message = "There are several great stress-relief apps available. Consider trying 'Headspace' or 'Calm' for guided meditation and relaxation."
        elif "What are some benefits of regular exercise?" in user_message:
            ai_message = "Regular exercise offers numerous benefits, including improved cardiovascular health, increased energy, reduced stress, and better sleep quality."
        elif "How can I boost my metabolism?" in user_message:
            ai_message = "To boost metabolism, focus on regular physical activity, eat smaller, balanced meals, and stay hydrated. Strength training can also help."
        elif "What's a good way to relieve muscle soreness?" in user_message:
            ai_message = "You can relieve muscle soreness by stretching, applying ice or heat, taking an Epsom salt bath, or trying foam rolling."
        elif "Any tips for improving digestion?" in user_message:
            ai_message = "To improve digestion, eat fiber-rich foods, chew food slowly, stay hydrated, and consider incorporating probiotics into your diet."
        elif "What's a healthy bedtime snack?" in user_message:
            ai_message = "A healthy bedtime snack option is a small serving of Greek yogurt with a drizzle of honey or a banana. Avoid heavy or spicy foods."
        elif "Can you recommend a meditation technique?" in user_message:
            ai_message = "One effective meditation technique is mindfulness meditation. Focus on your breath and observe thoughts without judgment."
        elif "How can I reduce stress at work?" in user_message:
            ai_message = "To reduce work-related stress, prioritize tasks, take short breaks, practice deep breathing, and communicate with your team."
        elif "Can you suggest a quick home workout?" in user_message:
            ai_message = "You can try a 15-minute home workout with bodyweight exercises like push-ups, squats, and planks to get your heart rate up."
        elif "What's the importance of a balanced diet?" in user_message:
            ai_message = "A balanced diet provides essential nutrients for overall health, energy, and disease prevention. It supports your body's functions."

        
        logging.debug('AI response: %s', ai_message)
        return jsonify({"reply": ai_message})
    except Exception as e:
        logging.exception('Error processing message: %s', user_message)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return 'Flask server is running!'

if __name__ == '__main__':
    app.run(debug=True)