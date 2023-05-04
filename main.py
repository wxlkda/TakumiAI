import pygame, sys, os, neat, math

from pygame.locals import *
from constants import *
from dino import *

import random

class Game:
    def __init__(self):
        pygame.init() #intiailize pygame and the pygame.mixer()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #intiaiize the window and set a caption for it
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock() #intiaiize thee  clock
        self.state = 'main_menu'
        self.player = Dinosaur()
        self.game_speed = 25
        self.points = 0
        self.obstacles = []
        self.obstacle_positions = []
        self.circle_cache = {}
        self.death_count = 0
        self.trees = [i *  self.resize_image(f"{os.path.dirname(__file__)}/Assets/Images/trees.png", (0.8, 0.8)).get_width() for i in range(3)]
        self.selected = "play"
        self.players = []
        self.ge = []
        self.nets = []
        self.pop = None

    def start(self):
        while True:
            if self.state == 'play':
                self.play_update()
                self.play_draw()
                self.play_events()
            if self.state == "main_menu":
                self.main_update()
                self.main_draw()
                self.main_events()
            if self.state == "game_over":
                self.over_update()
                self.over_draw()
                self.over_events()
            if self.state == "train":
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, 'config.txt')
                self.run(config_path)



    def create_obstacles(self):
        if self.obstacles == []:
            self.obstacles.append(3)
            self.obstacle_positions.append(WIDTH)

    def draw_score(self):
        self.points += 0.1
        if round(self.points, 2) % 100 == 0.0 and self.points > 0:
            self.game_speed += 1
        self.draw_text("Assets/Fonts/nokiafc22.ttf", 20, "Score: " + str(int(self.points)).zfill(4), WHITE, 105 - 23, 15)

    def draw_trees(self, speed = 1.5):
        self.animate_image((speed), f"{os.path.dirname(__file__)}/Assets/Images/trees.png", 93, (0.8, 0.8), self.trees)

    def draw_environment(self):
        self.screen.fill(BG)
        floor = pygame.Rect(0, 350, WIDTH, HEIGHT - 350)
        pygame.draw.rect(self.screen, FLOOR, floor)

    def draw_obstacles(self):
        for i in range(len(self.obstacles)):
            resized_image = self.resize_image(f"{os.path.dirname(__file__)}/Assets/Objects/Stones/{self.obstacles[i]}.png", (1.5,1.5))
            image_rect = resized_image.get_rect()
            image_rect.bottom = 369
            image_rect.x = self.obstacle_positions[i]
            self.screen.blit(resized_image, (image_rect.x, image_rect.y))
            if self.player.rect.colliderect(image_rect):
                self.state = "game_over"

    def play_draw(self):
        self.draw_environment()
        self.draw_trees()
        self.draw_obstacles()
        self.player.draw(self.screen)
        self.draw_score()

    def play_update(self):
        self.player.update(pygame.key.get_pressed())
        self.draw_score()
        self.create_obstacles()
        self.update_obstacles()

    def play_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        self.clock.tick(FPS)

    def over_draw(self):
        self.screen.fill(BG)
        self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 20, "Score: " + str(int(self.points)).zfill(4), BLACK, WIDTH / 2, HEIGHT / 2 - 30)
        self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 20, "u ded", BLACK, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 20, "gonna fix this soon", BLACK, WIDTH / 2, HEIGHT / 2 + 30)
        self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 20, "space to go back to the main menu", BLACK, WIDTH / 2, HEIGHT / 2 + 60)

    def over_update(self):
        pass

    def over_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    Game().start()
        pygame.display.update()
        self.clock.tick(FPS)

    def update_obstacles(self):
        for i in range(len(self.obstacle_positions)):
            self.obstacle_positions[i] -= self.game_speed / 3
            if self.obstacle_positions[i] < 0:
                self.obstacles.pop()
                self.obstacle_positions.pop()
                self.obstacles.append(random.randint(3,5))
                self.obstacle_positions.append(WIDTH)

    def main_update(self):
        self.player.update()

    def main_draw(self):
        self.draw_environment()
        self.draw_trees(0)
        self.draw_image(f"{os.path.dirname(__file__)}/Assets/Images/logo.png", (0.5, 0.5), WIDTH / 2, HEIGHT / 2 - 110)
        if self.selected == "play":
            self.render('Play', pygame.font.Font(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf",32), (94,194,223,255), (0,0,0), WIDTH / 2 - 1, HEIGHT / 2 - 7, 3)
            self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 32, "Train", (94,194,223,255), WIDTH / 2 - 1, HEIGHT / 2 + 57)
            self.draw_image(f"{os.path.dirname(__file__)}/Assets/Images/arrow.png", (0.1, 0.1),300, HEIGHT / 2 - 10)
        elif self.selected == "train":
            self.render('Train', pygame.font.Font(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf",32), (94,194,223,255), (0,0,0), WIDTH / 2 - 1, HEIGHT / 2 + 57, 3)
            self.draw_text(f"{os.path.dirname(__file__)}/Assets/Fonts/nokiafc22.ttf", 32, "Play", (94,194,223,255), WIDTH / 2 - 1, HEIGHT / 2 - 7)
            self.draw_image(f"{os.path.dirname(__file__)}/Assets/Images/arrow.png", (0.1, 0.1), 295, HEIGHT / 2 + 55)
        self.player.draw(self.screen)

    def main_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_DOWN:
                    self.selected = "play" if self.selected == "train" else "train"
                if event.key == K_RETURN:
                    self.state = self.selected
        pygame.display.update()
        self.clock.tick(FPS)

    def eval_genomes(self, genomes, config):
        self.points = 0
        self.trees = [i *  self.resize_image(f"{os.path.dirname(__file__)}/Assets/Images/trees.png", (0.8, 0.8)).get_width() for i in range(3)]
        for genome_id, genome in genomes:
            self.players.append(Dinosaur())
            self.ge.append(genome)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            genome.fitness = 0


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_environment()
            self.draw_trees()
            self.points += 0.2
            if round(self.points, 2) % 100 == 0.0 and self.points > 0:
                self.game_speed += 1
            self.draw_text("Assets/Fonts/nokiafc22.ttf", 20, "Score: " + str(int(self.points)).zfill(4), WHITE, 105 - 23, 15)
            self.draw_text("Assets/Fonts/nokiafc22.ttf", 20, "Generation: " + f"{self.pop.generation+1}", WHITE, 260, 15)
            self.draw_text("Assets/Fonts/nokiafc22.ttf", 20, "Players alive: " + f"{len(self.players)}", WHITE, 470, 15)
            self.draw_text("Assets/Fonts/nokiafc22.ttf", 20, "Speed: " + f"{self.game_speed}", WHITE, 650, 15)

            for player in self.players:
                player.update(pygame.key.get_pressed())
                player.draw(self.screen)

            if len(self.players) == 0:
                break

            self.create_obstacles()
            for i in range(len(self.obstacles)):
                resized_image = self.resize_image(f"{os.path.dirname(__file__)}/Assets/Objects/Stones/{self.obstacles[i]}.png", (1.5,1.5))
                image_rect = resized_image.get_rect()
                image_rect.bottom = 369
                image_rect.x = self.obstacle_positions[i]
                self.screen.blit(resized_image, (image_rect.x, image_rect.y))

                for i, dinosaur in enumerate(self.players):
                    if dinosaur.rect.colliderect(image_rect):
                        self.ge[i].fitness -= 1
                        self.players.pop(i)
                        self.ge.pop(i)
                        self.nets.pop(i)

                for i in range(len(self.obstacle_positions)):
                    self.obstacle_positions[i] -= self.game_speed / 3
                    if self.obstacle_positions[i] < 0:
                        self.obstacles.pop()
                        self.obstacle_positions.pop()
                        self.obstacles.append(random.randint(3,5))
                        self.obstacle_positions.append(WIDTH)

            for i, dinosaur in enumerate(self.players):
                dx = (dinosaur.rect.x)-image_rect.midtop[0]
                dy = dinosaur.rect.y-image_rect.midtop[1]
                distance = math.sqrt(dx**2+dy**2)
                output = self.nets[i].activate((dinosaur.rect.y, distance))
                if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                    dinosaur.dino_run = False
                    dinosaur.dino_jump = True

            self.clock.tick(FPS)
            pygame.display.update()

    def draw_image(self, image, scaling, xpos, ypos):
        image_obj = self.resize_image(image, (scaling[0], scaling[1]))
        img_rect = image_obj.get_rect()
        img_rect.center = (xpos, ypos)
        self.screen.blit(image_obj, (img_rect.x, img_rect.y))

    def draw_text(self, font, size, text, color, xpos, ypos): #method to display text on the screen
        font = pygame.font.Font(font,size) #creates the Font object
        text = font.render(text, True, color) #renders the font in pygam.e, returns a text object
        textRect = text.get_rect() #get the rect of the Text object
        textRect.center = (xpos, ypos) #center the rect given the x and y position passed into the params
        self.screen.blit(text, textRect) #blit the textRect onto the screen
        return textRect

    def animate_image(self, offset, image, original_y_pos, scaling, background_positions):
        if scaling != None:
            image = self.resize_image(image, (scaling[0], scaling[1]))
        for i in range(len(background_positions)):
            self.screen.blit(image, (background_positions[i], original_y_pos))
            background_positions[i] -= (offset)
            if background_positions[i] <= -image.get_width() + (offset):
                background_positions[i] = image.get_width() * (len(background_positions) - 1) - (offset)

    def resize_image(self, image, scaling):
        image = pygame.image.load(image)
        return pygame.transform.scale(image, (image.get_width() * scaling[0], image.get_height() * scaling[1]))

    def circle_points(self, r):
        r = int(round(r))
        if r in self.circle_cache:
            return self.circle_cache[r]
        x, y, e = r, 0, 1 - r
        self.circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def render(self, text, font, gfcolor, ocolor, xpos, ypos, opx=2):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self.circle_points(opx):
            surf.blit(osurf, (dx + opx, dy + opx))


        surf.blit(textsurface, (opx, opx))
        surfRect = surf.get_rect()
        surfRect.center = (xpos, ypos)
        self.screen.blit(surf, surfRect)
        return surf

    def run(self, config_path):
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

        self.pop = neat.Population(config)
        self.pop.run(self.eval_genomes, 50)

if __name__ == "__main__":
    Game().start()
