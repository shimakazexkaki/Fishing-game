# -*- coding: utf-8 -*-
"""
Created on Sat May 27 14:40:44 2023

@author: User
"""
''' A1.1:以註解#a表示
    A1.2:以註解#a2表示'''
import pygame
import random
import os

#基礎設定區
FPS = 60
WIDTH = 650
HEIGHT = 850

#顏色區
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (0,200,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

#遊戲初始化 and 遊戲畫面
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('釣魚小遊戲')
clock = pygame.time.Clock()

#載入圖片
fishing_bar = pygame.image.load(os.path.join('img', 'fishing_bar.png')).convert()
back_1 = pygame.image.load(os.path.join('img', 'fishing_back_1.png')).convert()
back_1 = pygame.transform.scale(back_1, (WIDTH,HEIGHT))
back_2 = pygame.image.load(os.path.join('img', 'fishing_back_2.png')).convert()
back_2 = pygame.transform.scale(back_2, (WIDTH,HEIGHT))
#不同魚類 #b
anchovy = pygame.image.load(os.path.join('img', 'Anchovy.png')).convert()
octopus = pygame.image.load(os.path.join('img', 'Octopus.png')).convert()
radioactive_carp = pygame.image.load(os.path.join('img', 'Radioactive_Carp.png')).convert()
sea_cucumber = pygame.image.load(os.path.join('img', 'Sea_Cucumber.png')).convert()
#放大魚類 #b
anchovy_big = pygame.transform.scale(anchovy, (100,100))
octopus_big = pygame.transform.scale(octopus, (100,100))
radioactive_carp_big = pygame.transform.scale(radioactive_carp, (100,100))
sea_cucumber_big = pygame.transform.scale(sea_cucumber, (100,100))

#載入音效音樂
pygame.mixer.music.load(os.path.join('music', 'ost.mp3'))   #背景音樂
pygame.mixer.music.set_volume(0.45) #a
#a
got_fish = pygame.mixer.Sound(os.path.join('music', 'jingle1.wav'))
fish_escape = pygame.mixer.Sound(os.path.join('music', 'fishEscape.wav'))
fish_bite = pygame.mixer.Sound(os.path.join('music', 'fishBite.wav'))
fish_bite.set_volume(0.8)
fish_hit = pygame.mixer.Sound(os.path.join('music', 'FishHit.wav'))
fish_hit.set_volume(0.6)
#b
fish_line_sound = pygame.mixer.Sound(os.path.join('music', 'fishing_line.mp3'))
fish_line_sound.set_volume(0.6)
special = pygame.mixer.Sound(os.path.join('music', 'getNewSpecialItem.wav'))

#載入字體 #b
font_name = pygame.font.match_font('arial')

#函式區
def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    elif hp > 100:
        hp = 100
    BAR_LENGTH = 30
    BAR_HEIGHT = 660
    fill = (hp/100)*BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y + BAR_HEIGHT - fill, BAR_LENGTH, fill)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def remove_fishing_sys(): #a
    all_sprites.remove(water)
    all_sprites.remove(bar)
    all_sprites.remove(fish)
    bars.remove(bar)
    fishs.remove(fish)

def show_text(surf, text, size, x , y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)

#物件區
class Water(pygame.sprite.Sprite):  #藍條
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((65,660))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 250 + 23
        self.rect.y = 120
        
class Fish(pygame.sprite.Sprite): #釣魚系統的魚 #a2
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fishing_bar, (65,65))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(0, -40) #a
        #pygame.draw.rect(self.image, RED, self.rect) #a:碰撞框顯示
        self.rect.x = 250 + 23
        self.rect.y = 710
        self.speed = 1
        self.next_pos = self.rect.y
        
    def update(self):
        if self.rect.y < self.next_pos:    #上下浮動
            if (self.next_pos - self.rect.y) >= self.speed:
                self.rect.y += self.speed
            else:
                self.rect.y += self.next_pos - self.rect.y
        elif self.rect.y > self.next_pos:
            if (self.rect.y - self.next_pos) >= self.speed:
                self.rect.y -= self.speed
            else:
                self.rect.y -= self.rect.y - self.next_pos
                
        if self.rect.top < 120:     #邊界規範
            self.rect.top = 120
        if self.rect.bottom > 780:
            self.rect.bottom = 780
            
    def move(self):
        self.next_pos = random.randrange(120, 780 - self.rect.height)
        self.speed = random.randrange(2,6)
         
class Bar(pygame.sprite.Sprite):    #綠條
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((65,150))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 250 + 23
        self.rect.y = 680
        self.get_down = 3.5
        self.hp = 25
        
    def update(self):
        self.rect.y += self.get_down #自由下沉
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]: #綠條上升
             self.rect.y -= 9
        
        if self.rect.top < 120:     #邊界規範
            self.rect.top = 120
        if self.rect.bottom > 780:
            self.rect.bottom = 780   

class Fish_bag(pygame.sprite.Sprite):   #b
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.anchovy = 0
        self.octopus = 0
        self.radioactive_carp = 0
        self.sea_cucumber = 0
        
    def update(self):
        self.show_bag()
        show_text(screen, str(self.octopus), 35, 75, 15)
        show_text(screen, str(self.anchovy), 35, 75, 65)
        show_text(screen, str(self.radioactive_carp), 35, 75, 120)
        show_text(screen, str(self.sea_cucumber), 35, 75, 175)
            
    def show_bag(self):
        screen.blit(octopus, (10,10))
        screen.blit(anchovy, (10,65))
        screen.blit(radioactive_carp, (10,115))
        screen.blit(sea_cucumber, (10,170))

#---------------------------------------------chang
class Player(pygame.sprite.Sprite):  # 玩家 CHANG
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 100), pygame.SRCALPHA) #a
        self.image.fill(pygame.Color(255, 0, 255, 0)) #a
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 + 108
        self.rect.y = HEIGHT // 2 + 35
        self.out = False
        self.line_length = 50
        self.line_end = None
        self.inWater = False

    def update(self):
        key_pressed = pygame.key.get_pressed()
        # if key pressed, throw the fish rod
        if key_pressed[pygame.K_UP]:
            if not fishCaught.hit and not fishCaught.delayCheck:
                self.out = True
                # draw the fishing line
                self.line_end = (
                    self.rect.centerx + self.line_length / 2,
                    self.rect.centery + self.line_length,
                )
                self.line_length += 10
                if self.line_length > 180:
                    self.line_length = 180
    
    #a2:刪除goFishing

    def stopFishing(self):
        self.out = False
        self.inWater = False
        self.line_end = None
        self.line_length = 50
        fishing_line.kill()
        bobble.kill()
        fishCaught.kill()
        
class Bobble(pygame.sprite.Sprite):  # 浮標 CHANG
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.color = RED
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self, line_end):
        self.rect.center = line_end

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (self.rect.centerx, self.rect.centery), self.radius
        )
        
class FishCaught(pygame.sprite.Sprite):  # 被釣到的魚 CHANG
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set fish's info
        self.name = "fish"
        self.weight = 10
        self.length = 1.5
        self.chance = 100
        #-------------------new
        self.passTime = 0
        self.startTime = 0
        self.delayCheck = False
        #------------------leaf #a
        self.hit = False
        self.bite_sound = True
        #------------------leaf #b
        self.show_which_fish = None

    def CheckOnHook(self, player, bobble, screen):
        # detect if the fish is caught
        if player.out:
            # use random to represent the chance that the fish got caught
            if self.chance != 1:
                self.chance = random.randint(1, 425)
            else:
                self.isCaught(bobble, screen)

    def isCaught(self, bobble, screen):
        # ------------------leaf #a
        if self.bite_sound == True:
            fish_bite.play()
            self.bite_sound = False
        if not self.delayCheck:
            self.startTime = pygame.time.get_ticks()
            self.delayCheck = True
        self.hit = True

        # count time passed since the fish is caught
        if self.hit:
            self.passTime = pygame.time.get_ticks()
            if ((self.passTime - self.startTime) // 1000) <= 1:
                # NEW FISH MESSAGE NEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGE
                showImage = pygame.image.load(
                    os.path.join("img", "fish_hit.png")
                ).convert()  # 抓到了!
                showImage.set_colorkey(WHITE)
                # rescale showImage to a smaller size
                scaled_Image = pygame.transform.scale(
                    showImage,
                    (
                        showImage.get_size()[0] // 2 + 60,
                        showImage.get_size()[1] // 2 + 70,
                    ),
                )
                screen.blit(scaled_Image, (400, 280))
                # update格式(text, x位置, y 位置, 字型大小)
                # NEW FISH MESSAGE NEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGE
            else:
                self.hit = False
    
    def randFish(self, fish_bag):
        randomFish = random.randrange(1, 201)
        if randomFish < 100:
            self.name = "Anchovy"
            fish_bag.anchovy += 1
            self.show_which_fish = anchovy_big
            #screen.blit(anchovy, (WIDTH // 2 + 108, HEIGHT // 2 -50))
        elif randomFish >= 100 and randomFish < 165:
            self.name = "Octopus"
            fish_bag.octopus += 1
            self.show_which_fish = octopus_big
        elif randomFish >= 165 and randomFish < 200:
            self.name = "Sea_Cucumber"
            fish_bag.sea_cucumber += 1
            self.show_which_fish = sea_cucumber_big
        else:
            self.name = "Radioactive_Carp"
            fish_bag.radioactive_carp += 1
            self.show_which_fish = radioactive_carp_big
        
class FishingLine(pygame.sprite.Sprite):  # 釣魚線 CHANG
    def __init__(self, player): 
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.color = BLACK
        self.start_pos = None
        self.end_pos = None

    def update(self):
        if self.player.out and self.player.line_end is not None:
            self.start_pos = self.player.rect.center
            self.end_pos = self.player.line_end

    def draw(self, screen):
        if self.start_pos is not None and self.end_pos is not None:
            pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 3)
            
# NEW FISH MESSAGE NEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGE
class Message(pygame.sprite.Sprite):  # 設計魚上鉤後的資料跳窗
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont(None, 100)
        self.text = ""
        self.color = YELLOW

    # method for printing out the message
    def update(self, text, x, y, text_size):
        self.text = text
        self.font = pygame.font.SysFont(None, text_size)
        self.image_text = self.font.render(self.text, True, self.color)
        screen.blit(self.image_text, (420 + x, 300 + y))


# NEW FISH MESSAGE NEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGENEW FISH MESSAGE

#物件加入
all_sprites = pygame.sprite.Group()
bars = pygame.sprite.Group()
fishs = pygame.sprite.Group()
pygame.mixer.music.play(-1)
fish_bag = Fish_bag()
#b
the_bag = pygame.sprite.Group()
the_bag.add(fish_bag)
#--------------------------------- chang #a2
player = Player()
fishCaught = FishCaught()
fishing_line = FishingLine(player)
bobble = Bobble()
all_sprites.add(player)

#遊戲迴圈開始
running = True
back_switch = 1
show_fish_start = None

#fish移動計時器
TIMER_EVENT = pygame.USEREVENT + 1
TIME_INTERVAL = random.randrange(750,3500)  # 0.75-3.5秒
pygame.time.set_timer(TIMER_EVENT, TIME_INTERVAL)

while running:
    clock.tick(FPS)
    #取得輸入
    stopDetect = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #------------------------------chang
            if event.key == pygame.K_DOWN:
                '''player.stopFishing()
                fishCaught.chance = 100'''
            #------------------------------leaf #a
                if fishCaught.hit == True:
                    if back_switch == 1:
                        back_switch = 2
                        water = Water()
                        fish = Fish()
                        bar = Bar()
                        all_sprites.add(water)
                        all_sprites.add(bar)
                        all_sprites.add(fish)
                        bars.add(bar)
                        fishs.add(fish)
                        bar.hp = 25
                        fish_hit.play()
                        #b
                        fish_line_sound.play(-1)
                        #----new chang
                        fishCaught.delayCheck = False
                        fishCaught.hit = False
                else:
                    fishCaught.delayCheck = False
                if back_switch == 1:
                    # NEWNEWNEWNEWNEWNEWNEWNEWEWN
                    player.stopFishing()
                    fishCaught.chance = 100
                    fishCaught.bite_sound = True
            
        elif event.type == TIMER_EVENT and back_switch == 2:
            TIME_INTERVAL = random.randrange(350,1500)  #魚改變位置的時間
            pygame.time.set_timer(TIMER_EVENT, TIME_INTERVAL)
            fish.move()
        #-----------------------------------------chang
        elif event.type == pygame.KEYUP and stopDetect:
            player.inWater = True
            stopDetect = False

    
    #更新遊戲
    all_sprites.update()
    fishing_line.update()
    get_point = pygame.sprite.groupcollide(bars, fishs, False, False)
    if back_switch == 2:
        if get_point:
            if bar.hp < 100:
                bar.hp += 0.25
            else:#a
                back_switch = 1
                fishCaught.hit = False
                remove_fishing_sys()
                #got_fish.play()
                fishCaught.bite_sound = True
                #--------------b leaf
                show_fish_start = pygame.time.get_ticks()
                #--------------b chang
                fishCaught.randFish(fish_bag)
                if fishCaught.show_which_fish == radioactive_carp_big: #b leaf:音效判斷
                    special.play()
                else:
                    got_fish.play()
                player.stopFishing()
                fishCaught.chance = 100
                fishCaught.delayCheck = False
                # NEWNEWNEWNEWNEWNEWNEWNEWEWN chang
                player.stopFishing()
                fishCaught.chance = 100
                fishCaught.delayCheck = False
        else:
            if bar.hp > 0:
                bar.hp -= 0.25
            else:#a
                back_switch = 1
                fishCaught.hit = False
                remove_fishing_sys()
                fish_escape.play()
                fishCaught.bite_sound = True
                # NEWNEWNEWNEWNEWNEWNEWNEWEWN
                player.stopFishing()
                fishCaught.chance = 100
                fishCaught.delayCheck = False
    
    #畫面顯示
    screen.fill(WHITE)
    if back_switch == 1:
        screen.blit(back_1, (0,0))
        #b
        fish_line_sound.stop()
    elif back_switch == 2:
        screen.blit(back_2, (0,0))
        draw_health(screen, bar.hp, 330 + 23, 120)
        all_sprites.draw(screen) #a
    the_bag.update()
    if fishCaught.show_which_fish is not None and show_fish_start is not None:
        show_fish_now = pygame.time.get_ticks()
        if (show_fish_now - show_fish_start) <= 2000:
            screen.blit(fishCaught.show_which_fish, (WIDTH // 2 + 185, HEIGHT // 2 - 125))
        else:
            show_fish_start = None
    #-------------------------------------chang
    # 判斷玩家拋餌
    if player.out: 
        fishing_line.draw(screen)
        bobble.update(player.line_end)
        bobble.draw(screen)
    # 判斷上鉤沒
    if player.out and player.inWater:
        fishCaught.CheckOnHook(player, bobble, screen)   
        
    pygame.display.update()
    
pygame.quit()