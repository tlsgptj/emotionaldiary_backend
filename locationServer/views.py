from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Locations

@login_required
def get_location_data(request):
    if request.method == 'GET':
        #장소 데이터 DB에서 가져옴
        user = request.user
        locations = Locations.objects.filter(user=user)
        locations.values('user_Locations')#상황 이름 선택
        locations.annotate(frequency=Count('user_Locations')) #필요하다면 빈도수
        locations.order_by('-frequency')[:4]

        situation_data = [
            {
                'user_Locations': Locations['user_Locations'],
                'frequency': Locations['frequency'],
            }
            for situation in situation_data
        ]

        return JsonResponse({'top_situations' : situation_data}, safe=False)
    
    return JsonResponse({"error" : "Invalid request method"}, status=405)


