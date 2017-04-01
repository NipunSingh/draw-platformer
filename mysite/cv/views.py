from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from cv.models import GameMap

def index(request):
    return HttpResponse("Hello, world. You're at the CV index.")

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
	    	#return render(request, 'game.html', {'map': file_contents})
            return HttpResponseRedirect("/cv/game/" + map_title)
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def game(request, name):
    game_obj = GameMap.objects.filter(title=name)
    if game_obj:
        game_obj = game_obj[0]
        return render(request, 'play.html', {'map': game_obj.map, 'high_score': game_obj.high_score, 'title': game_obj.title})
    else:
        return HttpResponse("<h1> Game Page Does Not Exist With Name: </h1>" + name)



