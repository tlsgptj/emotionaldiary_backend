import re
from collections import Counter
from models import wordCloud
from advice_generation.models import Conversation

def calculate_word_frequency(user_id):
    # DB에 있는 사용자 글 가져오기
    entries = Conversation.objects.filter(user_id=user_id)
    all_text = " ".join(entry.entry_text for entry in entries).lower()

    #정규식을 사용하여 단어 추출
    words = re.findall(r'\b\w+\b', all_text)

    #빈도 계산
    word_counts = Counter(words)
    return word_counts.most_common(30) #상위 30개의 단어만 추출함