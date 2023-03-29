'''
Nuh Aydoğdu -190316020
Sümer Can Ertuğral -190316004
Kadirhan Özen -190316042
Furkan Sert -190316060
'''

import math
from threading import Thread, Semaphore
import pygame
import random
import sys
import time


#This class is used to create an object that represents a piece of furniture that appears in the background of the game.
class BackgroundFurniture(pygame.sprite.Sprite):
    def __init__(self, image_file, location, scale_factor=1.0, horizontal_flip=False, vertical_flip=False):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.flip(self.image, horizontal_flip, vertical_flip)
        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale_factor),
                int(self.image.get_height() * scale_factor)
            )
        )
        self.rect = self.image.get_rect(center=location)

#This class is used to create an object that represents a chair that characters can sit on.
class Chair(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        self.rect = self.image.get_rect(center=location)

#This class is used to create an object that represents a character in the game. Each character has an ID, a state ID, a location, a direction, a moving flag, and a speed.
class Character(pygame.sprite.Sprite):
    def __init__(self, character_id, state_id, location):
        super().__init__()
        self.image = pygame.image.load("assets/characters.png")
        self.rect = self.image.get_rect(center=location)
        self.image = self.image.subsurface(pygame.Rect(abs(state_id)*16, character_id*16, 16, 16))
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        if state_id < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.direction = "right"
        self.moving = False
        self.speed = 5

#This class is used to create an object that represents text in the game. The text object has a string of text, a font, a text surface, and a text rectangle.
class Text:
    def __init__(self, text, location, font_size=25, font_color=(0, 0, 0)):
        self.text = text
        self.font = pygame.font.Font("assets/PressStart2P.ttf", font_size)
        self.text_surface = self.font.render(self.text, True, font_color)
        self.text_rect = self.text_surface.get_rect(center=location)

#This class is used to create an object that represents a meal in the game.The location is specified as a tuple of (x, y) coordinates, and the scale factor is used to specify the size of the meal.
class Meal(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load("assets/spaghetti_full.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1, self.image.get_height()*1))
        self.rect = self.image.get_rect(center=location)
        self.location = location
        self.scale = 1
#The update method is called to update the state of the Meal object. It decreases the value of the scale attribute by 1/7 and scales the image using the pygame.transform.
    def update(self):
        self.scale -= 0.5/7
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        pygame.Rect.move_ip(self.rect, +3, +3)


#This class is used to create an object that represents a chopstick in the game. The chopstick object has an image, a rectangle, and an angle.
class Chopstick(pygame.sprite.Sprite):
    def __init__(self, angle, location):
        super().__init__()
        self.image = pygame.image.load("assets/chopstick.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.3, self.image.get_height()*0.3))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=location)
        self.location = location
        self.angle = angle

    def update(self, state, event, philosopher):
        # If state is ' / ' and event is "T", the chopstick is moved upwards.
        if (state == ' /   ' and event == "T"):
            pygame.Rect.move_ip(self.rect, 0, -10)
            # If state is ' / \ ', the chopstick is moved upwards.
        elif (state == ' / \\ '):
            pygame.Rect.move_ip(self.rect, 0, -10)
            #If state is ' / ' and event is "L", the chopstick is moved downwards.
        elif (' /   ' and "L"):
            pygame.Rect.move_ip(self.rect, 0, +10)
            #Otherwise, the chopstick is moved downwards.
        else:
            pygame.Rect.move_ip(self.rect, 0, +10)





WIDTH = 800
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dining Philosophers")
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

background_group = pygame.sprite.Group()
background_group.add(
    [
        BackgroundFurniture("assets/floor.png", (x, y))
        for x in range(0, WIDTH+100, 62) for y in range(0, HEIGHT+100, 46)
    ]
)
background_group.add(BackgroundFurniture("assets/carpet.png", (WIDTH//2, HEIGHT//2), 12))
background_group.add(BackgroundFurniture("assets/fireplace.png", (WIDTH//2, 60), 4))
background_group.add(BackgroundFurniture("assets/music_player.png", (720, 90), 4))
background_group.add(BackgroundFurniture("assets/sofa_front.png", (560, 80), 4))
background_group.add(BackgroundFurniture("assets/sofa_single_right.png", (740, 200), 4))
background_group.add(BackgroundFurniture("assets/stairs.png", (700, 440), 4, True))
background_group.add(BackgroundFurniture("assets/desk.png", (170, 120), 3))
background_group.add(BackgroundFurniture("assets/table_horizontal.png", (WIDTH//2, HEIGHT//2), 4))

title_text = Text("Dining Philosophers", (WIDTH//2 - 100, HEIGHT - 50), 24, (200, 255, 200))

meal_0 = Meal((WIDTH//2 - 40, HEIGHT//2 - 50))
meal_1 = Meal((WIDTH//2 + 40, HEIGHT//2 - 50))
meal_2 = Meal((WIDTH//2 + 60, HEIGHT//2 - 15))
meal_3 = Meal((WIDTH//2 + 0, HEIGHT//2 - 10))
meal_4 = Meal((WIDTH//2 - 60, HEIGHT//2 - 15))
meal_group = pygame.sprite.Group()
meal_group.add([meal_0, meal_1, meal_2, meal_3, meal_4])
meals = [meal_0, meal_1, meal_2, meal_3, meal_4]


philosopher_group = pygame.sprite.Group()
chair_0 = Chair("assets/chair_front_2.png", (WIDTH//2 - 40, HEIGHT//2 - 110))
chair_1 = Chair("assets/chair_front_2.png", (WIDTH//2 + 40, HEIGHT//2 - 110))
chair_2 = Chair("assets/chair_right_2.png", (WIDTH//2 + 130, HEIGHT//2 - 10))
chair_3 = Chair("assets/chair_back_2.png", (WIDTH//2, HEIGHT//2 + 100))
chair_4 = Chair("assets/chair_left_2.png", (WIDTH//2 - 130, HEIGHT//2 - 10))
philosopher_0 = Character(3, 0, (WIDTH//2 + 10, HEIGHT//2 + 30))
philosopher_1 = Character(7, 0, (WIDTH//2 + 90, HEIGHT//2 + 30))
philosopher_2 = Character(10, -2, (WIDTH//2 + 160, HEIGHT//2 + 100))
philosopher_3 = Character(12, 1, (WIDTH//2 + 45, HEIGHT//2 + 180))
philosopher_4 = Character(8, 2, (WIDTH//2 - 65, HEIGHT//2 + 100))
chopstick_0 = Chopstick(225, (WIDTH//2 + 0, HEIGHT//2 - 60))
chopstick_1 = Chopstick(160, (WIDTH//2 + 55, HEIGHT//2 - 35))
chopstick_2 = Chopstick(75, (WIDTH//2 + 40, HEIGHT//2 + 10))
chopstick_3 = Chopstick(15, (WIDTH//2 - 40, HEIGHT//2 + 10))
chopstick_4 = Chopstick(290, (WIDTH//2 - 55, HEIGHT//2 - 35))
philosopher_group.add(
    [
        chair_0, chair_1, chair_2, chair_3, chair_4,
        philosopher_0, philosopher_1, philosopher_2, philosopher_3, philosopher_4,

        chopstick_0, chopstick_1, chopstick_2, chopstick_3, chopstick_4
    ]
)
chopsticks = [chopstick_0, chopstick_1, chopstick_2, chopstick_3, chopstick_4]



class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=7):
        #The semaphore is used to control access to the chopsticks
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        #[Semaphore(value=1) it means this resource(chopsticks) can only be use by one user one process(number_of_philosophers)
        #self.meals=[9,9,9,9,9,,,9] total index(n) number_of_philosophers
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        #The status list keeps track of the current status of each philosopher (either "T" for thinking or "E" for eating).
        self.status = ['  T  ' for _ in range(number_of_philosophers)]
        #The chopstick_holders list keeps track of which philosopher is holding each chopstick.
        self.chopstick_holders = ['     ' for _ in range(number_of_philosophers)]
        self.number_of_philosophers = number_of_philosophers

    def philosopher(self, i):
        j = (i+1) % self.number_of_philosophers
        #The method has a loop that continues as long as the philosopher has meals remaining.
        while self.meals[i] > 0:
            # the philosopher first updates their status to "T" (thinking) and sleeps for a random amount of time.
            self.status[i] = '  T  '
            time.sleep(1+ random.random())
            self.status[i] = '  _  '
            if self.chopsticks[i].acquire(timeout=1):
                # The philosopher tries to acquire a lock on the first chopstick by calling self.chopsticks[i].acquire(timeout=1).
                # If the lock is not available within 1 second, the method will return False and the philosopher will not be able to eat.
                self.chopstick_holders[i] = ' /   '

                chopsticks[i].update(' /   ', "T", i)
                time.sleep(random.random())
                if self.chopsticks[j].acquire(timeout=1):
                    #If the philosopher is able to acquire both locks, they update their status to "E" (eating), eat a meal, and release the locks on the chopsticks.
                    self.chopstick_holders[i] = ' / \\ '
                    chopsticks[j].update(' / \\ ', "T", i)
                    self.status[i] = '  E  '
                    meals[i].update()
                    time.sleep(random.random())
                    self.meals[i] -= 1  #yemeğinin bir kısmını yedi
                    self.chopsticks[j].release()
                    self.chopstick_holders[i] = ' /   '
                    chopsticks[j].update(' /   ', "L", i)
                self.chopsticks[i].release()
                self.chopstick_holders[i] = '     '
                chopsticks[i].update('     ', "L", i)
                self.status[i] = '  T  '


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    n = 5
    m = 7
    #The code first creates a DiningPhilosophers object and a list of Thread objects, each of which represents a philosopher in the simulation.
    # The philosophers are started by calling the start() method on each Thread object.
    dining_philosophers = DiningPhilosophers(n, m)
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)]
    for philosopher in philosophers:
        philosopher.start()
        #Inside the loop, the code updates the Pygame display, printing the status of the philosophers, the chopstick holders, and the number of meals remaining.
    while sum(dining_philosophers.meals) > 0:
        screen.fill((0, 0, 0))
        background_group.draw(screen)
        screen.blit(title_text.text_surface, title_text.text_rect)
        meal_group.draw(screen)
        philosopher_group.draw(screen)
        pygame.display.update()
        print("=" * (n * 5))
        print("".join(map(str, dining_philosophers.status)), " : ",
              str(dining_philosophers.status.count('  E  ')))
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print("".join("{:3d}  ".format(m) for m in dining_philosophers.meals), " : ",
              str(sum(dining_philosophers.meals)))
        time.sleep(0.1)
        pygame.display.update()
    for philosopher in philosophers:
        philosopher.join()
    break
    #When the loop ends (when all the meals have been eaten), the code calls the join() method on each philosopher
    # Thread object to wait for the threads to finish, and then breaks out of the loop.
    clock.tick(60)
