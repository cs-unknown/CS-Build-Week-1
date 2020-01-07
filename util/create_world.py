from django.contrib.auth.models import User
from adventure.models import Player, Room
from util.sample_generator import World
Room.objects.all().delete()
world = World()
world.generate_rooms(10, 10, 100)

roomTracker = {}

for row in world.grid:
    for rm in row:
        room = Room(title=f'{rm.name} {rm.id}', description=rm.name)
        room.save()
        roomTracker[(rm.x, rm.y)] = room
        if rm.x <= 9 and rm.x > 0:
          roomTracker[(rm.x, rm.y)].connectRooms(roomTracker[rm.x - 1, rm.y], "w") 
          roomTracker[(rm.x - 1, rm.y)].connectRooms(roomTracker[rm.x, rm.y], "e")
        if rm.y % 2 != 0:   
          if rm.x == 9 and rm.y > 0 and rm.y <= 9:
            roomTracker[(rm.x, rm.y)].connectRooms(roomTracker[rm.x, rm.y - 1], "s")
            roomTracker[(rm.x, rm.y - 1)].connectRooms(roomTracker[rm.x, rm.y], "n")
        if rm.y > 0 and rm.y % 2 == 0:
          if rm.x == 0:
            roomTracker[(rm.x, rm.y)].connectRooms(roomTracker[rm.x, rm.y - 1], "s")
            roomTracker[(rm.x, rm.y - 1)].connectRooms(roomTracker[rm.x, rm.y], "n")
world.print_rooms()
players = Player.objects.all()
for p in players:
    p.currentRoom = world.grid[0][0].id
    p.save()