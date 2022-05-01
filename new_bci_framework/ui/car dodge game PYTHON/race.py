import pygame
import time
import random

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)

class CarRacer:
    def __init__(self):
        self.display_width = 800
        self.display_height = 600

        self.right_detected = False
        self.left_detected = False

        #self.crash_sound = pygame.mixer.Sound("crash.mp3")

        self.car_width = 55

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.display.set_caption('Car Dodge Game')
        self.clock = pygame.time.Clock()

        gameIcon = pygame.image.load('carIcon.png')
        pygame.display.set_icon(gameIcon)

        self.backgroundImage = pygame.image.load("background.png")
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (800, 600))
        self.gameDisplay.blit(self.backgroundImage, (0, 0))

        self.carImg = pygame.image.load("michael.png")
        self.carImg = pygame.transform.scale(self.carImg, (80, 80)) # resize graphic
        self.carImg = self.carImg.convert_alpha() # remove whitespace from graphic

        car1 = pygame.image.load("diablo.png")
        car1 = pygame.transform.scale(car1, (60, 100)) # resize graphic
        car1 = car1.convert_alpha() # remove whitespace from graphic

        car2 = pygame.image.load("aventador.png")
        car2 = pygame.transform.scale(car2, (60, 100)) # resize graphic
        car2 = car2.convert_alpha() # remove whitespace from graphic

        car3 = pygame.image.load("nsx.png")
        car3 = pygame.transform.scale(car3, (60, 100)) # resize graphic
        car3 = car3.convert_alpha() # remove whitespace from graphic

        car4 = pygame.image.load("speeder.png")
        car4 = pygame.transform.scale(car4, (60, 100)) # resize graphic
        car4 = car4.convert_alpha() # remove whitespace from graphic

        car5 = pygame.image.load("slr.png")
        car5 = pygame.transform.scale(car5, (60, 100)) # resize graphic
        car5 = car5.convert_alpha() # remove whitespace from graphic

        car6 = pygame.image.load("Mach6.png")
        car6 = pygame.transform.scale(car6, (60, 100)) # resize graphic
        car6 = car6.convert_alpha() # remove whitespace from graphic

        car7 = pygame.image.load("Stingray.png")
        car7 = pygame.transform.scale(car7, (60, 100)) # resize graphic
        car7 = car7.convert_alpha() # remove whitespace from graphic

        car8 = pygame.image.load("bike.png")
        car8 = pygame.transform.scale(car8, (60, 100)) # resize graphic
        car8 = car8.convert_alpha() # remove whitespace from graphic

        self.randomCars = [car1, car2, car3, car4, car5, car6, car7, car8]
        self.enemy = random.choice(self.randomCars)

        #brought to you by code-projects.org
        self.pause = False
        # crash = True
        self.run()


    def run(self):
        self.game_intro()
        self.game_loop()
        pygame.quit()
        quit()

    def score(self, count):
        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render("SCORE: " + str(count), True, red)
        self.gameDisplay.blit(text, (0, 0))


    def things(self, thingx, thingy, thingw, thingh, color, enemyC):
        #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
        self.gameDisplay.blit(enemy, [thingx, thingy, thingw, thingh])

    def car(self, x, y):
        self.gameDisplay.blit(self.carImg, (x, y))


    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()


    def crash(self):
        ####################################

        # pygame.mixer.Sound.play(self.crash_sound)
        pygame.mixer.music.stop()
        ####################################
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.text_objects("You Crashed", largeText)
        TextRect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(TextSurf, TextRect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.button("Play Again", 150, 450, 100, 50, green, bright_green, self.game_loop)
            self.button("Quit", 550, 450, 100, 50, red, bright_red, self.quitgame)

            pygame.display.update()
            self.clock.tick(15)


    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gameDisplay.blit(textSurf, textRect)


    def quitgame(self):
        pygame.quit()
        quit()


    def unpause(self):
        global pause
        pygame.mixer.music.unpause()
        pause = False


    def paused(self):
        ############
        pygame.mixer.music.pause()
        #############
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.text_objects("Paused", largeText)
        TextRect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(TextSurf, TextRect)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.button("Continue", 150, 450, 100, 50, green, bright_green, self.unpause)
            self.button("Quit", 550, 450, 100, 50, red, bright_red, self.quitgame)

            pygame.display.update()
            self.clock.tick(15)


    def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill(white)
            largeText = pygame.font.SysFont("comicsansms", 115)
            TextSurf, TextRect = self.text_objects("Car Dodge", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 4))
            self.gameDisplay.blit(TextSurf, TextRect)

            largeText = pygame.font.SysFont("comicsansms", 40)
            TextSurf, TextRect = self.text_objects("Think LEFT or RIGHT to move", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(TextSurf, TextRect)

            self.button("LET PLAY!", 150, 450, 100, 50, green, bright_green, self.game_loop)
            self.button("Quit", 550, 450, 100, 50, red, bright_red, self.quitgame)

            pygame.display.update()
            self.clock.tick(15)


    def game_loop(self):
        global pause, enemy
        enemy = random.choice(self.randomCars)
        ############

        pygame.mixer.music.load('bgmusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        ############
        x = (self.display_width * 0.45)
        y = (self.display_height * 0.8)

        x_change = 0

        thing_startx = random.randrange(0, self.display_width)
        thing_starty = -600
        enemy_speed = 4
        thing_width = 55
        thing_height = 95
        enemyC = random.choice(self.randomCars)
        thingCount = 1

        dodged = 0

        gameExit = False

        while not gameExit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    if event.key == pygame.K_RIGHT:
                        x_change = 5
                    if event.key == pygame.K_p:
                        pause = True
                        self.paused()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

            if self.right_detected:
                x_change = 5
                self.right_detected = False

            if self.left_detected:
                x_change = -5
                self.left_detected = False

            x += x_change

            self.gameDisplay.blit(self.backgroundImage, (0, 0))

            self.things(thing_startx, thing_starty, thing_width, thing_height, block_color, enemyC)

            thing_starty += enemy_speed
            self.car(x, y)
            self.score(dodged)

            if x > self.display_width - self.car_width or x < 0:
                self.crash()

            if thing_starty > self.display_height:
                thing_starty = 0 - thing_height
                thing_startx = random.randrange(0, self.display_width)
                dodged += 1
                #enemy_speed += .25
                if dodged % 5 == 0:
                    enemy_speed += (dodged * 1)


            if y < thing_starty + thing_height:
                #print('y crossover')

                if x > thing_startx and x < thing_startx + thing_width or x + self.car_width > thing_startx and x + self.car_width < thing_startx + thing_width:
                    #print('x crossover')
                    self.crash()

            pygame.display.update()
            self.clock.tick(60)

    def move_right(self):
        self.right_detected = True

    def move_left(self):
        self.left_detected = True

c = CarRacer()