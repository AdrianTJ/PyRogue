import tcod as libtcod
import pygame

# Importing Files

import constants


########################################################################################################################
##############################################    STRUCTS    ###########################################################
########################################################################################################################

class struct_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


########################################################################################################################
#############################################    OBJECTS    ############################################################
########################################################################################################################

class obj_actor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x = x  # map adress
        self.y = y  # map adress
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:
            SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))




########################################################################################################################
###########################################    COMPONENTS    ###########################################################
########################################################################################################################

class com_Creature:
    '''Creatures have health, and can damage other objects by attacking them. They can also die.'''

    def __init__(self, name_instance, hp=10, death_function = None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target, 3)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + ' damage!')
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print(self.name_instance + "s health is " + str(self.hp) + "/" + str(self.maxhp))

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

# TODO class com_Item:

# TODO class com_Container:

########################################################################################################################
######################################    ARTIFICIAL INTELLIGENCE     ##################################################
########################################################################################################################

class ai_Test:
    '''Once per turn, execute.'''

    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

def death_monster(monster):
    '''On death, most monsters stop moving.'''
    print(monster.creature.name_instance + " is dead!")
    monster.creature = None
    monster.ai = None

########################################################################################################################
##################################################    MAP     ##########################################################
########################################################################################################################

def map_create():
    new_map = [[struct_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    for y in range(constants.MAP_WIDTH):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

    map_make_fov(new_map)

    return new_map

def map_check_for_creature(x, y, exclude_object = None):

    target = None

    if exclude_object:
        # Check object list to find creature at location that isnt excluded
        for obj in GAME_OBJECTS:
            if (obj is not exclude_object and
                    obj.x == x and
                    obj.y == y and
                    obj.creature):
                target = obj

            if target:
                return target
    else:
        # Check object list to find any creature, including self
        for obj in GAME_OBJECTS:
            if (obj.x == x and
                obj.y == y and
                obj.creature):
                    target = obj

            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y,
            not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y,
        constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)

########################################################################################################################
##############################################    DRAWING    ###########################################################
########################################################################################################################

def draw_game():
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # TODO clear the surface

    # TODO draw the map
    draw_map(GAME_MAP)

    # Drawing all objects
    for obj in GAME_OBJECTS:
        obj.draw()

    # update the display
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    # draw a wall
                    SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # draw a floor
                    SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored == True:
                    if map_to_draw[x][y].block_path == True:
                        # draw a wall
                        SURFACE_MAIN.blit(constants.S_WALL_EX, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                    else:
                        # draw a floor
                        SURFACE_MAIN.blit(constants.S_FLOOR_EX, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


########################################################################################################################
##################################################    GAME     #########################################################
########################################################################################################################

def game_main_loop():
    '''in this function we loop the main game'''
    game_quit = False

    while not game_quit:

        # Handle Player Input
        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True
        elif player_action != "no action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

    # TODO quit the game
    pygame.quit()
    exit()

def game_initialize():
    '''This function initializes the main window and pygame'''
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALCULATE

    # initialize pygame
    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    GAME_MAP = map_create()

    FOV_CALCULATE = True

    # Initializations
    creature_com1 = com_Creature("greg")
    PLAYER = obj_actor(1, 1, "snake", constants.S_PLAYER, creature=creature_com1)

    creature_com2 = com_Creature("jackie", death_function = death_monster)
    ai_com = ai_Test()
    ENEMY = obj_actor(15, 15, "crab", constants.S_ENEMY, creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [ENEMY, PLAYER]

def game_handle_keys():

    global FOV_CALCULATE
    # get player input
    events_list = pygame.event.get()

    # TODO process player input
    for event in events_list:
        # Close the game when pressing x
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player moved"
    return "no action"

########################################################################################################################
##############################################    EXECUTE GAME     #####################################################
########################################################################################################################

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
