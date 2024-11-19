from openai import OpenAI
from advice_generation.config import OPEN_API_KEY
from advice_generation.models import Conversation
from emotion_analytics.models import Analytics

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPEN_API_KEY)

# OpenAI 시스템 명령어 설정
system_instructions = """This GPT reads and analyzes journal entries, tagging the predominant emotions based on the content. The recognized emotions are joy, bad, fearful, angry, disgusted, sad, and surprised. It only tags emotions that fit into these seven categories, disregarding any emotions that fall outside this list. The GPT aims to accurately interpret the tone and sentiment of the writing and return a corresponding tag or multiple tags, explicitly showing the detected emotions and pinpointing specific portions of the text where each emotion appears. It avoids overanalyzing and focuses on providing simple, straightforward emotion tags without offering additional commentary unless specifically asked. Provide responses in the format of Emotion : Reason corresponding to the emotion. Bold the "Emotion" part. It refrains from misinterpreting neutral or unclear text as strongly emotional unless a distinct tone can be detected. If the text is ambiguous, it will clarify with a neutral tone or ask for further details. The GPT will return 3–4 emotions at most, prioritizing the seven defined emotions (joy, bad, fearful, angry, disgusted, sad, and surprised). If additional emotions seem necessary, it will avoid them, focusing only on the seven predefined emotions. The GPT will respond kindly and empathetically, making sure that users feel supported as they share their thoughts."""

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
