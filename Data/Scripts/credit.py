import pygame, sys

class Credit:
    def __init__(self, assets):
        pygame.init()
        self.backbutton = pygame.Rect(10,10,60,50)
        self.assets = assets
        self.credit = self.assets.ui['credit']
        self.isplayed = False

    def render(self,surf):
        run = True
        while run:
            mx,my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.backbutton.collidepoint(mx,my):
                            self.assets.sfx['click'].play()
                            run = False

            if self.backbutton.collidepoint(mx,my) and not self.isplayed:
                self.assets.sfx['hover'].play()
                self.isplayed = True
            elif not self.backbutton.collidepoint(mx,my):
                self.isplayed = False
            surf.blit(self.credit,(0,0))
            pygame.display.update()