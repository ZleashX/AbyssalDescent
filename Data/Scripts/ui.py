import pygame

class Ui:
    def __init__(self,assets):
        self.assets = assets
        self.font = pygame.font.SysFont(None,24)

    def render(self,game,surf,player):
        enemytextimg = self.font.render(str(game.totEnemy), True, "white")
        surf.blit(enemytextimg, (260,18))
        surf.blit(self.assets.ui['enemyicon'],(270,10))
        surf.blit(self.assets.ui['menu'],(150,14))
        for x in range (0,player.health):
            surf.blit(self.assets.ui['heart'], (10 + x * 30, 10))