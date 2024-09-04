import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogPostsAPIView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        limit = int(request.query_params.get('limit', 5))

        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',  # JSON 형식의 응답을 요청
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # JSON 응답 처리
            data = response.json()  # JSON 데이터를 파싱하여 Python 딕셔너리로 변환

            # 데이터 처리 예시 (limit 만큼 자르기)
            blog_posts = data[:limit]  # limit 만큼의 데이터만 가져오기

            return Response(blog_posts, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            return Response({"error": f"HTTP error occurred: {http_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.ConnectionError as conn_err:
            return Response({"error": f"Connection error occurred: {conn_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.Timeout as timeout_err:
            return Response({"error": f"Timeout error occurred: {timeout_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as req_err:
            return Response({"error": f"An error occurred: {req_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
