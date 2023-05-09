import pygame
from pygame.locals import *
import random
import math
from tkinter import messagebox as mbox
from pygame import mixer
import asyncio

class CarGame:
    def __init__(self):
        pygame.init()
        mixer.init()
        mixer.music.load('song.wav')
        #Set preferred volume
        mixer.music.set_volume(0.2)

        #Play the music
        mixer.music.play()


        #relative size of the window
        self.size = self.width, self.height = (1000, 1000)
        self.position = (self.width / 2, self.height / 2)

        #road
        self.road_w = int(self.width / 1.6)
        self.roadmark_w = int(self.width / 80)

        #Lane
        self.right_lane = (self.width / 2 + self.road_w / 4)
        self.left_lane = (self.width / 2 - self.road_w / 4)

        #Speeds, Counter
        self.speed = 1
        #pygame.init()
        self.running = True
    

        #Window Size
        self.screen = pygame.display.set_mode(self.size)

        #Drawing
        pygame.display.set_caption("Nayan\'s Car Game")
        self.screen.fill((0,102,0))
        pygame.display.update()

        self.car = pygame.image.load("ownCar.png")
        self.car_location = self.car.get_rect()
        self.car_location.center = (self.right_lane), self.height * 0.8

        self.car2 = pygame.image.load("enemyCar.png")
        self.car2_location = self.car2.get_rect()
        self.car2_location.center = (self.left_lane), self.height * 0.2

        self.game_font = pygame.font.Font("freesansbold.ttf", 21)
        self.game_font2 = pygame.font.Font("freesansbold.ttf", 18)
        self.game_font3 = pygame.font.Font("freesansbold.ttf", 18)

        self.counter = 0
        self.score = 0
        
        self.create_button()
        self.runGame()

    def create_button(self):
            button_width = 100
            button_height = 50
            button_color = (178,34,34)
            text_color = (30,30,30)
            font_size = 18
            font = pygame.font.Font("freesansbold.ttf", font_size)
            self.button_rect = pygame.Rect(10, 10, button_width, button_height)
            pygame.draw.rect(self.screen, button_color, self.button_rect)
            mute_icon = pygame.image.load("mute.png").convert_alpha()
            mute_icon = pygame.transform.scale(mute_icon, (18, 18))
            self.screen.blit(font.render(f'Mute', True, text_color), (self.button_rect.x + 30, self.button_rect.y + 30))
            self.screen.blit(mute_icon, (self.button_rect.x + 10, self.button_rect.y + 30))

    def toggle_music_volume(self):
        font_size = 18
        font = pygame.font.Font("freesansbold.ttf", font_size)
        text_color = (30, 30, 30)
        if mixer.music.get_volume() > 0:
            mixer.music.set_volume(0)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.button_rect.x, self.button_rect.y, self.button_rect.w, self.button_rect.h))
            unmute_icon = pygame.image.load("unmute.png").convert_alpha()
            unmute_icon = pygame.transform.scale(unmute_icon, (18, 18))
            self.screen.blit(font.render("Unmute", True, text_color), (self.button_rect.x + 30, self.button_rect.y + 30))
            self.screen.blit(unmute_icon, (self.button_rect.x + 10, self.button_rect.y + 30))
            
        else:
            mixer.music.set_volume(0.2)
            pygame.draw.rect(self.screen, (178,34,34), (self.button_rect.x, self.button_rect.y, self.button_rect.w, self.button_rect.h))
            mute_icon = pygame.image.load("mute.png").convert_alpha()
            mute_icon = pygame.transform.scale(mute_icon, (18, 18))
            self.screen.blit(font.render(f'Mute', True, text_color), (self.button_rect.x + 30, self.button_rect.y + 30))
            self.screen.blit(mute_icon, (self.button_rect.x + 10, self.button_rect.y + 30))
        
    async def runGame(self):
        while self.running:
            
            self.counter += 1
            self.draw_game()
            self.time_remaining = ((5000 - self.counter) / 1000) + 1  # add 1 to make sure it never displays as 0
            self.remaining_text = self.game_font2.render(f"Next Level in : {self.time_remaining:.2f}", False, (255,255,255))
            self.screen.blit(self.remaining_text, (10, 10))
            #level Up
            if self.counter == 5000:
                self.speed += 0.30
                self.counter = 0
                
            #ENEMY VECHICE
            self.car2_location[1]+= self.speed
        
            if self.car2_location[1]>self.height:
                self.score +=1
                if random.randint(0,1)==0:
                    self.car2_location.center = self.right_lane, -200
                else:
                    self.car2_location.center = self.left_lane, -200


            #END GAME CONDITION
            if self.car_location[0] == self.car2_location[0] and self.car2_location[1]>self.car_location[1] -250:
                
                self.choice = mbox.askretrycancel("Game Over", f"Your Score : {self.score}\n\nLevel: {math.ceil(self.speed)}\n\nWould you like to retry?")
                
                if self.choice:
                  
                    self.car_location.center = (self.right_lane),self.height*0.8
                    self.car2_location.center = (self.left_lane),self.height*0.2
                    self.speed = 1
                    self.counter = 0
                    self.score=0
                    
                else:
                    self.running = False
                    break
                    
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running=False
                
                if event.type==KEYDOWN:
                    if event.key in [K_a,K_LEFT]:
                        left_edge = (self.width/2-self.road_w/2+self.roadmark_w*2,0,self.roadmark_w,self.height)
                        self.car_location = self.car_location.move([-int(self.road_w/2),0])
                        if (self.car_location<left_edge):
                            self.car_location = self.car_location.move([int(self.road_w/2),0])
                    
                    if event.key in [K_d,K_RIGHT]:
                        right_edge = (self.width/2+self.road_w/2-self.roadmark_w*3,0,self.roadmark_w,self.height)
                        self.car_location = self.car_location.move([int(self.road_w/2),0])
                        if (self.car_location>right_edge):
                            self.car_location = self.car_location.move([-int(self.road_w/2),0])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.toggle_music_volume()

            self.draw_pavement()
            
            await asyncio.sleep(0)
            

        pygame.quit()

    def draw_game(self):
        
        game_text = self.game_font.render(f"Speed: {self.speed:.2f}", False, (255, 145, 0))
        game_text2 = self.game_font2.render(f"Level: {math.ceil(self.speed)}", False, (0, 251, 255))
        game_text3 = self.game_font3.render(f" Score: {self.score}", False, (50, 50, 50))

        # remove previous text location
        self.screen.fill((0, 102, 0), (820, 10, 150, 25))
        self.screen.fill((0, 102, 0), (820, 40, 150, 25))
        self.screen.fill((255, 200, 0), (820, 70, 150, 25))

        # blit updated text
        self.screen.blit(game_text, (820, 10))
        self.screen.blit(game_text2, (820, 40))
        self.screen.blit(game_text3, (820, 70))

        self.screen.fill((0, 102, 0), (10, 10, 250, 25))
        
        

       
        
    def draw_pavement(self):
            #Road 
            pygame.draw.rect(
                self.screen,
                (30, 30, 30),
                (self.width/2-self.road_w/2, 0, self.road_w, self.height)
            )
            #yellow mid line
            pygame.draw.rect(
                self.screen,
                (255, 240, 60),
                (self.width/2-self.roadmark_w/2,0,self.roadmark_w,self.height)
            )

            #white side line

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (self.width/2-self.road_w/2+self.roadmark_w*2,0,self.roadmark_w,self.height)
            )

            #white side line
            pygame.draw.rect(
                self.screen,
                (255,255,255),
                (self.width/2+self.road_w/2-self.roadmark_w*3,0,self.roadmark_w,self.height)
            )
            self.screen.blit(self.car,self.car_location)
            self.screen.blit(self.car2,self.car2_location)
            pygame.display.update()
            
            
        

if __name__ == "__main__":
    app = CarGame()
    asyncio.run(app.runGame())