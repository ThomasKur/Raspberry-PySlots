#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Written by Balázs Nagy <nxbalazs@gmail.com>
# Design by Ferenc Nagy <nferencfx@gmail.com>
# Project web site: http://bfruit.sf.net

import pygame
import pygame.camera
from pygame.locals import *
from random import randrange
import sys
from sys import argv
from getopt import getopt, GetoptError
import RPi.GPIO as GPIO ## Import GPIO library for Raspberry Pi
import time
import os

VERSION = "0.1.2"



GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(37, GPIO.OUT) ## Setup GPIO Pin 37 to OUT
GPIO.setup(38, GPIO.OUT) ## Setup GPIO Pin 38 to OUT
GPIO.setup(40, GPIO.OUT) ## Setup GPIO Pin 38 to OUT

# main menu###########################
class Menu:
    def __init__(self):
        self.screen = screen
        self.maincolor = [0, 0, 0]
        self.white = [255, 255, 255]
        self.red = [255, 0, 0]
        self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
        
        self.backgroundadded = pygame.image.load("data/menubg/backgroundMenu.png")
        
        GPIO.output(37,False) 
        GPIO.output(38,True)
        GPIO.output(40,True)
        # mainloop
        while True:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    exit()
                if self.event.type == pygame.KEYDOWN:
                    self.bsound.play()
                    if self.event.key == pygame.K_LEFT:
                        plc = Game()
                    if self.event.key == pygame.K_ESCAPE:
                        GPIO.cleanup()
                        exit()
            # 1st layer: background color
            self.screen.fill(self.maincolor)
            
            self.screen.blit(self.backgroundadded, (0, 0))
            # 3rd layer: transparent image
           
            font = pygame.font.Font("data/BRISTRT0.TTF", 100)
            text_surface = font.render("Start Game" , True, self.red)
            self.screen.blit(text_surface, (300, 600))
            font=pygame.font.Font("data/LiberationSans-Regular.ttf", 25)
            text_surface = font.render("Current Highscore: "+scr, True, self.white)
            self.screen.blit(text_surface, (300, 800))

            pygame.display.update()

# main menu###########################

class EndGame:
    def __init__(self, credits):
        self.screen = screen
        self.maincolor = [0, 0, 0]
        self.white = [255, 255, 255]
        self.red = [255, 0, 0]
        self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
        self.winsound = pygame.mixer.Sound("data/sounds/Win.WAV")
        self.gameoversound = pygame.mixer.Sound("data/sounds/GameOver.WAV")
        self.CentralScreen = [460,340]
        GPIO.output(37,True) 
        GPIO.output(38,True)
        GPIO.output(40,True)
        
        
        # 1st layer: background color
        self.screen.fill(self.maincolor)
        
        # 3rd layer: transparent image
        
        scrb = int(scr)
        self.creditsb = int(credits)
        if self.creditsb > scrb:
            self.winsound.play()
            font = pygame.font.Font("data/BRISTRT0.TTF", 130)
            text_surface = font.render("You have a new high score!!! Press start to continue.", True, [255, 0, 0])
            self.screen.blit(text_surface, self.CentralScreen)

            text_surface = font.render("Old high score: "+scr, True, [255, 255, 255])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 200
            self.screen.blit(text_surface, textpos)

            text_surface = font.render("New high score: "+str(credits), True, [255, 255, 255])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 300
            self.screen.blit(text_surface, textpos)
            self.NewHighscoreLedOn()
            self.writehs(myhsfile)
        elif self.creditsb == 0:
            self.gameoversound.play()
            font = pygame.font.Font("data/BRISTRT0.TTF", 130)
            text_surface = font.render("Looser", True, [255, 0, 0])

            self.screen.blit(text_surface, self.CentralScreen)

            font = pygame.font.Font("data/BRISTRT0.TTF", 60)
            text_surface = font.render("You ended the game with 0 points...press start to continue.", True, [255, 0, 0])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 200
            self.screen.blit(text_surface, textpos)
            
        else:
            font = pygame.font.Font("data/BRISTRT0.TTF", 130)
            text_surface = font.render("Game Over", True, [255, 0, 0])

            self.screen.blit(text_surface, self.CentralScreen)

            font = pygame.font.Font("data/BRISTRT0.TTF", 60)
            text_surface = font.render("You ended the game, but you don't have a new high score...press start to continue.", True, [255, 0, 0])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 200
            self.screen.blit(text_surface, textpos)

            text_surface = font.render("High score: "+scr, True, [255, 255, 255])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 300
            self.screen.blit(text_surface, textpos)

            text_surface = font.render("Your score: "+str(credits), True, [255, 255, 255])
            textpos = self.CentralScreen
            textpos[1] = textpos[1] + 400
            self.screen.blit(text_surface, textpos)
        
        pygame.display.update()

        # mainloop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.NewHighscoreLedOff()
                plc = Menu()

    def writehs(self, myhsfile):
        writef = open(myhsfile, "w")
        writef.write(str(self.creditsb))
        writef.close()

    def NewHighscoreLedOn (self):
        GPIO.output(37,False) 
        GPIO.output(38,False)
        GPIO.output(40,False)

    def NewHighscoreLedOff (self):
        GPIO.output(37,True) ## Set on GPIO pin 37 Low
        GPIO.output(38,True)
        GPIO.output(40,True)       

# the game###########################
class Game:
    def __init__(self):
        self.mut = 0
        self.wins = [0, 0, 0, 0, 0]
        self.WinPoints = [0, 1, 1, 2, 2,3,3,4,5]
        self.keys = 1
        self.credit = 20
        self.bet = 1
        self.lastwin = 0
        self.show = []
        self.SlotPosition = [250,40]
        self.SlotItemSize = [330,330]
        self.SlotColumnSpace = 8
        self.StatisticPosition = [1450,300]
        self.StatisitcRowSpace = 60
        self.StatisitcFontSize = 50
        self.CHeckLineWidth = 20
        
        self.screen = screen
        
        self.bsound = pygame.mixer.Sound("data/sounds/CLICK10A.WAV")
        self.rasound = pygame.mixer.Sound("data/sounds/film_projector.wav")
        self.rbsound = pygame.mixer.Sound("data/sounds/film_projector.wav")
        self.rcsound = pygame.mixer.Sound("data/sounds/film_projector.wav")
 
        self.beepsound = pygame.mixer.Sound("data/sounds/beep.wav")
        self.background = pygame.image.load("data/img/bg.png")
        self.windowlayer = pygame.image.load("data/img/windowlayer.png")
        self.imgone = pygame.image.load("data/img/1.png")
        self.imgtwo = pygame.image.load("data/img/2.png")
        self.imgthree = pygame.image.load("data/img/3.png")
        self.imgfour = pygame.image.load("data/img/4.png")
        self.imgfive = pygame.image.load("data/img/5.png")
        self.imgsix = pygame.image.load("data/img/6.png")
        self.imgseven = pygame.image.load("data/img/7.png")
        self.imgeight = pygame.image.load("data/img/8.png")
        
        img = []
        img.append(self.imgone)
        img.append(self.imgtwo)
        img.append(self.imgthree)
        img.append(self.imgfour)
        img.append(self.imgfive)
        img.append(self.imgsix)
        img.append(self.imgseven)
        img.append(self.imgeight)
        self.RunningLedOff()
        self.randi()
        self.drawl()
        # mainloop
        while True:
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    self.WinnerLedOff() #sets RasPi GPIO Pin26 to low
                    self.bsound.play()
                    if event.key == pygame.K_LEFT and self.keys == 1:
                        if self.credit > 0:
                            self.RunningLedOn()
                            if self.credit - self.bet < 0:
                                self.bet = self.credit
                            self.credit = self.credit - self.bet
                            self.randi()
                            self.roll(img)
                            self.check()
                            self.screen.blit(self.background, (0, 0))
                            self.drawl()
                            self.RunningLedOff()
                            self.winner()
                        elif self.credit == 0 and self.bet == 0:
                            plc = Menu()
                            
                    if self.credit > 0:
                        if event.key == pygame.K_UP and self.keys == 1:
                            if self.credit - self.bet - 1 >= 0:
                                self.bet = self.bet + 1
                            else:
                                self.bet = 1
                            if self.bet == 11:
                                self.bet = 1
                            
                    else:
                        self.bet = 0
                            
                            
                    if event.key == pygame.K_F1:
                        if self.keys == 1:
                            self.keys = 0
                            self.menu = "h"
                        elif self.keys == 0:
                            self.keys = 1
                            self.menu = "n"
                            
                    if event.key == pygame.K_RETURN:
                        self.keys = 0
                        self.menu = "e"
                      
                    if event.key == pygame.K_ESCAPE and self.keys == 1:
                        plc = Menu()
                            
            self.draw_side()
            
            if self.mut == 1:
                self.drawl()
                self.check()
                self.wins = [0, 0, 0, 0, 0]

            self.draw_rlayer()
            self.screen.blit(self.windowlayer, (0, 0))

            if self.credit == 0 and self.bet == 0:
                self.endthegame(scr, self.credit)
                
            
            if self.keys == 0 and self.menu == "h":
                self.helpmenu()
            if self.keys == 0 and self.menu == "e":
                self.endthegame(self.credit)
            
            pygame.display.update()
    
    def roll(self, img):
        szam = 0
        
        
        # toll time
        rolla = randrange(5, 14)
        rollb = randrange(rolla+1, rolla+5)
        rollc = randrange(rollb+1, rollb+5)
        
        # a column
        rollaf = []
        rollaf.append(img[int(self.show[0])-1])
        rollaf.append(img[int(self.show[1])-1])
        rollaf.append(img[int(self.show[2])-1])
        while szam <= rolla-3:
            rollaf.append(img[randrange(0, 8)])
            szam = szam + 1
        self.rasound.play()
        rollaf.append(img[int(self.showold[0])-1])
        rollaf.append(img[int(self.showold[1])-1])
        rollaf.append(img[int(self.showold[2])-1])
        
            
        szam = 0
        
        # b column
        rollbf = []
        rollbf.append(img[int(self.show[3])-1])
        rollbf.append(img[int(self.show[4])-1])
        rollbf.append(img[int(self.show[5])-1])
        while szam <= rollb-3:
            rollbf.append(img[randrange(0, 8)])
            szam = szam +1
        self.rbsound.play()
        rollbf.append(img[int(self.showold[3])-1])
        rollbf.append(img[int(self.showold[4])-1])
        rollbf.append(img[int(self.showold[5])-1])
            
        szam = 0
        
        # c column
        rollcf = []
        rollcf.append(img[int(self.show[6])-1])
        rollcf.append(img[int(self.show[7])-1])
        rollcf.append(img[int(self.show[8])-1])
        while szam <= rollc-3:
            rollcf.append(img[randrange(0, 8)])
            szam = szam +1
        self.rcsound.play()
        rollcf.append(img[int(self.showold[6])-1])
        rollcf.append(img[int(self.showold[7])-1])
        rollcf.append(img[int(self.showold[8])-1])
        
        szama = len(rollaf)-1
        szamb = len(rollbf)-1
        szamc = len(rollcf)-1
        
        while szamc > 2:
            self.screen.fill([0, 0, 0])
            self.screen.blit(self.background, (0, 0))
            
            if szama > 2:
                self.screen.blit(rollaf[len(rollaf)-3], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
                szama = szama - 1
                del(rollaf[len(rollaf)-1])
            else:
                self.screen.blit(rollaf[len(rollaf)-3], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.SlotPosition[0]+ self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
                self.rasound.stop()
                
            if szamb > 2:
                self.screen.blit(rollbf[len(rollbf)-3], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
                szamb = szamb - 1
                del(rollbf[len(rollbf)-1])
            else:
                self.screen.blit(rollbf[len(rollbf)-3], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.SlotPosition[0] + self.SlotItemSize[0] + 3 * self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
                self.rbsound.stop()
                
            if szamc > 2:
                self.screen.blit(rollcf[len(rollcf)-3], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
                szamc = szamc - 1
                del(rollcf[len(rollcf)-1])
            else:
                self.screen.blit(rollcf[len(rollcf)-3], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
            
            self.draw_side()
            
            self.draw_rlayer()
            
            self.screen.blit(self.windowlayer, (0, 0))
            pygame.display.update()
            rollc = rollc - 1
        self.rcsound.stop()
    
    def draw_rlayer(self):
        print("SkipDrawLayer")
        #pygame.draw.line(self.screen, [0, 0, 0], (self.SlotPosition[0], self.SlotPosition[1] + (0.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (0.5 * self.SlotItemSize[1])), 4)
        #pygame.draw.line(self.screen, [0, 0, 0], (self.SlotPosition[0], self.SlotPosition[1] + (1.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (1.5 * self.SlotItemSize[1])), 4)
        #pygame.draw.line(self.screen, [0, 0, 0], (self.SlotPosition[0], self.SlotPosition[1] + (2.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (2.5 * self.SlotItemSize[1])), 4)
        #pygame.draw.line(self.screen, [0, 0, 0], self.SlotPosition, (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (3 * self.SlotItemSize[1])), 4)
        #pygame.draw.line(self.screen, [0, 0, 0], (self.SlotPosition[0], self.SlotPosition[1] + (3 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1]), 4)

    def draw_side(self):
        #Bet
        font = pygame.font.Font("data/LiberationSans-Regular.ttf", 30)
        text_surface = font.render("Bet:", True, [230, 255, 255])
        self.screen.blit(text_surface, self.StatisticPosition)
        
        digifont = pygame.font.Font("data/DIGITAL2.ttf",self.StatisitcFontSize)
        text_surface = digifont.render(str(self.bet), True, [255, 0, 0])
        self.screen.blit(text_surface, (self.StatisticPosition[0], self.StatisticPosition[1] + self.StatisitcRowSpace))
        
        # last win
        font = pygame.font.Font("data/LiberationSans-Regular.ttf", 30)
        text_surface = font.render("Winner Points:", True, [230, 255, 255])
        self.screen.blit(text_surface, (self.StatisticPosition[0], self.StatisticPosition[1] + 3 * self.StatisitcRowSpace))
        
        digifont = pygame.font.Font("data/DIGITAL2.ttf",self.StatisitcFontSize)
        text_surface = digifont.render(str(self.lastwin), True, [255, 0, 0])
        self.screen.blit(text_surface, (self.StatisticPosition[0], self.StatisticPosition[1] + 4 * self.StatisitcRowSpace))
        
        font = pygame.font.Font("data/LiberationSans-Regular.ttf", 30)
        text_surface = font.render("Credit:", True, [230, 255, 255])
        self.screen.blit(text_surface, (self.StatisticPosition[0], self.StatisticPosition[1] + 6 * self.StatisitcRowSpace))
        # startsum
        digifont = pygame.font.Font("data/DIGITAL2.ttf",self.StatisitcFontSize)
        text_surface = digifont.render(str(self.credit), True, [255, 0, 0])
        self.screen.blit(text_surface, (self.StatisticPosition[0], self.StatisticPosition[1] + 7 * self.StatisitcRowSpace))
    
    def drawl(self):        
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[0])+".png"), (self.SlotPosition[0] + self.SlotColumnSpace, self.SlotPosition[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[1])+".png"), (self.SlotPosition[0] + self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[2])+".png"), (self.SlotPosition[0] + self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[3])+".png"), (self.SlotPosition[0] + self.SlotItemSize[0] + 3* self.SlotColumnSpace, self.SlotPosition[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[4])+".png"), (self.SlotPosition[0] + self.SlotItemSize[0] + 3* self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[5])+".png"), (self.SlotPosition[0] + self.SlotItemSize[0] + 3* self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[6])+".png"), (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[7])+".png"), (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + self.SlotItemSize[1]))
        self.screen.blit(pygame.image.load("data/img/"+str(self.show[8])+".png"), (self.SlotPosition[0] + 2 * self.SlotItemSize[0] + 4 * self.SlotColumnSpace, self.SlotPosition[1] + (2*self.SlotItemSize[1])))

    # random images
    def randi(self):
        self.showold = []
        if len(self.show) > 1:
            self.showold = self.show
        else:
            self.showold = ["8", "8", "8", "8", "8", "8", "8", "8", "8"]
        self.mut = 1
        ran = {}
        ran[0] = randrange(1, 335)
        ran[1] = randrange(1, 335)
        ran[2] = randrange(1, 335)
        ran[3] = randrange(1, 335)
        ran[4] = randrange(1, 335)
        ran[5] = randrange(1, 335)
        ran[6] = randrange(1, 335)
        ran[7] = randrange(1, 335)
        ran[8] = randrange(1, 335)
        self.show = []
        for n in ran:
            if 1 <= ran[n] <= 5:
                self.show.append("8")
            if 6 <= ran[n] <= 15:
                self.show.append("7")
            if 16 <= ran[n] <= 30:
                self.show.append("6")
            if 31 <= ran[n] <= 50:
                self.show.append("5")
            if 51 <= ran[n] <= 120:
                self.show.append("4")
            if 121 <= ran[n] <= 180:
                self.show.append("3")
            if 181 <= ran[n] <= 253:
                self.show.append("2")
            if 254 <= ran[n] <= 334:
                self.show.append("1")
                
    def check(self):
        self.wins = [0, 0, 0, 0, 0]
        if self.show[0] == self.show[3] == self.show[6]:
            pygame.draw.line(self.screen, [246, 226, 0], (self.SlotPosition[0], self.SlotPosition[1] + (0.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (0.5 * self.SlotItemSize[1])), self.CHeckLineWidth)
            self.wins[0] = self.show[0]
        if self.show[1] == self.show[4] == self.show[7]:
            pygame.draw.line(self.screen, [246, 226, 0], (self.SlotPosition[0], self.SlotPosition[1] + (1.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (1.5 * self.SlotItemSize[1])), self.CHeckLineWidth)
            self.wins[1] = self.show[1]
        if self.show[2] == self.show[5] == self.show[8]:
            pygame.draw.line(self.screen, [246, 226, 0], (self.SlotPosition[0], self.SlotPosition[1] + (2.5 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (2.5 * self.SlotItemSize[1])), self.CHeckLineWidth)
            self.wins[2] = self.show[2]
        if self.show[0] == self.show[4] == self.show[8]:
            pygame.draw.line(self.screen, [246, 226, 0], self.SlotPosition, (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1] + (3 * self.SlotItemSize[1])), self.CHeckLineWidth)
            self.wins[3] = self.show[0]
        if self.show[2] == self.show[4] == self.show[6]:
            pygame.draw.line(self.screen, [246, 226, 0], (self.SlotPosition[0], self.SlotPosition[1] + (3 * self.SlotItemSize[1])), (self.SlotPosition[0] + (3 * self.SlotItemSize[0]) +( 2 *self.SlotColumnSpace), self.SlotPosition[1]), self.CHeckLineWidth)
            self.wins[4] = self.show[2]
            
    def winner(self):
        winsum = 0
        print(winsum)
        for n in self.wins:
            winsum = winsum + (self.bet * self.WinPoints[int(n)])
            print("n=" + str(n))
            print(self.WinPoints[int(n)])
        if winsum > 0:
            print(winsum)
            self.credit = self.credit + winsum
            self.lastwin = self.lastwin + winsum
            self.beepsound.play()
            self.WinnerLedOn() ## Set GPIO pin 26 High
            
    def WinnerLedOn (self):
        GPIO.output(37,False) 
        GPIO.output(38,False)
        GPIO.output(40,True)

    def WinnerLedOff (self):
        GPIO.output(37,True) ## Set on GPIO pin 37 Low
        GPIO.output(38,True)
        GPIO.output(40,True)

    def RunningLedOn (self):
        GPIO.output(37,False) 
        GPIO.output(38,True)
        GPIO.output(40,True)

    def RunningLedOff (self):
        GPIO.output(37,True) ## Set on GPIO pin 37 Low
        GPIO.output(38,True)
        GPIO.output(40,True)
    
    

    def helpmenu(self):
        pygame.draw.line(self.screen, [176, 176, 176], (50, 250), (590, 250), 400)
        font = pygame.font.Font("data/LiberationSans-Regular.ttf", 15)
        text_surface = font.render("How to play:", True, [255, 255, 255])
        self.screen.blit(text_surface, (60, 60))
        text_surface = font.render("New spin: left arrow", True, [255, 255, 255])
        self.screen.blit(text_surface, (60, 80))
        text_surface = font.render("Raise bet: arrow up", True, [255, 255, 255])
        self.screen.blit(text_surface, (60, 100))
        text_surface = font.render("To end game to high score press Enter", True, [255, 255, 255])
        self.screen.blit(text_surface, (60, 120))
        text_surface = font.render("To close this as game over help press F1", True, [255, 255, 255])
        self.screen.blit(text_surface, (60, 160))
        
    def endthegame(self, scr):
        plc = EndGame(scr,self.credit)
    
    
        

def help():
    print("BFruit help:")
    print("Options:")
    print("-h, --help        display this help message")
    print("-v, --version     display game version")
    print("Contact: nxbalazs@gmail.com")

if __name__ == "__main__":
    try:
        long = ["help", "version"]
        opts = getopt(argv[1:], "hv", long)[0]
    except GetoptError:
        help()
        exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            exit()
        if opt in ("-v", "--version"):
            print("BFruit - version: "+ VERSION)
            exit()
            

    # .settings:
    homedir = os.path.expanduser("~")
    if homedir[0] == "/":
        mydir = homedir+"/.bfruit"
        myhsfile = mydir+"/hs"
    else:
        mydir = homedir+"\Application Data\.bfruit"
        myhsfile = mydir+"\hs"
    if os.path.exists(mydir) == False:
        os.mkdir(mydir)
    if os.path.exists(myhsfile) == False:
        open(myhsfile, "w").close()
    hsf = open(myhsfile, "r+")
    scr = hsf.readline() # high score
    hsf.close()
    if scr == "":
        scr = "1"

    # pygame init, set display
    pygame.init()
    screen = pygame.display.set_mode([1920,1080])
    pygame.display.toggle_fullscreen()
    pygame.display.set_caption("Rocker Slot")
    pygame.mouse.set_visible(False)
        
    plc = Menu()
    pygame.display.update()
