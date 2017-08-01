# DrawPlatformer
## Draw Your Own Platformer Style Video Game. 
The original version of this project was made at HackUVA, the University of Virginia's 24-hour hackathon, where it won the Grand Prize and was recognized as the best hack of the weekend. You can view a demo of the project and learn more about what inspired us to build this [by clicking here](www.nipunsingh.com). 
## Interesting Files
* [scan.py](https://github.com/NipunSingh/draw-platformer/blob/master/scan.py) -  Runs the image processing pipeline. Isolates your paper with the drawn game from the image background, looks for different colors in the image, and then outputs a file which contains the map data to be used by the Javascript game engine. 
* [play.html](https://github.com/NipunSingh/draw-platformer/blob/master/mysite/cv/templates/play.html) - Frontend code for the page that actually runs the Javascript game. 
* [views.py](https://github.com/NipunSingh/draw-platformer/blob/master/mysite/cv/views.py) - Backend code to handle file uploading, game highscores, & voting on maps. 
## Installation Instructions
Make sure you have Python 2.X installed on your computer. Then clone/download this project to your computer
```
$ git clone https://github.com/NipunSingh/draw-platformer.git
```
Then install all the dependencies (Django, Numpy, OpenCV, etc.) via pip:
```
$ pip install -r requirements.txt 
```
Change directory to 'mysite' and then run this command from the command prompt:
```
$ python manage.py runserver
```
Then open up your favorite browser and check the URL: http://127.0.0.1:8000

To view a demo of just the image processing pipeline on a singular image, run on the command line:
```
$ python scan.py --image images/face2.jpg
```
