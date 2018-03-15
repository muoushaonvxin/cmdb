from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from users.models import UserProfile
import json
import queue
import time


GLOBAL_MSG_QUEUE = {

}


class DashBoard(View):
    def get(self, request):
        return render(self.request, "webchat/index.html")


class GetUserFriend(View):
    def post(self, request):
        for key in request.POST:
            current_user = json.loads(key).get('email')

        my_friend = {
            "friend": {}
        }

        user = UserProfile.objects.get(email=current_user)
        for friend in user.friends.select_related():
            my_friend['friend'][friend.id] = friend.username
        print(my_friend)
        return HttpResponse(json.dumps(my_friend), content_type="application/json")


class MsgHandler(View):
    def post(self, request):
        print(request.user.username)
        print(request.user.id)

        for key in request.POST:
            msg_data = json.loads(key)
            if msg_data:
                msg_data['timestamp'] = time.time()
                if msg_data['type'] == 'single':
                    if not GLOBAL_MSG_QUEUE.get(int(msg_data['to'])):
                        GLOBAL_MSG_QUEUE[int(msg_data['to'])] = queue.Queue()
                    GLOBAL_MSG_QUEUE[int(msg_data['to'])].put(msg_data)
        print(GLOBAL_MSG_QUEUE)
        return HttpResponse()


class GetNewMsgs(View):
    def get(self, request):
        if request.user.id not in GLOBAL_MSG_QUEUE:
            print("no queue for user [%s] " % request.user.username)
            GLOBAL_MSG_QUEUE[request.user.id] = queue.Queue()
        msg_count = GLOBAL_MSG_QUEUE[request.user.id].qsize()
        queue_obj = GLOBAL_MSG_QUEUE[request.user.id]
        msg_list = []
        if msg_count > 0:
            for msg in range(msg_count):
                msg_list.append(queue_obj.get())
            print("new msg: ", msg_list)
        else:
            try:
                msg_list.append(queue_obj.get(timeout=60))
            except queue.Empty:
                print("\033[41;1mno msg for [%s][%s], timeout\033[0m" % (request.user.id, request.user.username))
        return HttpResponse(json.dumps(msg_list), content_type="application/json")