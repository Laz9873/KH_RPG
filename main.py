import asyncio 
import random
import pygame.display
import button
from sprites import *
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 800
screen_height = 450 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Kingdom Hearts RPG_Demo')  # game title

async def main():

        current_fighter = 1
        game_over = 0
        clicked = False
        cure = False
        action_cool_down = 0
        
        run00 = True
        run0 = False
        run1 = False  # runs Boss fight
        run2 = False  # runs retry screen
        run3 = False  # runs end game screen

        

        while run00:

            if start_button.draw():
                start_screen = 1
                if start_screen != 0:
                    fade_out(800, 600)
                    run00 = False
                    run0 = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run00 = False
            pygame.display.update()

            while run0:

                clock.tick(fps)
                g.main()
                if map_out == 1:
                    fade_out(800, 600)
                    run0 = False
                    run1 = True
                    mixer.music.load(f'final_music/One Winged Angel _ Kingdom Hearts HD 2.5 ReMIX Remastered OST.ogg')
                    mixer.music.play(-1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run0 = False

                pygame.display.update()

                while run1:

                    # frames for animation
                    clock.tick(fps)

                    # draw the background
                    draw_bg_battle()

                    # draw the panel
                    draw_panel()
                    sora_health_bar.draw(sora_fighter.hp)
                    sephiroth_health_bar.draw(sephiroth.hp)

                    # draw fighting functions includes animations and positions
                    sora_fighter.update()
                    sora_fighter.positioning_for_sora_fighter()
                    sora_fighter.draw()
                    sephiroth.update()
                    sephiroth.positioning_for_sephiroth()
                    sephiroth.draw()

                    # draw damage text
                    damage_text_group.update()
                    damage_text_group.draw(screen)

                    # control player action
                    # reset action variables
                    attack = False
                    cure = False
                    target = None
                    pos = pygame.mouse.get_pos()

                    # makes mouse visible
                    pygame.mouse.set_visible(True)
                    if sephiroth.rect.collidepoint(pos):
                        # hide mouse
                        pygame.mouse.set_visible(False)
                        # show key_blade in place of cursor
                        screen.blit(key_blade_img, pos)
                        if clicked and sephiroth.alive:
                            attack = True
                            target = sephiroth

                    if cure_button.draw():
                        cure = True
                    # show number of potions remaining
                    draw_text(str(sora_fighter.cure), font, green, 277, screen_height - bottom_panel + 78)

                    if game_over == 0:
                        # player action and enemy action
                        if sora_fighter.alive:
                            if current_fighter == 1:
                                action_cool_down += 1
                                if action_cool_down >= action_wait_time:
                                    if attack and target is not None:
                                        sora_fighter.attack(target)
                                        attack_sound = mixer.Sound('sound/sora/attack/Sora_Attack! (3).ogg')
                                        attack_sound.play()
                                        hit_sound = mixer.Sound('sound/sephiroth/hit/Hit!.ogg')
                                        hit_sound.play()
                                        current_fighter += 1
                                        action_cool_down = 0

                                    # cure
                                    if cure:
                                        if sora_fighter.hp != sora_fighter.max_hp:

                                            if sora_fighter.cure > 0:
                                                heal_sound = mixer.Sound('sound/sora/cure/Heal!.ogg')
                                                heal_sound.play()
                                                # check if cure heal beyond max health
                                                if sora_fighter.max_hp - sora_fighter.hp > cure_effect:
                                                    heal_amount = cure_effect
                                                else:
                                                    heal_amount = sora_fighter.max_hp - sora_fighter.hp
                                                sora_fighter.hp += heal_amount
                                                sora_fighter.cure -= 1
                                                current_fighter += 1
                                                action_cool_down = 0
                                            else:
                                                unable = mixer.Sound('sound/sora/unable/se000.ps3176.ogg')
                                                unable.play()
                                        else:
                                            unable = mixer.Sound('sound/sora/unable/se000.ps3176.ogg')
                                            unable.play()

                            # if current_fighter == 2:
                            if sephiroth.alive:
                                if current_fighter == 2:
                                    action_cool_down += 1
                                    if action_cool_down >= action_wait_time:
                                        sephiroth.attack(sora_fighter)
                                        attack_sound = mixer.Sound('sound/sephiroth/attack/Sephiroth_Attack!.ogg')
                                        attack_sound.play()
                                        hit_sound = mixer.Sound('sound/sora/hit/Hit! (1).ogg')
                                        hit_sound.play()
                                        current_fighter = 1
                                        action_cool_down = 0
                            else:
                                game_over = 1

                        else:
                            game_over = -1

                        if game_over == -1:
                            mixer.music.stop()
                            fade_out(800, 600)
                            run1 = False
                            run2 = True
                            while run2:
                                pygame.mouse.set_visible(True)
                                if retry_button.draw():
                                    fade_out(800, 600)
                                    mixer.music.load(
                                        f'final_music/One Winged Angel _ Kingdom Hearts HD 2.5 ReMIX Remastered OST.ogg')
                                    mixer.music.play(-1)
                                    sora_fighter.retry()
                                    sephiroth.retry()
                                    current_fighter = 1
                                    game_over = 0
                                    run2 = False
                                    run1 = True

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        run2 = False
                                pygame.display.update()
                        if game_over == 1:
                            mixer.music.stop()
                            fade_out(800, 600)
                            pygame.mixer.music.unload()
                            mixer.music.load(f'final_music/Kingdom Hearts_ Kairis Theme II.ogg')
                            mixer.music.play(-1)
                            run1 = False
                            run3 = True
                            while run3:
                                pygame.mouse.set_visible(True)
                                draw_bg_ending()

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        run3 = False
                                pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run1 = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            clicked = True
                        else:
                            clicked = False
                    pygame.display.update()
                
        await asyncio.sleep(0)


# define game variables
total_fighters = 2
action_wait_time = 90
attack = False
cure_effect = 15
map_out = 0


# defining text
font = pygame.font.SysFont('Times New Roman', 17)

# defining colors
grey = (128, 128, 128)
black = (0, 0, 0)
green = (0, 255, 0)
orange = (255, 165, 0)

# load images
# background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
ending_img = pygame.image.load('img/Background/zank you.jpg').convert_alpha()

# panel image
panel_img = pygame.image.load('img/Panel/kh_panel.png')
# button images
cure_img = pygame.image.load('img/Icon/cure.png')

# retry image
retry_img = pygame.image.load('img/Icon/retry-.png')

start_img = pygame.image.load('img/Icon/start.png')

# key_blade image
key_blade_img = pygame.image.load('img/Icon/key_cursor.png')


# drawing text function
def draw_text(text, fonts, text_col, x, y):
    img = fonts.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg_battle():
    screen.blit(background_img, (0, 0))


def draw_bg_ending():
    screen.blit(ending_img, (0, 0))


# drawing panel
def draw_panel():
    # drawing panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # show sora's and opponents stats
    draw_text(f'HP: {sora_fighter.hp}', font, grey, 150, screen_height - bottom_panel + 50)
    draw_text(f'HP: {sephiroth.hp}', font, grey, 487, screen_height - bottom_panel + 50)


class Island:
    def __init__(self):
        self.enemy = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.playing = True
        # update sprite sheet in file folder
        self.character_spritesheet = Spritesheet('img/Sora/island/character.png')
        self.terrain_spritesheet = Spritesheet('img/Sora/island/terrain.png')
        self.sephiroth = Spritesheet('img/Sephiroth/island/sephiroth.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)

    def new(self):

        self.createTilemap()

    def events(self):
        global map_out
        if not self.playing:
            map_out = 1

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self, screen):
        screen.fill(BLACK)
        # can change background image
        self.all_sprites.draw(screen)
        # center a position.

    def main(self):
        # game loop
        self.events()
        self.update()
        self.draw(screen)


g = Island()
g.new()


# class for fighting
class Fighting:
    def __init__(self, x, y, name, max_hp, strength, cure):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_cure = cure
        self.cure = cure
        self.alive = True
        self.sprite = []
        self.current_sprite = 0
        self.action = 0  # 0 idle, 1 attack, 2 hurt, 3 dead

        # loading idle images...
        temp_list = [pygame.image.load(f'img/{self.name}/idle/idle000.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle001.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle002.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle003.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle004.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle005.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle006.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle007.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle008.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle009.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle010.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle011.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle012.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle013.png'),
                     pygame.image.load(f'img/{self.name}/idle/idle014.png')]
        self.sprite.append(temp_list)

        # loading attack images...
        temp_list = [pygame.image.load(f'img/{self.name}/attack/atk000.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk001.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk002.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk003.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk004.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk005.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk006.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk007.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk008.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk009.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk010.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk011.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk012.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk013.png'),
                     pygame.image.load(f'img/{self.name}/attack/atk014.png')]
        self.sprite.append(temp_list)

        # hurt animation
        temp_list = [pygame.image.load(f'img/{self.name}/hurt/hurt000.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt001.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt002.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt003.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt004.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt005.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt006.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt007.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt008.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt009.png'),
                     pygame.image.load(f'img/{self.name}/hurt/hurt010.png')]
        self.sprite.append(temp_list)

        # dead animation
        temp_list = [pygame.image.load(f'img/{self.name}/dead/dead000.png')]
        self.sprite.append(temp_list)

        self.image = self.sprite[self.action][self.current_sprite]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.current_sprite += 0.4

        if self.current_sprite >= len(self.sprite[self.action]):
            if self.action == 3:
                self.current_sprite = len(self.sprite[self.action]) - 1
            else:
                self.idle()
        self.image = self.sprite[self.action][int(self.current_sprite)]

    def idle(self):
        self.action = 0
        self.current_sprite = 0

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.dead()
        damage_text = DamageText(target.rect.x, target.rect.y, str(damage), orange)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.current_sprite = 0

    def hurt(self):
        self.action = 2
        self.current_sprite = 0

    def dead(self):
        self.action = 3
        self.current_sprite = 0

    def retry(self):
        self.alive = True
        self.cure = self.start_cure
        self.hp = self.max_hp
        self.current_sprite = 0
        self.action = 0

    def positioning_for_sephiroth(self):
        if self.action == 1:
            self.rect.center = (580, 287)

    def positioning_for_sora_fighter(self):
        if self.action == 1:
            self.rect.center = (0, 270)


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update to the new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, black, (self.x, self.y, 100, 10))
        pygame.draw.rect(screen, grey, (self.x, self.y, 100 * ratio, 10))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete damage text after few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

sora_fighter = Fighting(0, 270, 'Sora', 50, 15, 3)
sephiroth = Fighting(580, 287, 'Sephiroth', 99, 10, 0)


sora_health_bar = HealthBar(150, screen_height - bottom_panel + 70, sora_fighter.hp, sora_fighter.max_hp)
sephiroth_health_bar = HealthBar(487, screen_height - bottom_panel + 70, sephiroth.hp, sephiroth.max_hp)

cure_button = button.Button(screen, 255, screen_height - bottom_panel + 60, cure_img, 20, 20)
retry_button = button.Button(screen, 340, 200, retry_img, 110, 40)
start_button = button.Button(screen, 340, 200, start_img, 110, 40)


def fade_out(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

asyncio.run(main())
