from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .frequency import calculate_word_frequency
from wordCloud import WordCloud
import matplotlib.pyplot as plt
import io

class GenerateWordCloudAPIView(APIView):
    def get(self, request, user_id):
        #사용자 단어 빈도 계산
        word_frequencies = calculate_word_frequency(user_id)
        word_dict = dict(word_frequencies)

        #워드클라우드 생성
        wc = WordCloud(width=800, height=400, background_color="black").generate_from_frequencies(word_dict)

        #이미지를 메모리에 저장
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
