import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def clean_json_content(content: str) -> str:
    content = content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "", 1).strip()
    if content.startswith("```"):
        content = content.replace("```", "", 1).strip()
    if content.endswith("```"):
        content = content[:-3].strip()
    return content


def generate_questions(topic: str) -> list[str]:
    prompt = f"""
You are an AI interviewer.

Generate exactly 5 thoughtful, concise, open-ended interview questions about this topic:
"{topic}"

Requirements:
- Questions should flow from general to specific
- Avoid repetition
- Keep each question under 25 words
- Return valid JSON only in this format:
{{
  "questions": ["question 1", "question 2", "question 3", "question 4", "question 5"]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate structured interview questions."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content
    content = clean_json_content(content)
    data = json.loads(content)
    return data["questions"]


def generate_summary(topic: str, qa_pairs: list[dict]) -> dict:
    formatted_qa = "\n".join(
        [f"Q: {pair['question']}\nA: {pair['answer']}" for pair in qa_pairs]
    )

    prompt = f"""
You are analyzing a short interview transcript.

Topic: {topic}

Questions and answers:
{formatted_qa}

Return valid JSON only in this format:
{{
  "summary": "3-5 sentence summary",
  "sentiment": "positive | neutral | negative",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze interview transcripts and return structured JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
    )

    content = response.choices[0].message.content
    content = clean_json_content(content)
    data = json.loads(content)
    return data