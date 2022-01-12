import pygame
import os
import sys

size = width, height = 1280, 720
pygame.init()
pygame.display.set_caption('Window')
screen = pygame.display.set_mode(size)
fps = 200
jump_height = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Sky(pygame.sprite.Sprite):
    image = load_image("sky.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Sky.image
        self.rect = self.image.get_rect()


class Floor(pygame.sprite.Sprite):
    image = load_image("ground.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Brick(pygame.sprite.Sprite):
    image = load_image("brick_ground.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Brick.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def give_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self, group):
        super().__init__(group)
        self.jump = False
        self.jump_point = None
        self.first_jump = False
        self.speed_x = 0
        self.speed_y = 10
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.on_the_ground = False

    def update(self, *args):
        for i in structure_objects:
            if pygame.sprite.collide_mask(self, i):
                self.on_the_ground = True
                break
            else:
                self.on_the_ground = False

        if not self.on_the_ground:
            self.rect = self.rect.move(0, 1)
        if pygame.key.get_pressed()[pygame.K_LEFT] and 0 < self.rect.x:
            self.rect = self.rect.move(-1, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x + self.rect.width < width:
            self.rect = self.rect.move(1, 0)
        if args and args[0].type == pygame.KEYDOWN:
            if args and args[0].key == pygame.K_SPACE:
                print(1)
                if not self.jump:
                    self.finish_point = self.rect.y - jump_height
                    self.first_jump = True
                    self.up = True
                self.jump = True
                print(self.finish_point)
                print(self.rect.y)
        if self.jump:
            self.do_jump()

    def do_jump(self):
        if not self.on_the_ground or self.first_jump:
            self.first_jump = False
            if self.rect.y >= self.finish_point and self.up:

                self.rect = self.rect.move(0, -2)
                print(self.on_the_ground, self.rect.y)
            else:
                self.up = False
                print(3)
        else:
            self.jump = False






if __name__ == '__main__':
    screen.fill((255, 255, 255))
    running = True
    clock = pygame.time.Clock()
    structure_objects = pygame.sprite.Group()
    backgrounds = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    ground = Floor(structure_objects)
    sky = Sky(backgrounds)
    hero = Hero(characters)
    brick1 = Brick(structure_objects)
    brick1.give_coords(100, 200)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in characters:
                        i.update(event)
        screen.fill((255, 255, 255))
        backgrounds.draw(screen)
        structure_objects.draw(screen)
        characters.draw(screen)
        characters.update()

        pygame.display.flip()
        clock.tick(fps)