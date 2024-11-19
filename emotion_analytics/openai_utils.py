from openai import OpenAI
from advice_generation.config import OPEN_API_KEY
from advice_generation.models import Conversation
from emotion_analytics.models import Analytics

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPEN_API_KEY)

# OpenAI 시스템 명령어 설정
system_instructions = """너는 글을 읽고 감정을 맞추는 일을 하며, 너가 맞춰야 할 감정은 총 6가지이다. 기쁨, 슬픔, 걱정, 분노, 공포, 우울, 부끄러움"""

def get_emotion_analysis(conversation_id):
    """
    특정 Conversation의 user_input을 분석하여 감정을 추출하고 저장.
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
        analytics = Analytics.objects.create(
            user=conversation.user,       # Conversation의 user와 연결
            conversation=conversation,    # Conversation과 연결
            emotional=emotional           # 감정 분석 결과 저장
        )

        return analytics

    except Conversation.DoesNotExist:
        return {"error": "Conversation not found."}

    except Exception as e:
        return {"error": str(e)}
