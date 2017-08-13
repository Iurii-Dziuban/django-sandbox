import json
import threading

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import F

from application.app_constants import EVENT_CATEGORIES
from application.models import LikedEvent, User, Journey, Category, UserRank
from .models import Question, EventRequest, Event, LikeRequest


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'application/index.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def create_question_view(request, arg):
    return render(request, 'application/createq.html')


def create_question_create(request, arg):
    questionJSON = json.loads(request.body)

    question = Question()
    question.question_text = str(questionJSON.get("Text"))
    question.pub_date = timezone.now()

    question.save()

    return HttpResponse("Question is created")


def create_question_create(request, arg):
    questionJSON = json.loads(request.body)

    question = Question()
    question.question_text = str(questionJSON.get("Text"))
    question.pub_date = timezone.now()

    question.save()

    return HttpResponse("Question is created")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'application/detail.html', {'question': question})


def get_events(request, arg):
    if request.method == 'POST':
        return "POST is Ok"
    return HttpResponse("Get Event request is not supported")


def save_request_info(event_request):
    save_user(event_request.username)
    save_journey(event_request)
    for category_id in event_request.categories:
        save_category(event_request, category_id)


def save_journey(event_request):
    journey = Journey()
    journey.username = User.objects.get(pk=event_request.username)
    journey.longitude = event_request.longitude
    journey.latitude = event_request.latitude
    journey.fromDate = event_request.fromDate
    journey.toDate = event_request.toDate
    journey.save()


def save_category(event_request, category_id):
    category = Category()
    category.id = event_request.username + str(category_id)
    category.category_id = category_id
    category.username = User.objects.get(pk=event_request.username)

    category.save()


def save_user(username):
    user = User()
    user.username = username

    user.save()


def likeDeprecated(request, service_id, event_id):
    if request.method == 'POST':
        return HttpResponse('serviceId {0} , id {1}'.format(service_id, event_id))
    return HttpResponse("Get Event request is not supported")


def like(request, args):
    if request.method == 'POST':
        return HttpResponse('Post like successful')
    if request.method == 'DELETE':
        likeRequestJSON = json.loads(request.body)
        likeRequest = LikeRequest()
        likeRequest.username = likeRequestJSON.get("username")
        likeRequest.event_id = likeRequestJSON.get("event_id")
        likeRequest.service_id = likeRequestJSON.get("service_id")
        liked_event = LikedEvent()
        liked_event.id = likeRequest.event_id + likeRequest.username
        liked_event.delete()
        return HttpResponse('Dislike successful')
    return HttpResponse("Get Event request is not supported")


def user_likes(request, username):
    likes = LikedEvent.objects.filter(username__exact=F('username'))
    json_resp = json.dumps(list(like for like in likes), default=lambda o: o.__dict__)

    return HttpResponse(json_resp)


def recommendCompanions(request, username):
    if request.method == 'GET':

        recs = [["User1", 1], ["User2", 2]]

        user_ranks_array = []

        for rec_pair in recs:
            user_rank = UserRank()
            user_rank.username = rec_pair[0]
            user_rank.rank = rec_pair[1]

            user_ranks_array.append(user_rank)

        sorted_array = sorted(user_ranks_array, key=lambda user_rank: user_rank.rank, reverse=True)
        json_resp = json.dumps(sorted_array, default=lambda o: o.__dict__)
        return HttpResponse(json_resp)
    return HttpResponse("Only Get Companions is supported")
