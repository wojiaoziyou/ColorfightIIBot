from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS, BUILDING_COST

def play_game(game, room, username, password, join_key):
    # Connect to the server
    game.connect(room = room)
    
    # game.register should return True if succeed.
    if game.register(
            username = username, \
            password = password, \
            join_key = join_key ):

        # ========================= This is the game loop ===============================
        while True:
            if not game.update_turn():
                break

            if game.me == None:
                continue
    
            me = game.me

        # ================================== policy begins ============================
            cmd_list = []
            building = ''

            cell_list=list(me.cells.values())
            random.shuffle(cell_list)
            for cell in cell_list:
                # build all
                if cell.owner == me.uid \
                        and cell.building.is_empty \
                        and me.gold >= BUILDING_COST[0]:
                    for pos in cell.position.get_surrounding_cardinals():
                        c = game.game_map[pos]
                        if c.owner != 0:
                            building = BLD_FORTRESS
                    if building == '':
                        if cell.energy > cell.gold:
                            building = BLD_ENERGY_WELL
                        else:
                            building = BLD_GOLD_MINE

                    if building != '':
                        cmd_list.append(game.build(cell.position, building))
                        print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                        me.gold -= BUILDING_COST[0]


                # upgrade all
                if cell.building.can_upgrade \
                        and (cell.building.is_home or cell.building.level < me.tech_level) \
                        and cell.building.upgrade_gold < me.gold \
                        and cell.building.upgrade_energy < me.energy :
                    cmd_list.append(game.upgrade(cell.position))
                    print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                    me.gold   -= cell.building.upgrade_gold
                    me.energy -= cell.building.upgrade_energy

                # attack
                attack_list = []
                for pos in cell.position.get_surrounding_cardinals():
                    c = game.game_map[pos]
                    if c.attack_cost < me.energy and c.owner != me.uid \
                            and c.position not in attack_list \
                            and len(cell_list) < 225:
                        cmd_list.append(game.attack(pos, c.attack_cost))
                        print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, c.attack_cost))
                        me.energy -= c.attack_cost
                        attack_list.append(c.position)
            
            game.send_cmd(cmd_list)
        # ==================================== policy ends ============================

if __name__ == '__main__':
    # Create a Colorfight Instance. This will be the object that you interact with.
    game = Colorfight()

    # ==================== Enter a room ====================================
    room = 'public'; join_key = ''
    # room = 'Hell'; join_key = 'Crowley'
    username = 'DEMON'
    password = 'ineffablehusbands'

    # ==========================  Play game once ===========================
    play_game(
        game     = game, \
        room     = room, \
        username = username, \
        password = password, \
        join_key = join_key )
    # ======================================================================

