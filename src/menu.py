'''
Created on Jan 25, 2012

@author: Matej
'''



class Menu:
    def __init__(self, options,position,font, fontBig):
        self.choices=options
        self.font=font
        self.position=position
        self.selected=0
        self.fontBig=fontBig
        
    def up(self):
        self.selected=self.selected-1
        if(self.selected<0):
            self.selected=len(self.choices)-1
            
    def down(self):
        self.selected=self.selected-1
        if(self.selected>= len(self.choices)):
            self.selected=0
            
    def getSelected(self):
        return self.choices[self.selected]
    
    def draw(self, screen):
        for i,choice in enumerate(self.choices):
            msg = choice
            if(self.selected==i):
                msgSurface = self.fontBig.render(msg,False, (20,50,100))
            else:
                msgSurface = self.fontSmall.render(msg,False, (20,50,100))
            msgRect = msgSurface.get_rect()
            msgRect.topleft=(self.position[0],self.position[1]+i*30)
            
            screen.blit(msgSurface,msgRect)
        