def move(self, dx, dy):
    tile_is_wall = (GAME_MAP[self.x + dx][self.y + dy].block_path == True)

    target = None

    for obj in GAME_OBJECTS:
        if (obj is not self and
                obj.x == self.x + dx and
                obj.y == self.y + dy and
                obj.creature):
            target = obj
            break

    if target:
        print(self.creature.name_instance + " attacks " + target.creature.name_instance + " for 5 damage!")
        target.creature.take_damage(5)

    if not tile_is_wall and target is None:
        self.x += dx
        self.y += dy