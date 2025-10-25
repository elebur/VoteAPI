from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from base.models import Employee, Menu, Vote
from api.serializers import DoVoteSerializer


@api_view(["GET"])
def get_vote_results(request: Request):
    today = timezone.now().date()
    today_menu = Menu.objects.filter(launch_date=today)
    result = list()
    for menu in today_menu:
        likes = menu.votes.filter(like=True).count()
        dislikes = menu.votes.filter(like=False).count()
        diff = likes - dislikes

        result.append({
            "menu_id": menu.id,
            "likes": likes,
            "dislikes": dislikes,
            "result": diff
        })
    return Response(result)


@csrf_exempt
@api_view(["POST"])
def do_vote(request: Request, menu_id: int):
    menu = get_object_or_404(Menu, pk=menu_id)

    serializer = DoVoteSerializer(data=request.data)

    if serializer.is_valid():
        emp = get_object_or_404(Employee, pk=serializer.data["employee_id"]) # type: ignore
        vote = Vote.objects.filter(menu=menu, employee=emp).first()
        # An employee can't vote multiple times
        if vote:
            status_code = status.HTTP_400_BAD_REQUEST
            action = "liked" if vote.like else "dislike"
            err_msg = (f"You've already {action} this menu '{menu.title}'.")
            result = {"details": err_msg}
        else:
            vote = Vote.objects.create(menu=menu, employee=emp, like=serializer.data["like"]) # type: ignore
            action = "liked" if vote.like else "disliked"
            status_code = status.HTTP_200_OK
            result = {"vote_id": vote.id, "action": action} # type: ignore
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
