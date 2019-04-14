from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL

# Create a Colorfight Instance. This will be the object that you interact
# with.
game = Colorfight()

# Connect to the server. This will connect to the public room. If you want to
# join other rooms, you need to change the url to the room.
game.connect(url = 'https://colorfightii.herokuapp.com/gameroom/public')

# game.register should return True if succeed.
# As no duplicate usernames are allowed, a random integer string is appended
# to the example username. You don't need to do this, change the username
# to your ID.
# You need to set a password. For the example AI, the current time is used
# as the password. You should change it to something that will not change 
# between runs so you can continue the game if disconnected.
if game.register(username = 'ExampleAI' + str(random.randint(1, 100)), \
        password = str(int(time.time()))):
    # This is the game loop
    while True:
        # The command list we will send to the server
        cmd_list = []
        # The list of cells that we want to attack
        my_attack_list = []
        # update_turn() is required to get the latest information from the
        # server. This will halt the program until it receives the updated
        # information. 
        # After update_turn(), game object will be updated.   
        game.update_turn()

        # Check if you exist in the game. If not, wait for the next round.
        # You may not appear immediately after you join. But you should be 
        # in the game after one round.
        if game.me == None:
            continue

        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.
        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Get the MapCell object of that position
                c = game.game_map[pos]
                # Attack if the cost is less than what I have, and the owner
                # is not mine, and I have not attacked it in this round already
                if c.attack_cost < game.me.energy and c.owner != game.uid \
                        and c.position not in my_attack_list:
                    print(c.position, c.owner, game.uid)
                    print(c.attack_cost)
                    # Add the attack command in the command list
                    # Subtract the attack cost manually so I can keep track
                    # of the energy I have.
                    # Add the position to the attack list so I won't attack
                    # the same cell
                    cmd_list.append(game.attack(pos, c.attack_cost))
                    game.me.energy -= c.attack_cost
                    my_attack_list.append(c.position)
        
        # Send the command list to the server
        game.send_cmd(cmd_list)
