from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from cv.models import GameMap

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
            handle_uploaded_file(request.FILES['file'])
            map_title = request.POST['title']
            with open('test_output.txt', 'r') as f:
            	file_contents = f.read()
                new_game_map = GameMap.objects.create(title=map_title,map=file_contents)
                new_game_map.save()
            return HttpResponseRedirect("/game/" + map_title + "/")
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def game(request, name):
    game_obj = GameMap.objects.filter(title=name)
    if game_obj:
        game_obj = game_obj[0]
        high_score_string = game_obj.high_score
        if (game_obj.high_score == 9999): # defualt value
            high_score_string = "Level never beaten!"
        return render(request, 'play.html', {'map': game_obj.map, 'high_score': high_score_string, 'title': game_obj.title})
    else:
        return HttpResponse("<h1> Game Page Does Not Exist With Name: </h1>" + name)

def update_score(request, name):
    if request.method == 'POST':
        high_score = int(request.POST.get("score"))
        debug_string = "Trying to update score for game " + name + " with score: " + request.POST.get("score")
        game_obj = GameMap.objects.filter(title=name)[0]
        if (game_obj.high_score > high_score):
            game_obj.high_score = high_score
            game_obj.save()
        return HttpResponse(debug_string)
    else:
        return HttpResponse("Requires POST request to update scores")

def update_votes(request, name):
    if request.method == 'POST':
        game_obj = GameMap.objects.filter(title=name)[0]
        game_obj.votes = game_obj.votes + 1
        game_obj.save()
        return HttpResponse("Updated Votes")
    else:
        return HttpResponse("Requires POST request to update votes")

def discover(request):
    recent_maps = GameMap.objects.order_by('-created')[:15]
    return render(request, 'discover.html', {'recent_maps': recent_maps})



