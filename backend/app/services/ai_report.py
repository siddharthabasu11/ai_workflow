from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_report(metrics: dict, code_sample: str) -> str:
    prompt = f"""You are a senior software engineer reviewing a codebase for the first time.

Metrics:
- File count: {metrics['file_count']}
- Total lines of code: {metrics['total_loc']}
- Language breakdown: {metrics['language_breakdown']}
- Largest files: {metrics['largest_files']}

Code sample:
{code_sample}

Write a concise engineering report (3-4 short paragraphs) covering:
1. What this project appears to be and its likely purpose
2. Code organization and structure quality
3. Any notable risks or areas needing attention
4. One concrete improvement suggestion"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )

    return response.choices[0].message.content