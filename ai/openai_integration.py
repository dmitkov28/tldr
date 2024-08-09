from openai import OpenAI


def get_openai_analysis(input_data: str):
    openai_client = OpenAI()
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                You are a helpful assistant, expert software engineer. 
                You will receive tech news, github repositories, assess the data you're given
                and provide useful summaries and insights into emerging trends around software.
                Focus on the following topics: web development, cloud infrastructure, AI, LLMs, Python, JS Frameworks, data science.
                Format your analysis as HTML. Use headings and paragraphs.
                """,
            },
            {"role": "user", "content": input_data},
        ],
    )
    return completion.choices[0].message.content
