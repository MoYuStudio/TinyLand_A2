
import os
import glob
import pygame

class Tile:
    def __init__(self,pos,code,tile_data,pixal_level):
        '''
            瓷砖对象
        '''
        self.pos = pos
        self.code = code
        self.tile_data = tile_data
        self.pixal_level = pixal_level
        
        num = []
        for filename in glob.glob(r'tinyland/assets/tile/*.png'):
            num.append(filename)
        self.tile_num = len(num)
        
        self.assets_small = [pygame.image.load('tinyland/assets/tile/tile'+str(i)+'.png')for i in range(0,(self.tile_num),1)]
        self.assets = [pygame.transform.scale(self.assets_small[i],(16*self.pixal_level, 16*self.pixal_level))for i in range(0,(self.tile_num),1)]
        
        self.rect = self.assets[self.code].get_rect()
        self.width = self.rect.width
        
        self.mask_small = pygame.image.load('tinyland/assets/mask/landtile_mask.png').convert_alpha()
        self.mask = pygame.transform.scale(self.mask_small,((self.width,self.width)))
        
        self.timer_timer = {'grow':0,'animation':0}
        
        self.offset = [0,0]
        
    def renderer(self,surface):
        self.timer()
        self.rect.x = self.pos['z']*(self.width/2)-self.pos['x']*(self.width/2)+self.offset[0]
        self.rect.y = self.pos['x']*(self.width/4)+self.pos['z']*(self.width/4)+self.offset[1]+(-self.width/2)*int(self.pos['y'])
        
        surface.blit(self.assets[self.code], self.rect)
        
    def timer(self):
        for type in self.timer_timer:
            try:
                timer = self.tile_data[str(self.code)][type+'_timer']
                nextfps = self.tile_data[str(self.code)][type+'_nextfps']
                if timer >= 0:
                    self.timer_timer[type] += 1
                if self.timer_timer[type] == timer:
                    self.code = nextfps
                    self.timer_timer[type] = 0
            
            except:
                pass
        
    def touch(self,change_tile):
        if self.pos['y'] == '1':
            touch_rect = self.rect.copy()
            touch_rect.y = touch_rect.y + touch_rect.height/2
            
            pos = pygame.mouse.get_pos()
            tile_mask = pygame.mask.from_surface(self.mask)
            pos_in_mask = (pos[0]-touch_rect.x),(pos[1]-touch_rect.y)
            touching = touch_rect.collidepoint(*pos) and tile_mask.get_at(pos_in_mask)
            
            if pygame.mouse.get_pressed()[0] == True:
                if touching == True:
                    if self.code == 0:
                        self.code = change_tile
