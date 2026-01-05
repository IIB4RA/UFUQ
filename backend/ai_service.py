import google.generativeai as genai
import json


API_KEY = "AIzaSyCbr1FoVF24f0P6v1_qZbL1fWoJryEFu9s"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # موديل سريع ومجاني


class AIService:

    # --- النقطة 1: المطابقة الذكية (Smart Match) ---
    @staticmethod
    def get_smart_matches(learner_skills, teachers_list):
        prompt = f"""
        Act as a professional educational matchmaker.
        Student Interests: {learner_skills}
        Available Teachers: {teachers_list}

        Task: Find the top 3 best matching teachers. 
        Even if keywords don't match exactly, use semantic meaning (e.g., 'Web' matches 'HTML').
        Return ONLY a JSON array of objects with: 
        "teacher_id", "match_percentage", and "reason_in_arabic".
        """
        try:
            response = model.generate_content(prompt)
            # تنظيف النص المستلم لتحويله لـ JSON
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    # --- النقطة 2: ملخص الجلسة (Session Summary) ---
    @staticmethod
    def summarize_session(chat_history):
        prompt = f"""
            Analyze this chat history from an educational session. 
            Create a professional summary including:
            1. Topics covered.
            2. Important notes.
            3. Homework/Next steps.

            Important: Use the same language(s) used in the chat (Arabic, English, or both).
            Chat History: {chat_history}
            """
        response = model.generate_content(prompt)
        return response.text


    # In ai_service.py
@staticmethod
def generate_bio(name, skills):
    # Added instructions for uniqueness and creative variety
    prompt = f"""
    Create a unique, professional 2-line bio for a mentor named {name}.
    Their expertise includes: {skills}.
    
    Requirements:
    - Make it different from common generic bios.
    - Focus on the specific skills provided.
    - Professional but engaging tone.
    - English only.
    """
    try:
        # Use a fresh request every time
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Expert mentor dedicated to sharing specialized knowledge and helping learners grow."