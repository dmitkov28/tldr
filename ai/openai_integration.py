from openai import OpenAI


def analyze_with_openai(system_prompt: str, prompt: str, model: str = "gpt-4o") -> str:
    openai_client = OpenAI()
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
