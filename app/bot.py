from os import getenv

from openai import OpenAI
from dotenv import load_dotenv


class ChatBot:
    load_dotenv()
    client = OpenAI(api_key=getenv('OPENAI_API_KEY'))

    def __call__(self, context: list[dict]):
        result, *_ = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context,
        ).choices
        return result.message.content


if __name__ == '__main__':
    bot = ChatBot()
    print(bot([{"role": "user", "content": "What color is the sky?"}]))
