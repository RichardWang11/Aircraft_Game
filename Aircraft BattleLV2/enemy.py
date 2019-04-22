import pygame
from os import path
import random

img_dir = path.join(path.dirname(__file__), 'pic')
sound_folder = path.join(path.dirname(__file__), 'sounds')

# 定义游戏窗口、玩家血量条尺寸，游戏运行速度、炮火持续时间等参数
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# 定义白、黑、红、绿、蓝、黄的RGB参数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 初始化pygame模块，创建游戏窗口、游戏窗口命名、创建跟踪时间对象
pygame.init()
pygame.mixer.init()  # 初始化音效
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aircraft Battle")
clock = pygame.time.Clock()

# 定义文本字体
font_name = pygame.font.match_font('arial')

#######################################加载图片#######################################

# 加载游戏进行中背景图片
background = pygame.image.load(path.join(img_dir, 'new2.png')).convert()
background = pygame.transform.scale(background, (WIDTH, 1536))
height = -936

# 加载玩家图片
player_img = pygame.image.load(path.join(img_dir, 'enemies1.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (20, 20))
player_mini_img.set_colorkey(BLACK)

# 加载玩家炮弹、导弹图片
bullet_img = pygame.image.load(path.join(img_dir, 'zidan2.png')).convert()
bullet1_img = pygame.image.load(path.join(img_dir, 'zidan.png')).convert()
missile1_img = pygame.image.load(path.join(img_dir, '1.png')).convert_alpha()

# 加载敌机炮弹图片
enemies_bullet_img = pygame.image.load(path.join(img_dir, 'direnzidan.png')).convert()

# 加载盾牌、闪电图片
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()

# 加载敌机和火山石图片
enemies_images = []
lava_images = []
# 敌机
enemies_list = [
    'enemies2.png',
    'enemies2.png',
    'feiji1.png',
    'feiji3.png',
    'player.png'

]
# 火山石
lava_list = [
    'yunshi1.png',
    'yunshi2.png',
    'yunshi3.png',

]
for image in enemies_list:
    enemies_img = pygame.image.load(path.join(img_dir, image)).convert()
    enemies_img = pygame.transform.scale(enemies_img, (80, 60))
    enemies_images.append(enemies_img)
for image in lava_list:
    lava_images.append(pygame.image.load(path.join(img_dir, image)).convert())

# 加载爆炸图片
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    # 敌机、火山石爆炸
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    # 大爆炸
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    # 小爆炸
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    # 玩家爆炸
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

##############################################################################

class Mob(pygame.sprite.Sprite):
    '''创建敌机类'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemies_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if random.randrange(10) >= 6:
            self.enemies_shoot()
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def enemies_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            from feiji2.bullet import EnemiesBullet
            enemies_bullet = EnemiesBullet(self.rect.centerx, self.rect.bottom)
            from feiji2._main_ import all_sprites
            all_sprites.add(enemies_bullet)
            from feiji2._main_ import enemies_bullets
            enemies_bullets.add(enemies_bullet)



class Lava(pygame.sprite.Sprite):
    '''创建火山石类'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(lava_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()