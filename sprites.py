from config import *
import math
import pygame


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, island, x, y):

        self.camera_follow = 0
        self.camera_follow_y = 0
        self.island = island
        self._layer = PLAYER_LAYER
        self.groups = self.island.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.island.character_spritesheet.get_sprite(3, 2, 56, 56)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_Enemy()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def collide_Enemy(self):

        hits = pygame.sprite.spritecollide(self, self.island.enemy, False)
        if hits:
            self.island.playing = False

    def collide_blocks(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.island.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                self.camera_follow = 1

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.island.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                self.camera_follow_y = 1

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.camera_follow == 0:
                for sprite in self.island.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'

            else:
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
                self.camera_follow = 0

        if keys[pygame.K_RIGHT]:
            if self.camera_follow == 0:
                for sprite in self.island.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                self.x_change += PLAYER_SPEED
                self.facing = 'right'

            else:
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
                self.camera_follow = 0

        if keys[pygame.K_UP]:
            if self.camera_follow_y == 0:
                for sprite in self.island.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
            else:
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
                self.camera_follow_y = 0

        if keys[pygame.K_DOWN]:
            if self.camera_follow_y == 0:
                for sprite in self.island.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
            else:
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
                self.camera_follow_y = 0

    def animate(self):

        down_animations = [self.island.character_spritesheet.get_sprite(0, 0, 32, 55),
                           self.island.character_spritesheet.get_sprite(0, 61, 31, 39),
                           self.island.character_spritesheet.get_sprite(33, 61, 31, 40),
                           self.island.character_spritesheet.get_sprite(62, 56, 29, 44),
                           self.island.character_spritesheet.get_sprite(97, 56, 29, 44),
                           self.island.character_spritesheet.get_sprite(131, 62, 29, 38),
                           self.island.character_spritesheet.get_sprite(166, 61, 29, 39),
                           self.island.character_spritesheet.get_sprite(169, 56, 29, 43),
                           self.island.character_spritesheet.get_sprite(232, 57, 29, 43)
                           ]

        up_animations = [self.island.character_spritesheet.get_sprite(0, 252, 28, 55),
                         self.island.character_spritesheet.get_sprite(0, 308, 32, 52),
                         self.island.character_spritesheet.get_sprite(33, 304, 27, 56),
                         self.island.character_spritesheet.get_sprite(61, 309, 27, 52),
                         self.island.character_spritesheet.get_sprite(92, 311, 29, 50),
                         self.island.character_spritesheet.get_sprite(122, 307, 31, 53),
                         self.island.character_spritesheet.get_sprite(155, 305, 28, 56),
                         self.island.character_spritesheet.get_sprite(183, 310, 27, 51),
                         self.island.character_spritesheet.get_sprite(213, 310, 29, 51)
                         ]

        left_animations = [self.island.character_spritesheet.get_sprite(1, 520, 26, 55),
                           self.island.character_spritesheet.get_sprite(1, 578, 33, 52),
                           self.island.character_spritesheet.get_sprite(34, 579, 45, 48),
                           self.island.character_spritesheet.get_sprite(83, 578, 47, 48),
                           self.island.character_spritesheet.get_sprite(132, 578, 43, 48),
                           self.island.character_spritesheet.get_sprite(174, 580, 37, 48),
                           self.island.character_spritesheet.get_sprite(212, 579, 44, 48),
                           self.island.character_spritesheet.get_sprite(260, 581, 49, 48),
                           self.island.character_spritesheet.get_sprite(309, 580, 40, 46)
                           ]

        right_animations = [self.island.character_spritesheet.get_sprite(1, 520, 26, 55),
                            self.island.character_spritesheet.get_sprite(1, 578, 33, 52),
                            self.island.character_spritesheet.get_sprite(34, 579, 45, 48),
                            self.island.character_spritesheet.get_sprite(83, 578, 47, 48),
                            self.island.character_spritesheet.get_sprite(132, 578, 43, 48),
                            self.island.character_spritesheet.get_sprite(174, 580, 37, 48),
                            self.island.character_spritesheet.get_sprite(212, 579, 44, 48),
                            self.island.character_spritesheet.get_sprite(260, 581, 49, 48),
                            self.island.character_spritesheet.get_sprite(309, 580, 40, 46)
                            ]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.island.character_spritesheet.get_sprite(0, 0, 32, 55)
                self.image.set_colorkey(WHITE)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += .2
                if self.animation_loop >= 9:
                    self.animation_loop = 1
                self.image.set_colorkey(WHITE)

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.island.character_spritesheet.get_sprite(0, 252, 28, 55)
                self.image.set_colorkey(WHITE)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += .2
                if self.animation_loop >= 9:
                    self.animation_loop = 1
                self.image.set_colorkey(WHITE)

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.island.character_spritesheet.get_sprite(1, 520, 26, 55)
                self.image.set_colorkey(WHITE)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += .2
                if self.animation_loop >= 9:
                    self.animation_loop = 1
                self.image.set_colorkey(WHITE)

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.island.character_spritesheet.get_sprite(1, 520, 26, 55)
                self.image.set_colorkey(WHITE)
                self.image = pygame.transform.flip(self.image, True, False)

            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += .2
                if self.animation_loop >= 9:
                    self.animation_loop = 1
                self.image.set_colorkey(WHITE)
                self.image = pygame.transform.flip(self.image, True, False)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, island, x, y):
        self.island = island
        self._layer = ENEMY_LAYER
        self.groups = self.island.all_sprites, self.island.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.island.sephiroth.get_sprite(0, 0, 95, 70)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):
    def __init__(self, island, x, y):
        self.island = island
        self._layer = BLOCK_LAYER
        self.groups = self.island.all_sprites, self.island.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.island.terrain_spritesheet.get_sprite(961, 417, 29, 29)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, island, x, y):
        self.island = island
        self._layer = GROUND_LAYER
        self.groups = self.island.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.island.terrain_spritesheet.get_sprite(961, 417, 29, 30)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        