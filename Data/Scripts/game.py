import pygame
import sys

from Data.Scripts.tilemap import Tilemap
from Data.Scripts.characters import Player , Enemy
from Data.Scripts.ui import Ui
from Data.Scripts.credit import Credit

class Game:
    def __init__(self, window, clock, assets):
        pygame.init()

        self.window = window
        self.display = pygame.Surface((320,240))
        self.blackrect = pygame.Rect(0,0,320,240)
        self.clock = clock
        self.assets = assets
        self.player = Player(self,self.assets,(50,50),(13,24),(22,10))
        self.map = Tilemap(self,self.assets,16)
        self.ui = Ui(self.assets)
        self.credit = Credit(self.assets)
        self.menubutton = pygame.Rect(450,42,90,60)
        self.cam = [0,0]
        self.indexmap = 0
        self.isplayed = False


    def run(self):
        pygame.mixer.music.load('Data/Assets/SFX/ambience.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        run = True
        while run:
            mx,my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menubutton.collidepoint(mx,my):
                            self.assets.sfx['click'].play()
                            pygame.mixer.music.stop()
                            run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_x:
                        self.player.dash()
                    elif event.key == pygame.K_c:
                        self.player.attack()
                    elif event.key == pygame.K_z and self.endstart:
                        self.player.turn_end_pillar(self.map)

            if self.menubutton.collidepoint(mx,my) and not self.isplayed:
                self.assets.sfx['hover'].play()
                self.isplayed = True
            elif not self.menubutton.collidepoint(mx,my):
                self.isplayed = False

            if self.indexmap == 3:
                run = False
                pygame.mixer.music.stop()
                self.credit.render(self.window)

            pygame.draw.rect(self.display, (11,11,11), self.blackrect)
            self.cam[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.cam[0]) / 30
            self.cam[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.cam[1]) / 30
            render_cam = (int(self.cam[0]), int(self.cam[1]))

            self.map.draw_tile(self.display, render_cam, self.player.pos)

            for hellbot in self.hellbots.copy():
                enemydeath = hellbot.update(self.map)
                hellbot.render(self.display, render_cam)
                if enemydeath:
                    self.hellbots.remove(hellbot)
                    self.totEnemy -= 1

            if self.totEnemy == 0 and not self.endstart:
                self.map.start_end_pillar()
                self.endstart = True

            playerdeath = self.player.update(self.map)
            if playerdeath:
                self.player = Player(self,self.assets,(50,50),(13,24),(22,10))
                self.change_map(self.indexmap)
            else:
                self.player.render(self.display, render_cam)

            self.ui.render(self,self.display,self.player)
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def change_map(self,index):
        self.indexmap = index
        self.endstart = False
        self.map.set_map(index)
        match index:
            case 2: 
                self.player.pos = [16,288]
            case _:
                self.player.pos = [50,50]
        self.hellbots = []
        for spawner in self.map.get_spawner():
                self.hellbots.append(Enemy(self,self.assets,(spawner.x- 10,spawner.y - 18),(13,24),(12,10)))
        self.totEnemy = len(self.hellbots)
