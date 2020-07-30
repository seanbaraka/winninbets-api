from json import loads
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Tip
import json

# Create your views here.

# function to get tips. TODO: VIP users should be able to access all tips, both free and paid, non-VIP members should only access free tips
@api_view(['GET'])
@permission_classes([AllowAny])
def get_tips(request):
    user_accessing_tips = request.user
    if user_accessing_tips.is_staff:
        tips_queryset = Tip.objects.all()
        return HttpResponse(serialize('json',tips_queryset), content_type='application/json')

    if request.auth is not None and user_accessing_tips.member.is_vip:
        tips_queryset = Tip.objects.all()
    else:
       tips_queryset = Tip.objects.filter(is_vip_tip=False)

    tips_json = serialize('json', tips_queryset)
   

    return HttpResponse(tips_json, content_type='application/json')

@api_view(['GET'])
@permission_classes([AllowAny])
def recent_tips(request):
    user = request.user
    if request.auth is not None and user.member.is_vip:
        tips_queryset = Tip.objects.filter(status=None)
    else:
       tips_queryset = Tip.objects.filter(is_vip_tip=False, status=None)

    tips_json = serialize('json', tips_queryset)
   

    return HttpResponse(tips_json, content_type='application/json')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_tip(request):
    # serialize the request.body object to a python list/dict
    tip_request = json.loads(request.body)
    
    # attempt to add a tip to the database
    tip_to_add = Tip.objects.create(
        home_team = tip_request['home'],
        away_team = tip_request['away'],
        match_date = tip_request['date'],
        prediction = tip_request['prediction'],
        prediction_odds = tip_request['prediction_odds'],
        home_odds = tip_request['home_odds'],
        away_odds = tip_request['draw_odds'],
        draw_odds = tip_request['away_odds'],
        is_vip_tip = tip_request['isVip'],
        is_featured = tip_request['isFeatured']
    )

    # if successfully added a tip
    if tip_to_add is not None:
        success_message = {
            "success": "Operation completed successfully"
        }
        return JsonResponse(success_message, safe=False)

@api_view(['PUT'])
def end_fixture(request):
    fixture_request = json.loads(request.body)
    fixture_to_edit = Tip.objects.get(id=fixture_request['id']) # get the Tip associated with the id passed in the request body

    fixture_to_edit.score = fixture_request['score']
    fixture_to_edit.status = fixture_request['status']

    fixture_to_edit.save()

    print(fixture_to_edit)

    success_message = {
            "success": "Operation completed successfully"
        }
    return JsonResponse(success_message, safe=False)

# TODO: Create delete TODO: DO not forget


@api_view(['GET'])
@permission_classes([AllowAny])
def totalOdds(request):
    user = request.user
    total_odds = 1
    if request.auth is not None and user.member.is_vip:
        tips_queryset = Tip.objects.filter(status=None)
        for tip in tips_queryset:
            total_odds = total_odds * tip.prediction_odds
    
        return HttpResponse(total_odds.__round__(2), content_type='application/json')

    else:
        tips_queryset = Tip.objects.filter(is_vip_tip=False, status=None)
        for tip in tips_queryset:
            total_odds = total_odds * tip.prediction_odds
    
        return HttpResponse(total_odds.__round__(2), content_type='application/json')

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_match(request):
    user = request.user
    odds = []
    if request.auth is not None and user.member.is_vip:
        recent_matches = Tip.objects.filter(status=None)
        for match in recent_matches:
            odds.append(match.prediction_odds)
            
        most_odds = max(odds)

        featured_match = Tip.objects.filter(is_featured=True).first()

        return HttpResponse(serialize('json', featured_match), content_type='application/json')

    else:
        recent_matches = Tip.objects.filter(status=None)
        for match in recent_matches:
            odds.append(match.prediction_odds)
        
        most_odds = max(odds)
        featured_match = Tip.objects.filter(prediction_odds=most_odds)
        
        return HttpResponse(serialize('json',featured_match), content_type='application/json')

    
@api_view(['DELETE'])
def delete_prediction(request, id):
    match_id = id
    selected_match = Tip.objects.get(pk=match_id)

    if(selected_match is not None):
        selected_match.delete()
        delete_message = {
            "message": "Successfully deleted"
        }
        return JsonResponse(delete_message, safe=False)

    error_delete = {
        "error": "Failed to delete the item"
    }
    return JsonResponse(error_delete, safe=False)
