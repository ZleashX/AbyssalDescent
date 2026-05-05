import pygame
import random
from Data.Scripts.utils import Particle

class Characters:
    def __init__(self, game, assets, charatype, pos, size, hitbox):
        self.game = game
        self.charatype = charatype
        self.pos = list(pos)
        self.size = size
        self.hitbox = list(hitbox)
        self.move = [0, 0]
        self.vel = [0, 0]
        self.collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.action = ''
        self.flip = False
        self.assets = assets
        self.hitstop = 0

    def rect(self):
        return pygame.Rect(self.pos[0] + self.hitbox[0], self.pos[1] + self.hitbox[1], self.size[0], self.size[1])
    
    def determine_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.assets.get_asset(self.charatype + ' ' + self.action)

    def update(self, tilemap):

        self.hitstop = max(0,self.hitstop - 1)
        if self.hitstop > 0:
            return False

        self.collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.pos[0] += (self.move[0] + self.vel[0])
        char_rects = self.rect()
        for rect in tilemap.get_collision_tiles():
            if char_rects.colliderect(rect):
                if self.move[0] > 0 or self.vel[0] > 0:
                    char_rects.right = rect.left
                    self.collisions['right'] = True
                if self.move[0] < 0 or self.vel[0] < 0:
                    char_rects.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = char_rects.x - self.hitbox[0]

        self.pos[1] += (self.move[1] + self.vel[1])
        char_rects = self.rect()
        for rect in tilemap.get_collision_tiles():
            if char_rects.colliderect(rect):
                if self.vel[1] > 0:
                    char_rects.bottom = rect.top
                    self.collisions['bottom'] = True
                if self.vel[1] < 0:
                    char_rects.top = rect.bottom
                    self.collisions['top'] = True
                self.pos[1] = char_rects.y - self.hitbox[1]

        self.vel[1] = min(3,self.vel[1] + 0.1)
        if self.vel[0] > 0:
            self.vel[0] = max(0, self.vel[0] - 0.1)
        elif self.vel[0] < 0:
            self.vel[0] = min(0, self.vel[0] + 0.1)

        if self.move[0] > 0:
            self.flip = False
        if self.move[0] < 0:
            self.flip = True

        if self.collisions['bottom'] or self.collisions['top']:
            self.vel[1] = 0

        self.animation.resetloop()
        self.animation.update()
        return True

    def render(self, surf, offset):
        flipped_image = pygame.transform.flip(self.animation.img(), self.flip, False)
        pos_x = self.pos[0] - offset[0] - self.hitbox[0] - self.size[0] if self.flip else self.pos[0] - offset[0]
        surf.blit(flipped_image, (pos_x, self.pos[1] - offset[1]))

class Player(Characters):
    def __init__(self, game, assets, pos, size, hitbox):
        super().__init__(game, assets, 'player', pos, size, hitbox)
        self.isjump = False
        self.prevjump = ''
        self.air_time = 0
        self.animation = self.assets.get_asset('player idle')
        self.jumpfx = Particle("jump dust")
        self.isslide = False
        self.isdash = False
        self.numdash = 0
        self.combo = 0
        self.isattack = False
        self.dealdmg = False
        self.nextcombo = False
        self.dmgonce = False
        self.health = 4
        self.takedmg = 0
        self.walksfxtimer = 0

    def get_inputs(self):
        key = pygame.key.get_pressed()
        self.move[0] = 0

        if not self.isdash and not self.isattack:
            if key[pygame.K_LEFT]:
                if self.walksfxtimer == 0 and not self.isjump and not self.isslide and self.air_time < 6:
                    self.assets.sfx['walk'].play()
                    self.walksfxtimer = 20
                self.move[0] -= 1
            if key[pygame.K_RIGHT]:
                if self.walksfxtimer == 0 and not self.isjump and not self.isslide and self.air_time < 6:
                    self.assets.sfx['walk'].play()
                    self.walksfxtimer = 20
                self.move[0] += 1

    def jump(self):
        if self.isslide and (self.collisions['right'] and self.prevjump != 'right') or (self.collisions['left'] and self.prevjump != 'left'):
            self.assets.sfx['jump'].play()
            self.isjump = True
            self.isslide = False
            if self.collisions['right']:
                self.prevjump = 'right'
                self.vel[1] = max(-3, self.vel[1] - 3)
                self.vel[0] -= 2.5
                self.assets.sfx['jump'].play()
            elif self.collisions['left']:
                self.prevjump = 'left'
                self.vel[1] = max(-3, self.vel[1] - 3)
                self.vel[0] += 2.5
                self.assets.sfx['jump'].play()
        elif not self.isjump and not self.isdash and self.air_time < 6:
            self.assets.sfx['jump'].play()
            ljumpfx = (self.rect().centerx - self.jumpfx.width, self.rect().centery)
            self.jumpfx.startfx(ljumpfx, self.flip)
            self.vel[1] -= 3
            self.isjump = True
            self.determine_action('jump')

    def dash(self):
        if self.isdash == False and self.numdash != 0:
            self.numdash -= 1
            self.isdash = True
            self.determine_action('dash')
            self.assets.sfx['dash'].play()
            if self.flip:
                self.vel[0] = -4
            else:
                self.vel[0] = 4

    def attack(self):
        if not self.isattack and not self.isjump and not self.isdash and not self.isslide:
            self.determine_action('attack1')
            self.isattack = True
            self.combo = 1
        elif self.combo == 1:
            self.nextcombo = True

    def attackrect(self):
        if self.flip:
            return pygame.Rect(self.pos[0] - self.size[0] - 10, self.pos[1] + self.hitbox[1], 55, self.size[1])
        else:
            return pygame.Rect(self.pos[0] + self.hitbox[0], self.pos[1] + self.hitbox[1], 55, self.size[1])
        
    def turn_end_pillar(self,tilemap):
        if self.rect().colliderect(tilemap.get_end_pillar()):
            self.game.indexmap += 1
            self.game.change_map(self.game.indexmap)

    def update(self, tilemap):

        if self.health <= 0:
            self.determine_action('die')
            self.animation.update()
            if self.animation.finish:
                self.animation.resetloop()
                return True
            return False
   
        self.get_inputs()
        self.jumpfx.update()

        self.air_time += 1
        if self.collisions['bottom']:
            if self.air_time > 20:
                self.assets.sfx['landing'].play()
                self.determine_action('endfall')
            self.isdash = False
            self.numdash = 1
            self.isjump = False
            self.prevjump = ''
            self.air_time = 0

        if not super().update(tilemap):
            return False

        self.takedmg = max(0, self.takedmg - 1)
        self.walksfxtimer = max(0, self.walksfxtimer - 1)

        if self.nextcombo and self.animation.finish:
            self.determine_action('attack2')
            self.combo = 2
            self.nextcombo = False
            self.dmgonce = False
            self.dealdmg = False
            self.animation.resetloop()
        elif self.isattack and self.animation.finish:
            self.dmgonce = False
            self.dealdmg = False
            self.isattack = False
            self.combo = 0

        if self.isattack and not self.dealdmg:
            if self.combo == 1 and int(self.animation.current_frame) == 2:
                self.assets.sfx['attack'].play()
                self.dealdmg = True
            elif self.combo == 2 and int(self.animation.current_frame) == 1:
                self.assets.sfx['attack'].play()
                self.dealdmg = True

        if self.isdash and not self.animation.finish:
            self.vel[1] = 0
        elif self.isdash and self.animation.finish:
            self.isdash = False
            self.vel[0] = 0

        if (self.collisions['left'] or self.collisions['right']) and self.air_time > 5:
            if self.action != 'startslide' and not self.isslide:
                self.determine_action('startslide')
            else:
                self.determine_action('endslide')
            self.isdash = False
            self.isslide = True
            self.vel[0] = 0
            self.vel[1] = min(0.5,self.vel[1] + 0.1)
        else:
            self.isslide = False

        if not self.isslide and not self.isdash:
            if self.vel[1] < 0 and self.air_time > 5:
                self.determine_action('jump')
            elif self.vel[1] > -1 and self.vel[1] < 1 and self.air_time > 20:
                self.determine_action('midfall')
            elif self.vel[1] >= 1 and self.air_time > 20:
                self.determine_action('fall')
            elif (self.animation.finish or self.animation.loop):
                if self.move[0] != 0 :
                    self.determine_action('walk')
                else:
                    self.determine_action('idle')

        if self.takedmg == 0:
            char_rects = self.rect()
            for rect in tilemap.get_trap_tiles():
                if char_rects.colliderect(rect):
                    self.assets.sfx['hit'].play()
                    self.determine_action('damaged')
                    self.animation.resetloop()
                    self.animation.current_frame = 1
                    self.takedmg = 60
                    self.hitstop = 20
                    self.vel[1] -= 1
                    self.health -= 1
                    break
            for hellbot in self.game.hellbots:
                if hellbot.health > 0:
                    char_rects = self.rect()
                    if char_rects.colliderect(hellbot.rect()):
                        self.assets.sfx['hit'].play()
                        self.determine_action('damaged')
                        self.animation.resetloop()
                        self.animation.current_frame = 1
                        self.takedmg = 60
                        self.hitstop = 20
                        hellbot.hitstop = 20
                        self.vel[1] -= 1
                        self.health -= 1
                        if hellbot.flip:
                            self.vel[0] -= 1
                        else:
                            self.vel[0] += 1
                        break

    def render(self, surf, offset):
        super().render(surf,offset)
        self.jumpfx.render(surf, offset)
        

class Enemy(Characters):
    def __init__(self, game, assets, pos, size, hitbox):
        super().__init__(game, assets, 'enemy', pos, size, hitbox)
        self.animation = self.assets.get_asset('enemy idle')
        self.walktimer = 0
        self.health = 3
        self.hitfx = Particle('hit impact')

    def update(self, tilemap):
        if self.health <= 0:
            self.determine_action('die')
            self.animation.update()
            self.hitfx.update()
            if self.animation.finish:
                self.animation.resetloop()
                return True
            return False

        self.hitfx.update()
        self.walk()
        if not super().update(tilemap):
            return False

        char_rects = self.rect()
        for rect in tilemap.get_block_tiles():
            if char_rects.colliderect(rect):
                if self.move[0] > 0:
                        self.flip = True
                if self.move[0] < 0:
                        self.flip = False

        if self.move[0] != 0:
            self.determine_action('walk')
        else:
            self.determine_action('idle')

        if self.game.player.isattack and self.game.player.dealdmg and not self.game.player.dmgonce:
            if self.game.player.attackrect().colliderect(char_rects):
                self.determine_action('damaged')
                self.hitfx.startfx((self.pos[0] - self.hitbox[0],self.pos[1]),False)
                self.game.player.dmgonce = True
                self.hitstop = 15
                self.game.player.hitstop = 15
                self.vel[1] -= 1
                self.health -= 1
                if self.game.player.flip:
                    self.vel[0] -= 1
                else:
                    self.vel[0] += 1
        
        return False
        

    def walk(self):
        walkrand = random.randint(1,100)
        self.walktimer = max(0, self.walktimer - 1)
        isstop = False

        if walkrand != 10 and self.walktimer == 0:
            if self.flip:
                self.move[0] = -0.7
            else:
                self.move[0] = 0.7
        elif isstop == False and self.walktimer == 0:
            isstop = True
            self.walktimer = 120
            self.move[0] = 0

    def render(self, surf, offset):
        flipped_image = pygame.transform.flip(self.animation.img(), self.flip, False)
        pos_x = self.pos[0] - offset[0] - self.hitbox[0] - self.size[0] - 30 if self.flip else self.pos[0] - offset[0]
        surf.blit(flipped_image, (pos_x, self.pos[1] - offset[1]))
        self.hitfx.render(surf, offset)