import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Loads variables from your .env file
load_dotenv()

class LLMClient:
    def __init__(self):
        # Creates OpenAI client using your API key
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Tracks total tokens used across calls
        self.total_tokens = 0

    def generate(self, prompt, retries=3):
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                # Tracks tokens used
                tokens = response.usage.total_tokens
                self.total_tokens += tokens

                return {
                    "text": response.choices[0].message.content,
                    "tokens_used": tokens
                }

            except Exception as e:
                print(f"Retry {attempt + 1}: {e}")
                time.sleep(2)

        raise Exception("LLM failed after retries")