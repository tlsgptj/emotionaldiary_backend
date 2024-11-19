from openai import OpenAI
from advice_generation.config import OPEN_API_KEY
from advice_generation.models import Conversation
from wordCloud.models import wordCloud
# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPEN_API_KEY)

# OpenAI 시스템 명령어 설정
system_instructions = """You are a model designed to read diary entries and identify the context of the situation described within. You will select and suggest one or more of the following tags that best match the situation described: Friends, Family, Co-workers, School, Work, Home, Exercise. Your responses should only include the identified tags and nothing else, formatted as a list. If none of the tags apply, respond with '-'. Avoid any additional commentary or explanation."""

def get_emotion_analysis(conversation_id):
    """
    특정 Conversation의 user_input을 분석하여 장소를 추출하고 저장.
    """
    try:
        # Conversation 객체 가져오기
        conversation = Conversation.objects.get(id=conversation_id)

        # OpenAI API를 호출하여 감정 분석 수행
        completion = client.chat.completions.create(
            model="gpt-4.0-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_instructions,
                },
                {
                    "role": "user",
                    "content": conversation.user_input,  # Conversation의 user_input 값 사용
                },
            ],
        )

        # OpenAI의 응답에서 감정 결과 추출
        emotional = completion.choices[0].message.content.strip()

        # Analytics 모델에 결과 저장
        wordClouds = wordCloud.objects.create(
            user=conversation.user,       # Conversation의 user와 연결
            conversation=conversation,    # Conversation과 연결
            word=wordCloud.word     # 감정 분석 결과 저장
        ) # 고객이 쓴 글이 개많음 이중에서 단어를 추출해서 표기를 해야함 상위 30개 데이터베이스를 어떻게 구성해야할까

        return wordClouds

    except Conversation.DoesNotExist:
        return {"error": "Conversation not found."}

    except Exception as e:
        return {"error": str(e)}
