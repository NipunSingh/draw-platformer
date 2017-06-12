from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from cv.models import GameMap
import sys

def handle_uploaded_file(f):
    with open('input.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    import os
    os.system("python ../scan.py --image input.jpg > test_output.txt")
    os.system("chmod 777 test_output.txt")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_img = request.FILES['file']
            handle_uploaded_file(input_img)
            map_title = request.POST['title']
            with open('test_output.txt', 'r') as f:
                file_contents = f.read()
                new_game_map = GameMap.objects.create(title=map_title,map=file_contents,input_img=input_img)
                new_game_map.save()
            return HttpResponseRedirect("/play/" + map_title)
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def game(request, map_name):
    game_obj = GameMap.objects.filter(title=map_name)
    if game_obj:
        game_obj = game_obj[0]
        high_score_string = game_obj.high_score
        if (game_obj.high_score == 9999): # defualt value
            high_score_string = "Level never beaten!"
        return render(request, 'play.html', {'map': game_obj, 'high_score': high_score_string})
    else:
        return HttpResponse("<h1> Game Page Does Not Exist With Name: </h1>" + map_name)

def update_score(request, map_name):
    if request.method == 'POST':
        high_score = int(request.POST.get("score"))
        username = request.POST.get("username")
        game_obj = GameMap.objects.filter(title=map_name)[0]
        print >> sys.stderr, (high_score, username)
        if (game_obj.high_score > high_score):
            game_obj.high_score = high_score
            if username == "":
                username = "Anonymous"
            game_obj.high_score_name = username
            game_obj.save()
        return HttpResponse(debug_string)
    else:
        return HttpResponse("Requires POST request to update scores")

def vote(request):
    for key, value in request.POST.items():
        print >>sys.stderr, (key, value)

    if request.method == 'POST':
        map_id = request.POST.get("id")
        is_upvote = request.POST.get("up")
        is_downvote = request.POST.get("down")
        prev = request.POST.get("prev") #previously clicked button {none,downvoted,upvoted}

        game_obj = GameMap.objects.filter(id=map_id)[0]
        if prev == "none":
            if is_upvote == "true":
                game_obj.votes = game_obj.votes + 1
            else:
                game_obj.votes = game_obj.votes - 1
        elif prev == "downvoted":
            if is_upvote == "true":
                game_obj.votes = game_obj.votes + 2
            else:
                game_obj.votes = game_obj.votes + 1
        elif prev == "upvoted":
            if is_downvote == "true":
                game_obj.votes = game_obj.votes - 2
            else:
                game_obj.votes = game_obj.votes - 1
        else:
            print >> sys.stderr, "Logical Error, prev not matched to any of the cases"

        game_obj.save()
        return HttpResponse("Updated Votes")

    else:
        return HttpResponse("Requires POST request to update votes")

def discover_home(request):
    return discover(request, 1)

def discover(request, page):
    page = int(page)
    start_index = page*10-10
    end_index = page*10
    next_page = page + 1
    recent_maps = GameMap.objects.order_by('-created')[start_index:end_index]
    return render(request, 'discover.html', {'recent_maps': recent_maps, 'next_page': next_page})

