import pygame

# from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.5
from pygame import time

screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

walking_left = False
walking_right = False
jumping_up = False
attack = False
level_move = False
city = pygame.image.load('city.jpg').convert_alpha()
city_transformed = pygame.transform.scale(city, (screen_width, screen_height))
city_rect = city_transformed.get_rect()
city_flipped = pygame.transform.flip(city_transformed, True, False)
level_map = [
    '                           ',
    '                           ',
    '                     C      ',
    ' XX   XXX            XX    ',
    ' XX             C           ',
    'XXXXX       P   XX       XXXXXXX XCCXXX   XXXXXX',
    'XXXXX       XX      CC    CCCCCCCCCCCCCCC                   CCCCCC',
    'XX     X   XXXX     XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
    '       X   XXXXX    XX  XXX                             ',
    '    XXXX   XXXXX    XX  XXX',
    'XXXXXXXX   XXXXX    XX  XXX']


class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        pygame.sprite.Sprite.__init__(self)
        global dirt_bg
        self.tiles = level_map
        self.dirt_bg = pygame.image.load("dirt_block.png").convert_alpha()
        self.dirt_bg = pygame.transform.scale(self.dirt_bg, (102, 102))
        self.rect = self.dirt_bg.get_rect()

        global coin
        coin = pygame.image.load ("1.jpg").convert_alpha()
        coin = pygame.transform.scale(coin, (52, 52))

    # coin = pygame.transform.scale(coin,(32,32))

    def tile_maker(self):
        rects_tile = []
        y_position = 0
        for row in level_map:
            x_position = 0
            for tile in row:
                if tile == 'X':
                    screen.blit(self.dirt_bg, (x_position * 102 + self.offsetX, y_position * 102 + self.offsetY))

                if tile != 'X':
                    rects_tile.append(pygame.Rect(x_position * 102, y_position * 102, 102, 102))
                if tile == 'C':
                    screen.blit(coin, (x_position * 102 + self.offsetX, y_position * 102 + self.offsetY))
                if tile != 'C':
                    rects_tile.append(pygame.Rect(x_position * 102, y_position * 102, 102, 102))



                x_position += 1
            y_position += 1
        return rects_tile



# player
class Player(pygame.sprite.Sprite):
    def __init__(self,p_or_e, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.movement_speed = 10
        self.action = 0
        self.index = 0
        self.jump = 0

        self.p_or_e = p_or_e
        self.flip_image = False
        self.axis = 1
        self.update_time = pygame.time.get_ticks()
        my_list = []

        for i in range(7):
            character = pygame.image.load(f"{p_or_e}{i}idle.png").convert_alpha()
            character = pygame.transform.scale(character, (100, 150))
            # character_rect = character.get_rect()
            my_list.append(character)

        self.animation_list.append(my_list)

        my_list = []
        for i in range(7):
            character = img = pygame.image.load(f'{p_or_e}{i}run.png').convert_alpha()
            character = pygame.transform.scale(img, (100, 150))
            my_list.append(character)

        self.animation_list.append(my_list)

        my_list = []
        for i in range(5):
            character = img = pygame.image.load(f'{p_or_e}attack{i}.png').convert_alpha()
            character = pygame.transform.scale(img, (100, 150))
            my_list.append(character)
        self.animation_list.append(my_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def movement(self, walking_left, walking_right):
        if walking_left == True:
            self.rect.x -= self.movement_speed
            self.flip_image = True
            self.axis = -1

        if walking_right == True:
            self.rect.x += self.movement_speed
            self.flip_image = False
            self.axis = 1
        if jumping_up == True:
            self.jump = -5
            self.rect.y += self.jump
            self.rect.y += self.jump - 15
        if level_move == True:
            city_rect.x += 8
            self.movement_speed = 0

        self.rect.y += GRAVITY

        if self.rect.bottom > 930:
            self.rect.bottom = 930
        # -jumping_up == False

        # self.jump
        # self.rect.y += self.jump

        self.rect.y -= self.jump

    def update_animation(self):

        cooldown_time_Animation = 100
        self.image = self.animation_list[self.action][self.index]

        if pygame.time.get_ticks() - self.update_time > cooldown_time_Animation:
            self.update_time = pygame.time.get_ticks()
            self.index += 1

        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def override_currentAction(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def camera_movement(self, tiles):
        move_speed = 10
        if self.rect.x > screen_width - 200 and walking_right == True:
            city_rect.x -= 10
            tiles.offsetX -= 10
            self.movement_speed = 0
            # screen.blit(city_flipped,(1700,0))
            # self.movement_speed = 0
        elif self.rect.x < 200 and walking_left == True:
            city_rect.x += 10
            tiles.offsetX += 10
            self.movement_speed = 0
        else:
            move_speed=0
            self.movement_speed = 10




        #if self.rect.colliderect(dirt_bg_rect):
         #   self.movement_speed = 0
    def collide_tests(self,tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self,movement,tiles,tile):
        types_collison = {"top": False, "bottom":False, "left":False,"right":False}
        #self.rect.x += movement[0]
        hit_list = self.collide_tests(tile)
        for tile in hit_list:
            if walking_right:
                self.rect.right = tile.left
                types_collison ["right"] = True
  



        return self.rect,types_collison






    def draw(self):
        # screen.blit(city_transformed,city_rect)
        screen.fill('light blue')
        screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)
        screen.blit(pygame.transform.flip(self.image, self.flip_image, False), self.rect)


# PLAYER CLASS CALL
p1 = Player('p',500, 500)
e1 = Player('e',500,500)

tile = Tiles()

# if p1.rect.colliderect(tile.rect):
#    p1.rect.y == tile.rect.y

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                walking_left = True
                flip_image = True
            if event.key == pygame.K_d:
                walking_right = True
            if event.key == pygame.K_w:
                jumping_up = True
            if event.key == pygame.K_e:
                attack = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                walking_left = False
            if event.key == pygame.K_d:
                walking_right = False
            if event.key == pygame.K_w:
                jumping_up = False
            if event.key == pygame.K_e:
                attack = False

    p1.draw() 
    p1.update_animation()
    p1.movement(walking_left, walking_right)
    p1.camera_movement(tile)
    #p1.collison(rects_tile)
   # p1.collide(tile)

    if walking_left or walking_right:
        p1.override_currentAction(1)
    elif attack == True:
        p1.override_currentAction(2)
    else:
        p1.override_currentAction(0)

    e1.draw()
    e1.update_animation()
    e1.movement(walking_left,walking_right)
    e1.camera_movement(tile)
   # e1.collide(tile)
  #  e1.collison(tile)

    if walking_left or walking_right:
        e1.override_currentAction(1)
    elif attack == True:
        e1.override_currentAction(2)
    else:
        e1.override_currentAction(0)

   

    # char=pygame.image.load("0enemy.png")
    #  char = pygame.transform.scale(char,(150,250))
    # screen.blit(char,(200,700))
    tile.tile_maker()

    pygame.display.update()
