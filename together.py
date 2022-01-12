import pygame
import os
import sys


pygame.init()
w, h = 1280, 720
size = width, height = w, h
pygame.display.set_caption('Game over')
screen = pygame.display.set_mode(size)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
characters = pygame.sprite.Group()
bricks = pygame.sprite.Group()
grounds = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
main = pygame.sprite.Group()
prizes = pygame.sprite.Group()
numbers = pygame.sprite.Group()
fps = 60
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


def load_level(name):
    e = []
    with open(name, 'rt', encoding="utf8") as level:
        rows = level.readlines()
        for i in rows:
            col = []
            for j in i[:-1]:
                col.append(j)
            e.append(col)
    return e


class Sky(pygame.sprite.Sprite):
    image = load_image("sky.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Sky.image
        self.rect = self.image.get_rect()


class Ground(pygame.sprite.Sprite):
    image = load_image("ground.png", -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Ground.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Brick(pygame.sprite.Sprite):
    image = load_image("brick.png", -1)

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Brick.image
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height

    def update(self):
        if pygame.sprite.collide_mask(self, hero):
            if self.left_up_y <= hero.right_bottom_y and self.left_up_y >= hero.left_up_y and \
                    (self.left_up_x - hero.rect.width + 7 < hero.left_up_x < self.right_bottom_x - 7):
                hero.obstacle_below = True
            if hero.left_up_y <= self.right_bottom_y and hero.right_bottom_y >= self.right_bottom_y and \
                    (self.left_up_x - hero.rect.width + 7 < hero.left_up_x < self.right_bottom_x - 7):
                hero.obstacle_above = True
            if hero.left_up_x <= self.right_bottom_x and hero.right_bottom_x >= self.right_bottom_x and \
                    (self.left_up_y - hero.rect.height + 7 < hero.left_up_y < self.right_bottom_y - 7):
                hero.obstacle_on_the_left = True
            if self.left_up_x <= hero.right_bottom_x and self.left_up_x >= hero.left_up_x and \
                    (self.left_up_y - hero.rect.height + 7 < hero.left_up_y < self.right_bottom_y - 7):
                hero.obstacle_on_the_right = True

    def give_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Border(pygame.sprite.Sprite):
    def __init__(self, group, x1, y1, x2, y2):
        super().__init__(group)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Hero(pygame.sprite.Sprite):
    image = load_image("mario.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Hero.image
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect =self.rect.move(0, 400)
        self.mask = pygame.mask.from_surface(self.image)
        self.vy = 1
        self.vx = 0
        self.flip = False
        self.jump = False
        self.jump_point = None
        self.first_jump = False
        self.left_border_colide = False
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height
        self.obstacle_below = False
        self.obstacle_on_the_left = False
        self.obstacle_on_the_right = False
        self.obstacle_above = False

    def left(self):
        if not self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = True

    def right(self):
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = False

    def update(self, *args):
        self.obstacle_below = False
        self.obstacle_on_the_left = False
        self.obstacle_on_the_right = False
        self.obstacle_above = False
        bricks.update()
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height
        self.vx = 0
        self.vy = 0
        if pygame.sprite.collide_mask(self, ground):
            self.obstacle_below = True
        if not self.obstacle_below:
            self.vy = 2
        if pygame.key.get_pressed()[pygame.K_LEFT] and 0 < self.rect.x and not self.obstacle_on_the_left:
            self.left()
            self.vx = -2
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not self.obstacle_on_the_right:
            self.right()
            self.vx = 2
        if args and args[0].type == pygame.KEYDOWN:
            if args and args[0].key == pygame.K_SPACE:
                if self.obstacle_below:
                    if not self.jump:
                        self.finish_point = self.rect.y - jump_height
                        self.first_jump = True
                        self.up = True
                    self.jump = True
        if self.jump:
            self.do_jump()
        self.rect = self.rect.move(self.vx, self.vy)

    def do_jump(self):
        if (not self.obstacle_below or self.first_jump) and not self.obstacle_above:
            self.first_jump = False
            if self.rect.y >= self.finish_point and self.up:
                self.vy = -3
            else:
                self.up = False
        else:
            self.jump = False


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, group, sheet: pygame.Surface, columns: int, rows: int, x: int, y: int):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(-7, 25)
        self.rect = self.rect.move(x * 80, y * 80)
        self.max_fps = fps // 10
        self.fps = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if not self.fps:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.collide_mask(self, hero):
                numbers.update()
                self.kill()
        self.fps = (self.fps + 1) % self.max_fps


class Numbers(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.frames = []
        temp_image = load_image("numbers.png", "white")
        temp_image = pygame.transform.scale(temp_image, (800, 80))
        self.cut_sheet(temp_image, 10, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    try:
        running = True
        coin_image = load_image("coin.png", -1)
        coin_image = pygame.transform.scale(coin_image, (880, 80))
        clock = pygame.time.Clock()
        ground = Ground(grounds)
        hero = Hero(characters)
        number = Numbers(numbers)
        level = load_level("level")
        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == "*":
                    Brick(bricks, j * 80, i * 80 + 25)
                if level[i][j] == "@":
                    coin = AnimatedSprite(prizes, coin_image, 10, 1, j, i)
        sky = Sky(backgrounds)
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
            grounds.draw(screen)
            numbers.draw(screen)
            characters.draw(screen)
            characters.update()
            prizes.draw(screen)
            prizes.update()
            bricks.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
    except ValueError:
        print("Неправильный формат ввода")


