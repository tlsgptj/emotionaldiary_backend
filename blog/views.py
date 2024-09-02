import requests
from bs4 import BeautifulSoup
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # 데이터 확인 (디버깅을 위해 추가)
            print(response.content)

            # XML 파싱 시도
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=limit)

            # 파싱된 데이터를 담을 리스트
            blog_posts = []
            for item in items:
                post = {
                    "title": item.title.text if item.title else "No Title",
                    "link": item.link.text if item.link else "No Link",
                    "published": item.pubDate.text if item.pubDate else "No Date",
                    "description": item.description.text if item.description else "No Description",
                }
                blog_posts.append(post)

            # 응답 데이터 반환
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
