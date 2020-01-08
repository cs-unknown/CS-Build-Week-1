from django.contrib.auth.models import User
from adventure.models import Player, Room
from util.sample_generator import World
import requests
import random
Room.objects.all().delete()
word_site = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(word_site)
WORDS = response.content.splitlines()

world = World()
world.generate_rooms(10, 10, 100)

roomTracker = {}

for row in world.grid:
    for rm in row:
        title = random.choice(WORDS).decode('utf-8').capitalize()
        room = Room(title=f' {title} Room', description=f'You have entered the {title} Room')
        room.save()
        roomTracker[(rm.x, rm.y)] = room
        if rm.e_to != None:
            coords = (rm.e_to.x, rm.e_to.y)
            if coords in roomTracker:
                roomTracker[rm.x, rm.y].connectRooms(roomTracker[coords], 'e')
                roomTracker[coords].connectRooms(roomTracker[rm.x, rm.y], 'w')
        if rm.w_to != None:
            coords = (rm.w_to.x, rm.w_to.y)
            if coords in roomTracker:
                roomTracker[rm.x, rm.y].connectRooms(roomTracker[coords], 'w')
                roomTracker[coords].connectRooms(roomTracker[rm.x, rm.y], 'e')
        if rm.s_to != None:
            coords = (rm.s_to.x, rm.s_to.y)
            if coords in roomTracker:
                roomTracker[rm.x, rm.y].connectRooms(roomTracker[coords], 's')
                roomTracker[coords].connectRooms(roomTracker[rm.x, rm.y], 'n')
world.print_rooms()

players = Player.objects.all()
for p in players:
    p.currentRoom = world.grid[0][0].id
    p.save()
