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
        if rm.n_to != None:
            coords = (rm.n_to.x, rm.n_to.y)
            if coords in roomTracker:
                roomTracker[rm.x, rm.y].connectRooms(roomTracker[coords], 'n')
                roomTracker[coords].connectRooms(roomTracker[rm.x, rm.y], 's')
        if rm.s_to != None:
            coords = (rm.s_to.x, rm.s_to.y)
            if coords in roomTracker:
                roomTracker[rm.x, rm.y].connectRooms(roomTracker[coords], 's')
                roomTracker[coords].connectRooms(roomTracker[rm.x, rm.y], 'n')
world.print_rooms()

# r_outside = Room(title="Outside Cave Entrance",
#                  description="North of you, the cave mount beckons")

# r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
# passages run north and east.""")

# r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
# into the darkness. Ahead to the north, a light flickers in
# the distance, but there is no way across the chasm.""")

# r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
# to north. The smell of gold permeates the air.""")

# r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
# chamber! Sadly, it has already been completely emptied by
# earlier adventurers. The only exit is to the south.""")

# r_outside.save()
# r_foyer.save()
# r_overlook.save()
# r_narrow.save()
# r_treasure.save()

# # Link rooms together
# r_outside.connectRooms(r_foyer, "n")
# r_foyer.connectRooms(r_outside, "s")

# r_foyer.connectRooms(r_overlook, "n")
# r_overlook.connectRooms(r_foyer, "s")

# r_foyer.connectRooms(r_narrow, "e")
# r_narrow.connectRooms(r_foyer, "w")

# r_narrow.connectRooms(r_treasure, "n")
# r_treasure.connectRooms(r_narrow, "s")

players = Player.objects.all()
for p in players:
    p.currentRoom = world.grid[0][0].id
    p.save()
