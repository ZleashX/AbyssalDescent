import pygame

class Spritesheet:
    def __init__(self,sheet, width, height):
        self.sheet = sheet
        self.sheet_width, self.sheet_height = self.sheet.get_size()
        self.width = width
        self.height = height

    def get_images(self,index, horizontal = True):
        index -= 1
        images = []
        if horizontal:
            for x in range(0, self.sheet_width, self.width):
                img = self.sheet.subsurface(pygame.Rect(x, index * self.height, self.width, self.height))
                images.append(img)
        else:
            for y in range(0, self.sheet_height, self.height):
                img = self.sheet.subsurface(pygame.Rect(index * self.width, y, self.width, self.height))
                images.append(img)
        
        return images
    
class Animation:
    def __init__(self, images, speed, length, loop = True):
        self.images = images
        self.speed = speed
        self.loop = loop
        self.length = length - 1
        self.current_frame = 0
        self.finish = False

    def update(self):
        if self.current_frame <= self.length:
            self.current_frame += self.speed
        elif self.loop == True:
            self.current_frame = 0
        else:
            self.finish = True

    def resetloop(self):
        if self.finish == True:
            self.current_frame = 0
            self.finish = False

    def getWidth(self):
        temp = self.images[0]
        return temp.get_width()

    def img(self):
        return self.images[int(self.current_frame)]
    
class Particle:
    def __init__(self,name):
        self.pos = [0,0]
        self.start = False
        self.assets = Assets()
        self.anim = self.assets.get_asset(name)
        self.width = self.anim.getWidth()
    
    def update(self):
        if self.start == True:
            self.anim.update()

        if self.anim.finish == True:
            self.start = False
            self.anim.resetloop()

    def startfx(self, pos, flip):
        if self.start != True:
            self.start = True
            self.pos = list(pos)
            self.flip = flip

    def render(self, surf, offset):
        if self.start == True:
            flipped_image = pygame.transform.flip(self.anim.img(), self.flip, False)
            pos_x = self.pos[0] - offset[0] + self.anim.getWidth() if self.flip else self.pos[0] - offset[0]
            surf.blit(flipped_image, (pos_x, self.pos[1] - offset[1]))

class Assets:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Assets, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.player_spritesheet = Spritesheet(pygame.image.load('Data/Assets/Entities/Player/player.png'), 90, 37)
        self.jumpfx_spritesheet = Spritesheet(pygame.image.load('Data/Assets/Particle/jump dust.png'), 24, 14)
        self.hitfx_spritesheet = Spritesheet(pygame.image.load('Data/Assets/Particle/hit impact.png'), 75, 23)
        self.hellbot_spritesheet = Spritesheet(pygame.image.load('Data/Assets/Entities/Enemy/hellbot.png'), 92, 36)
        self.endpillar_spritesheet = Spritesheet(pygame.image.load('Data/Assets/Map/End/end.png'), 16, 19)
        
        self.anim = {
            'player idle': Animation(self.player_spritesheet.get_images(2), 0.2, 9),
            'player walk': Animation(self.player_spritesheet.get_images(3), 0.2, 8),
            'player jump': Animation(self.player_spritesheet.get_images(14), 0.2, 3),
            'player midfall': Animation(self.player_spritesheet.get_images(15), 0.2, 4),
            'player fall': Animation(self.player_spritesheet.get_images(16), 0.2, 3),
            'player endfall': Animation(self.player_spritesheet.get_images(20), 0.2, 4, False),
            'player startslide': Animation(self.player_spritesheet.get_images(23), 0.2, 2, False),
            'player endslide': Animation(self.player_spritesheet.get_images(24), 0.2, 3),
            'player dash': Animation(self.player_spritesheet.get_images(13), 0.2, 6, False),
            'player attack1': Animation(self.player_spritesheet.get_images(10), 0.2, 5, False),
            'player attack2': Animation(self.player_spritesheet.get_images(11), 0.2, 6, False),
            'player damaged': Animation(self.player_spritesheet.get_images(26), 0.1, 2, False),
            'player die': Animation(self.player_spritesheet.get_images(27), 0.1, 6, False),
            'enemy idle': Animation(self.hellbot_spritesheet.get_images(1, False), 0.07, 6),
            'enemy walk': Animation(self.hellbot_spritesheet.get_images(2, False), 0.1, 8),
            'enemy damaged': Animation(self.hellbot_spritesheet.get_images(6, False), 0.1, 1, False),
            'enemy die': Animation(self.hellbot_spritesheet.get_images(5, False), 0.1, 10, False),
            'jump dust': Animation(self.jumpfx_spritesheet.get_images(1), 0.2, 7, False),
            'hit impact': Animation(self.hitfx_spritesheet.get_images(1), 0.2, 6, False),
            'end inactive': Animation(self.endpillar_spritesheet.get_images(1), 0.2, 1),
            'end start': Animation(self.endpillar_spritesheet.get_images(1), 0.1, 7, False),
            'end idle': Animation(self.endpillar_spritesheet.get_images(2), 0.2, 4)
        }

        self.sfx = {
            'jump' : pygame.mixer.Sound('Data/Assets/SFX/jump.wav'),
            'landing' : pygame.mixer.Sound('Data/Assets/SFX/landing.wav'),
            'hit' : pygame.mixer.Sound('Data/Assets/SFX/hit.wav'),
            'walk' : pygame.mixer.Sound('Data/Assets/SFX/walk.wav'),
            'dash' : pygame.mixer.Sound('Data/Assets/SFX/dash.wav'),
            'attack' : pygame.mixer.Sound('Data/Assets/SFX/attack.wav'),
            'hover' : pygame.mixer.Sound('Data/Assets/SFX/hover.wav'),
            'click' : pygame.mixer.Sound('Data/Assets/SFX/click.wav')
        }

        self.ui = {
            'heart' : pygame.transform.smoothscale(pygame.image.load('Data/Assets/UI/heart.png'),(28,28)),
            'menu' : pygame.image.load('Data/Assets/UI/menubutton.png'),
            'enemyicon' : pygame.image.load('Data/Assets/UI/enemyicon.png'),
            'mainmenu' : pygame.image.load('Data/Assets/UI/mainmenu.png'),
            'credit' : pygame.image.load('Data/Assets/UI/credit.png')
        }

    def add_asset(self, key, value):
        self.assets.update({key: value})

    def get_asset(self, key):
        return self.anim[key]