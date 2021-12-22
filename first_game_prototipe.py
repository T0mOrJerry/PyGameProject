import pygame
import os
import sys

size = width, height = 900, 600
pygame.init()
pygame.display.set_caption('Window')
screen = pygame.display.set_mode(size)
fps = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('Textures', name)
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


class Floor(pygame.sprite.Sprite):
    image = load_image("ground.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Floor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self, group):
        super().__init__(group)
        self.speed_x = 0
        self.speed_y = 10
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.collide_mask(self, ground):
            self.rect = self.rect.move(0, 1)



if __name__ == '__main__':
    screen.fill((255, 255, 255))
    running = True
    clock = pygame.time.Clock()
    structure_objects = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    ground = Floor(structure_objects)
    hero = Hero(characters)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        structure_objects.draw(screen)
        characters.draw(screen)
        characters.update()
        pygame.display.flip()
        clock.tick(fps)