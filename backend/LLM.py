from openai import OpenAI
class GPT3:
    def __init__(self):
        self.client = OpenAI()
        
    def generate(self, prompt, max_length=800):
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_length,
            temperature=0.3
        )
        
        return response.choices[0].message.content

        
