from openai import OpenAI
from advice_generation.config import OPEN_API_KEY
from models import Conversation

client = OpenAI(api_key=OPEN_API_KEY)
#명령을 입력하는 로직인것 같음
system_instructions = """너는 감정상담사이고, 글을 쓰면 그 사람이 감동을 받을 수 있게 조언을 해주는 역할을 한다."""

def get_chat_response(user_input):
    #챗봇답변
    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {
                "role": "system",
                "content": system_instructions,

            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )
#이거 DB로 저장하는 로직으로 변경완료
bot_response = get_chat_response.completion.choices[0].message.content
#이게 맞는지 모르겟음 같은 completion인가?

conversation = Conversation.objects.create(
    user=Conversation.user,
    user_input=Conversation.user_input,
    bot_response=Conversation.bot_response
)


#config가 두개임, 근데 API키를 가리키고 있지는 않는 것 같음