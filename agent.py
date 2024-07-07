import openai
from chatgpt_config import GPT_MODEL
from prompt import generate_prompt
from database import execute_query

class LLM_Agent:
    def __init__(self, db_config):
        self.db_config = db_config

    def query_chatgpt(self, prompt):
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "system", "content": "You are a Python programming assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message['content'].strip()

    def process_question(self, question):
        prompt = generate_prompt(question, self.db_config)
        final_code = None
        for attempt in range(3):
            code = self.query_chatgpt(prompt)
            try:
                result = execute_query(code, self.db_config)
                final_code = code
                break
            except Exception as e:
                print(f"Error occurred with the generated code:\n{code}\nError details:\n{str(e)}\n")
                error_prompt = f"{prompt}\nThe following error occurred:\n{str(e)}\nPlease fix the code."
                prompt = error_prompt

        if final_code:
            with open('result.py', 'w') as file:
                file.write(final_code)
            return result
        else:
            return "Unable to retrieve the data after 3 attempts."
