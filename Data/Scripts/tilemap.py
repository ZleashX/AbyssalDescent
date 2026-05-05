import pygame
from pytmx.util_pygame import load_pygame

class Tilemap:
    def __init__(self, game, assets, tile_size=16):
        self.game = game
        self.assets = assets
        self.tile_size = tile_size
        self.collision_tiles = []
        self.spawner_tiles = []
        self.block_tiles = []
        self.trap_tiles = []
        self.end_pillar = pygame.Rect(0,0,0,0)
        self.map_data = load_pygame('Data/Assets/Map/tutorial.tmx')
        self.end_anim = self.assets.get_asset('end inactive')
        for layer in self.map_data.layers:
            if (layer.name == 'Blocker'):
                for obj in layer:
                    self.block_tiles.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            else:
                for x,y,gid in layer:
                    tile_img = self.map_data.get_tile_image_by_gid(gid)
                    if (layer.name == 'Collider' and tile_img != None):
                        self.collision_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'Spawner' and tile_img != None):
                        self.spawner_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'Trap' and tile_img != None):
                        self.trap_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'End' and tile_img != None):
                        self.end_pillar = pygame.Rect(x * self.tile_size, (y * self.tile_size) - 3, self.tile_size, self.tile_size)

    def draw_tile(self, surf, offset, playerpos):
        if not self.end_anim.loop and self.end_anim.finish:
            self.end_anim.resetloop()
            self.end_anim = self.assets.get_asset('end idle')
        self.end_anim.update()
        for layer in self.map_data.visible_layers:
            for x, y, image in layer.tiles():
                #check if tile within camera before blit
                xdisplay_offset = (x+4)*self.tile_size >= (playerpos[0] - (surf.get_width() / 2)) and (x-8)*self.tile_size <= (playerpos[0] + (surf.get_width() / 2))
                ydisplay_offset = (y+4)*self.tile_size >= (playerpos[1] - (surf.get_height() / 2)) and (y-4)*self.tile_size <= (playerpos[1] + (surf.get_height() / 2))
                if (xdisplay_offset and ydisplay_offset and image != None):
                    surf.blit(image,(x*self.tile_size - offset[0], y*self.tile_size - offset[1]))
        surf.blit(self.end_anim.img(),(self.end_pillar.x - offset[0],self.end_pillar.y - offset[1]))
                    
    def set_map(self,index):
        match index:
            case 0:
                self.map_data = load_pygame('Data/Assets/Map/tutorial.tmx')
            case 1:
                self.map_data = load_pygame('Data/Assets/Map/level1.tmx')
            case 2:
                self.map_data = load_pygame('Data/Assets/Map/level2.tmx')
        self.collision_tiles = []
        self.spawner_tiles = []
        self.block_tiles = []
        self.trap_tiles = []
        self.end_pillar = pygame.Rect(0,0,0,0)
        self.end_anim = self.assets.get_asset('end inactive')
        for layer in self.map_data.layers:
            if (layer.name == 'Blocker'):
                for obj in layer:
                    self.block_tiles.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            else:
                for x,y,gid in layer:
                    tile_img = self.map_data.get_tile_image_by_gid(gid)
                    if (layer.name == 'Collider' and tile_img != None):
                        self.collision_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'Spawner' and tile_img != None):
                        self.spawner_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'Trap' and tile_img != None):
                        self.trap_tiles.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                    elif (layer.name == 'End' and tile_img != None):
                        self.end_pillar = pygame.Rect(x * self.tile_size, (y * self.tile_size) - 3, self.tile_size, self.tile_size)

    def start_end_pillar(self):
        self.end_anim = self.assets.get_asset('end start')

    def get_collision_tiles(self):
        return self.collision_tiles
    
    def get_spawner(self):
        return self.spawner_tiles
    
    def get_block_tiles(self):
        return self.block_tiles
    
    def get_trap_tiles(self):
        return self.trap_tiles
    
    def get_end_pillar(self):
        return self.end_pillar
        
