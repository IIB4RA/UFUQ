import google.generativeai as genai
import json
import os

# ⚠️ تأكد من وضع مفتاحك هنا
GENAI_API_KEY = "YOUR_API_KEY_HERE"

genai.configure(api_key=GENAI_API_KEY)

class AIService:
    model = genai.GenerativeModel('gemini-1.5-flash')

    @staticmethod
    def clean_ai_response(text):
        """تنظيف النص من رموز الماركداون لتجنب الأخطاء"""
        return text.replace("```json", "").replace("```", "").strip()

    @staticmethod
    def generate_bio(name, skills, headline=""):
        """توليد بايو يعتمد على الاسم، المهارات، والعنوان الوظيفي"""
        
        # تحسين البرومبت ليأخذ الـ Headline بعين الاعتبار
        prompt = f"""
        Act as a professional profile writer.
        Write a concise, engaging, and professional bio (max 2 lines) for a user on a mentorship platform.
        
        User Details:
        - Name: {name}
        - Job Title/Headline: {headline if headline else "Expert"}
        - Skills: {skills}
        
        Instructions:
        - Focus on how they can help others based on their Headline and Skills.
        - Do NOT include hashtags.
        - Write in English only.
        - Return ONLY the bio text, nothing else.
        """
        try:
            response = AIService.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"AI Bio Error: {e}")
            return f"Professional mentor specializing in {skills}. Ready to help you achieve your goals."

    @staticmethod
    def get_smart_matches(learner_interests, teachers_list):
        """مطابقة ذكية تعيد بيانات بصيغة JSON حصراً"""
        if not learner_interests:
            return []

        teachers_json = json.dumps(teachers_list)
        
        prompt = f"""
        Act as a matchmaking algorithm. 
        I have a learner interested in: {learner_interests}.
        Here is a list of available teachers: {teachers_json}.
        
        Task:
        Select the best 3 matches based on skills overlap.
        
        Output Format:
        You MUST return a valid JSON array strictly like this:
        [
            {{"id": "TEACHER_ID", "name": "NAME", "role": "Their Headline or Main Skill", "match_percentage": "95%", "reason": "Why matched"}}
        ]
        
        Constraints:
        - Return ONLY JSON. No intro text. No markdown.
        """
        try:
            response = AIService.model.generate_content(prompt)
            clean_text = AIService.clean_ai_response(response.text)
            return json.loads(clean_text)
        except Exception as e:
            print(f"AI Match Error: {e}")
            # إرجاع قائمة فارغة بدلاً من تحطيم الموقع
            return []