from openai import OpenAI
import config
from models import Conversation

client = OpenAI(api_key=config.OPEN_API_KEY)
#명령을 입력하는 로직인것 같음
system_instructions = """너는 감정상담사이고, 글을 쓰면 그 사람이 감동을 받을 수 있게 조언을 해주는 역할을 한다."""

completion = client.chat.completions.create(
    model = "gpt-4.0-turbo",
    messages=[
        {
            "role": "system",
            "content": system_instructions,
        },
        {
            "role" : "user"
            "content" : "Conversation.user_input"
        },
    ],
)
#이거 DB로 저장하는 로직으로 변경해야함
#print(completion.choices[0].message.content)