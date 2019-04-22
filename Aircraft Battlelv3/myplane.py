import pygame
import random
from pygame.locals import *
from os import path

#######################################基本参数配置#######################################

# 获取图片库和声音库路径
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
pygame.display.set_caption("Four Second")
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

# 加载敌机图片
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
for image in enemies_list:
    enemies_img = pygame.image.load(path.join(img_dir, image)).convert()
    enemies_img = pygame.transform.scale(enemies_img, (80, 60))
    enemies_images.append(enemies_img)
# 加载爆炸图片
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    # 敌机爆炸
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
class Player(pygame.sprite.Sprite):
    '''创建玩家类'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 98))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30
        self.speedx = 0
        self.speedy = 0
        # 方向控制：A控制左、D控制右、W控制上、S控制下、A+W控制左上、A+S控制左下、D+W控制右上、D+S控制右下
        keystate = pygame.key.get_pressed()
        if keystate[K_a]:
            self.speedx = -5
        if keystate[K_d]:
            self.speedx = 5
        if keystate[K_w]:
            self.speedy = -5
        if keystate[K_s]:
            self.speedy = 5
        # 发射控制：空格
        if keystate[pygame.K_j]:
            self.shoot()
        # 设置玩家移动边界
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # 单火力
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            # 双火力
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)

            # 三火力
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top)  # 导弹
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)


    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)