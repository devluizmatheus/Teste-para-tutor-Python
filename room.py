import pygame
import random
from pgzero.builtins import images
from pgzero.actor import Actor

ORIGINAL_TILE_SIZE = 16
SCALE = 2 
TILE_SIZE = ORIGINAL_TILE_SIZE * SCALE 

class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[f"floor_{random.randint(1, 3)}" for x in range(width)] for y in range(height)]
        self.apply_walls()

        off_x = (780 - (self.width * TILE_SIZE)) // 2
        off_y = (600 - (self.height * TILE_SIZE)) // 2

        self.spawners = [
            (off_x + TILE_SIZE * 2, off_y + TILE_SIZE * 2),       
            (off_x + TILE_SIZE * (width - 3), off_y + TILE_SIZE * 2),
            (off_x + TILE_SIZE * 2, off_y + TILE_SIZE * (height - 3)), 
            (off_x + TILE_SIZE * (width - 3), off_y + TILE_SIZE * (height - 3))
        ]

    def apply_walls(self):
        last_x = self.width - 1
        last_y = self.height - 1

        for y in range(self.height):
            for x in range(self.width):
     
                if y == 0 and (x == 0 or x == last_x):
                    self.map[y][x] = "wall_corner_up"
                elif y == last_y and (x == 0 or x == last_x):
                    self.map[y][x] = "wall_corner_down"
                elif x == 0 or x == last_x:
                    self.map[y][x] = "wall_top"
                elif y == 0 or y == last_y:
                    self.map[y][x] = "wall_front"

    def draw(self, screen):
        offset_x = (780 - (self.width * TILE_SIZE)) // 2
        offset_y = (600 - (self.height * TILE_SIZE)) // 2

        for y in range(self.height):
            for x in range(self.width):
                pos = (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                tile_id = self.map[y][x]
                
                try:
                    img = getattr(images, tile_id)
                    img_rescale = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                    screen.blit(img_rescale, pos)
                except AttributeError:
                    screen.draw.filled_rect(pygame.Rect(pos, (TILE_SIZE, TILE_SIZE)), (50, 50, 50))

class Portal(Actor):
    def __init__(self, pos):
        super().__init__('portal', pos) 
        self.timer = 0

class Enemy(Actor):
    def __init__(self, pos):
        super().__init__('goblin_idle0', pos)
        self.hp = 2
        self.speed = random.uniform(0.5, 0.8)
        
        # Controle de Animação
        self.state = "idle"
        self.frame = 0
        self.anim_timer = 0
        self.look_dir = "left"

    def update(self, player_pos):
        if self.state == "death" or self.state == "hurt":
            self.update_animation()
            return
        
        moved = False
        if self.x < player_pos[0]: 
            self.x += self.speed
            self.look_dir = "right"
            moved = True
        elif self.x > player_pos[0]: 
            self.x -= self.speed
            self.look_dir = "left"
            moved = True
            
        if self.y < player_pos[1]: 
            self.y += self.speed
            moved = True
        elif self.y > player_pos[1]: 
            self.y -= self.speed
            moved = True

        if moved:
            self.state = "walk"
        else:
            self.state = "idle"
            
        self.update_animation()

    def update_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.frame += 1
            
            max_frames = {"idle": 4, "walk": 6, "attack": 4, "death": 5, "hurt": 2}
            
            if self.frame >= max_frames.get(self.state, 4):
                if self.state == "death":
                    self.frame = max_frames["death"] - 1
                elif self.state == "hurt" or self.state == "attack":
                    self.state = "idle"
                    self.frame = 0
                else:
                    self.frame = 0
            
            self.image = f"goblin_{self.state}{self.frame}"