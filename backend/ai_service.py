from openai import OpenAI
import json

# مفتاح OpenAI الخاص بك
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

class AIService:
    model_name = "gpt-4o-mini"

    @staticmethod
    def generate_bio(name, teach_skills, learn_skills, headline=""):
        """توليد بايو ذكي يربط الخبرات بالأهداف التعليمية."""
        system_msg = "You are a professional brand strategist. Connect expertise with learning goals creatively."
        user_msg = f"""
        User: {name}
        Headline: {headline if headline else "Expert Mentor"}
        Teaches: {teach_skills}
        Learns: {learn_skills}

        Task: Write a fresh 2-sentence bio. Link what they teach with what they learn in a punchy way. 
        Variety: Ensure this is unique and sounds human, not like a template.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
                temperature=1.0,  # لضمان عدم التكرار
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Bio Error: {e}")
            return f"Expert in {teach_skills} with a hunger for {learn_skills}."

    @staticmethod
    def get_smart_matches(learner_interests, teachers_list):
        """مطابقة ذكية تعتمد على التفكير المنطقي وليس فقط الكلمات."""
        if not learner_interests: return []
        teachers_json = json.dumps(teachers_list)
        system_msg = "You are a matchmaking engine. Return top 3 matches as JSON matches:[]"
        user_msg = f"Learner interests: {learner_interests}\nMentors available: {teachers_json}"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content).get("matches", [])
        except: return []