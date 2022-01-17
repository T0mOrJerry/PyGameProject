import pygame
import os
import sys
import shutil
import csv


def clear_copy():
    copy_level = os.listdir(f"all_levels/{cur_level[0]}")[1:]
    copy_level.sort(key=lambda x: int(x[-1]))
    for i in range(len(copy_level)):
        shutil.copy(f"all_levels/{cur_level[0]}/{copy_level[i]}", f'all_levels/Copy/{i + 1}')


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
others = pygame.sprite.Group()
numbers = pygame.sprite.Group()
monsters = pygame.sprite.Group()
co = pygame.sprite.Group()
men = pygame.sprite.Group()
dead = pygame.sprite.Group()
location = 'menu'
fps = 60
jump_height = 110
cur_level = (1, 1)
menu_page = 'all_levels/menu/menu_main'
level_money = 0
li = []
with open('all_levels/menu/info', 'rt', encoding='utf-8') as file:
    money = file.readline().rstrip()
with open('all_levels/menu/skins.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        li.append(row)
levels = []
with open('all_levels/menu/levels.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        levels.append(row)
trophies = []
with open('all_levels/menu/trophy.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        trophies.append(row)
clear_copy()


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
    for i in range(len(e)):
        for j in range(len(e[0])):
            if e[i][j] == "*":
                Brick(bricks, j * 80, i * 80 + 25)
            elif e[i][j] == "@":
                AnimatedSprite(prizes, coin_image, 10, 1, j, i)
            elif e[i][j] == "+":
                gear = Gear(others)
            elif e[i][j] in "123456":
                Skin(bricks, j * 80, i * 80 + 25, int(e[i][j]) - 1)
            elif e[i][j] in "lmhe":
                LevelBrick(bricks, j * 80, i * 80 + 25, e[i][j])
            elif e[i][j] == "s":
                Star(bricks, j * 80, i * 80 + 25)
            elif e[i][j] in "dbigp":
                Trophy(bricks, j * 80, i * 80 + 25, e[i][j])
            elif e[i][j] == "&":
                Blast(monsters, blast_image, 9, 9, j, i)


def kill_all():
    for i in bricks:
        i.kill()
    for i in prizes:
        i.kill()
    for i in others:
        i.kill()
    for i in monsters:
        i.kill()


def reload_level():
    global menu_page, level_money
    hero.rect.x = 40
    hero.rect.y = 500
    hero.right()
    kill_all()
    level_money = 0
    sky.image = load_image("sky_menu.png")
    load_level(menu_page)


def coins(screen):
    global text_w, text_h, money, level_money, location
    font = pygame.font.Font('Data/copperplategothic_bold.ttf', 68)
    if location == 'menu':
        with open('all_levels/menu/info', 'wt', encoding='utf-8') as file:
            print(money, file=file)
        text = font.render(f"{money}", True, (0, 0, 0))
    else:
        text = font.render(f"{level_money}", True, (0, 0, 0))
    text_x = 0
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    for i in co:
        i.kill()
    scm = SingleCoin(co)


def cost_print(screen, n, x, y, b):
    font = pygame.font.Font('Data/copperplategothic_bold.ttf', 40)
    if b:
        text = font.render(f"choose", True, (0, 135, 0))
        text_x = x - 120
    elif int(n) > int(money):
        text = font.render(f"{n}", True, (255, 0, 0))
        text_x = x - (80 - text.get_width()) - 45
    else:
        text = font.render(f"{n}", True, (0, 135, 0))
        text_x = x - (80 - text.get_width()) - 45
    text_y = y
    screen.blit(text, (text_x, text_y))


def death():
    global cur_level
    a = hero.image
    kill_all()
    hero.image = load_image('RIP.png')
    hero.image = pygame.transform.scale(hero.image, (80, 80))
    characters.draw(screen)
    pygame.display.flip()
    pygame.time.wait(1000)
    kill_all()
    load_level("all_levels/Copy/1")
    cur_level = (cur_level[0], 1)
    hero.image = a
    hero.rect.x = 0
    hero.rect.y = 500


class Sky(pygame.sprite.Sprite):
    image = load_image("sky_menu.png")

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


class Gear(pygame.sprite.Sprite):
    image = load_image("gear.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Gear.image
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(10 * 80, 4 * 80 + 25)
        self.mask = pygame.mask.from_surface(self.image)


class SingleCoin(pygame.sprite.Sprite):
    image = load_image("single_coin.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = SingleCoin.image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = text_w + 5
        self.rect.y = text_h - self.rect.height - 10
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

    def update(self, *args):
        global menu_page, location
        if location == 'menu':
            if pygame.sprite.collide_mask(self, hero) and menu_page != 'all_levels/menu/menu_level':
                menu_page = 'all_levels/menu/menu_level'
                reload_level()
        else:
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
        self.rect =self.rect.move(0, 500)
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
        global menu_page, location, cur_level
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
        if pygame.key.get_pressed()[pygame.K_LEFT] and not self.obstacle_on_the_left:
            self.left()
            self.vx = -2
        elif pygame.key.get_pressed()[pygame.K_RIGHT] and not self.obstacle_on_the_right:
            self.right()
            self.vx = 2
        if args and args[0].type == pygame.KEYDOWN:
            if args and args[0].key == pygame.K_SPACE or args[0].key == pygame.K_UP:
                if self.obstacle_below:
                    if not self.jump:
                        self.finish_point = self.rect.y - jump_height
                        self.first_jump = True
                        self.up = True
                    self.jump = True
        if location == 'menu':
            if self.rect.x <= 1 and menu_page != 'all_levels/menu/menu_main':
                menu_page = 'all_levels/menu/menu_main'
                reload_level()
            if self.rect.x <= 1 and menu_page == 'all_levels/menu/menu_main':
                if self.vx < 0:
                    self.vx = 0
            if self.right_bottom_x >= width and menu_page == 'all_levels/menu/menu_main':
                if self.vx > 0:
                    self.vx = 0
            if self.rect.x >= width:
                menu_page = 'all_levels/menu/menu_main'
                reload_level()
        else:
            if self.right_bottom_x >= width:
                cur_level = (cur_level[0], cur_level[1] + 1)
                full_levelname = os.path.join(f'all_levels/Copy', f'{cur_level[1]}')
                if not os.path.isfile(full_levelname):
                    # Здесь можно закончить уровень и вывести итоги
                    self.rect.x = width - self.rect.width
                    cur_level = (cur_level[0], cur_level[1] - 1)
                else:
                    self.rect.x = 0
                    kill_all()
                    load_level(full_levelname)
            if self.rect.x < 0:
                if cur_level[1] > 1:
                    cur_level = (cur_level[0], cur_level[1] - 1)
                    full_levelname = os.path.join(f'all_levels/Copy', f'{cur_level[1]}')
                    kill_all()
                    self.rect.x = width - self.rect.width
                    load_level(full_levelname)
                else:
                    self.rect.x = 0
                    self.vx = 0
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
        self.pos_x = y
        self.pos_y = x
        self.pause = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        global menu_page, location, level_money
        if location == 'menu':
            if not self.fps:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                mask = pygame.mask.from_surface(self.image)
                if pygame.sprite.collide_mask(self, hero):
                    menu_page = 'all_levels/menu/menu_shop'
                    reload_level()
                    sky.image = load_image("sky.png")
            self.fps = (self.fps + 1) % self.max_fps
        else:
            if not self.fps:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.collide_mask(self, hero):
                level_money += 1
                self.kill()
                ##########
                with open("all_levels/menu/info", "r") as f:
                    money = int(f.readline())
                with open("all_levels/menu/info", "w") as f:
                    print(money + 1, file=f)
                with open(f"all_levels/Copy/{cur_level[1]}", "r") as file:
                    lvl_c = file.readlines()
                st = lvl_c.pop(self.pos_x)
                st = st[:self.pos_y] + "." + st[(self.pos_y + 1):]
                lvl_c.insert(self.pos_x, st)
                with open(f"all_levels/Copy/{cur_level[1]}", "w") as file:
                    for i in lvl_c:
                        file.write(i)
        self.fps = (self.fps + 1) % self.max_fps


class Skin(pygame.sprite.Sprite):

    def __init__(self, group, x, y, n):
        super().__init__(group)
        self.number = n
        self.a = str(li[self.number][3])
        self.image = load_image(self.a, -1)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.cost = li[self.number][2]
        self.bought = int(li[self.number][1])
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height


    def update(self, *args):
        global money
        cost_print(screen, self.cost, self.right_bottom_x, self.right_bottom_y, self.bought)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos[0], args[0].pos[1]):
                if self.bought:
                    hero.image = load_image(self.a, -1)
                    hero.image = pygame.transform.scale(self.image, (80, 80))
                elif int(money) >= int(self.cost):
                    li[self.number][1] = 1
                    self.bought = 1
                    money = int(money) - int(self.cost)
                    coins(screen)
                    with open('all_levels/menu/skins.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(
                            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for i in li:
                            writer.writerow(i)


class LevelBrick(pygame.sprite.Sprite):

    def __init__(self, group, x, y, n):
        super().__init__(group)
        if n == 'l':
            self.a = 0
        elif n == 'm':
            self.a = 1
        elif n == 'h':
            self.a = 2
        else:
            self.a = 3
        self.page = levels[self.a]
        self.image = load_image(self.page[2], -1)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height


    def update(self, *args):
        global menu_page, location, cur_level
        if pygame.sprite.collide_mask(self, hero):
            kill_all()
            location = 'level'
            hero.rect.x = 0
            hero.rect.y = 400
            cur_level = (int(self.page[1]), 1)
            sky.image = load_image("sky.png")
            menu_icon = MenuIcon(men)
            level_money = 0
            clear_copy()
            load_level(f'all_levels/Copy/{cur_level[1]}')


class MenuIcon(pygame.sprite.Sprite):
    image = load_image('menu_brick.png', -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = MenuIcon.image
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.width
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height


    def update(self, *args):
        global menu_page, location
        if location != 'menu':
            if args and args[0].type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(args[0].pos[0], args[0].pos[1]):
                    menu_page = 'all_levels/menu/menu_level'
                    location = 'menu'
                    self.kill()
                    reload_level()


class Blast(AnimatedSprite):
    def update(self):
        global cur_level
        self.max_fps = fps // 30
        if self.cur_frame == 80 and self.pause < 50:
            self.pause += 1
        else:
            if not self.fps:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                if pygame.sprite.collide_mask(self, hero):
                    death()
            self.fps = (self.fps + 1) % self.max_fps
            self.pause = 0


class Star(pygame.sprite.Sprite):
    image = load_image("star.png", -1)

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Star.image
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height

    def update(self, *args):
        global menu_page
        if pygame.sprite.collide_mask(self, hero):
            menu_page = 'all_levels/menu/menu_trophies'
            reload_level()


class Trophy(pygame.sprite.Sprite):

    def __init__(self, group, x, y, n):
        super().__init__(group)
        if n == 'd':
            self.a = 0
        elif n == 'b':
            self.a = 1
        elif n == 'i':
            self.a = 2
        elif n == 'g':
            self.a = 3
        else:
            self.a = 4
        self.page = trophies[self.a]
        self.image = load_image(self.page[2], -1)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.mask = pygame.mask.from_surface(self.image)
        self.left_up_x = self.rect.x
        self.left_up_y = self.rect.y
        self.right_bottom_x = self.rect.x + self.rect.width
        self.right_bottom_y = self.rect.y + self.rect.height


    def update(self, *args):
        global menu_page, location, cur_level
        if pygame.sprite.collide_mask(self, hero) and self.a != 0:
            full_levelname = os.path.join(f'all_levels/', f'{cur_level[0]}/level{cur_level[0]}.{cur_level[1]}')


if __name__ == '__main__':
    try:
        running = True
        coin_image = load_image("coin.png", -1)
        coin_image = pygame.transform.scale(coin_image, (880, 80))
        blast_image = load_image("blast2.png", -1)
        blast_image = pygame.transform.scale(blast_image, (720, 720))
        clock = pygame.time.Clock()
        ground = Ground(grounds)
        hero = Hero(characters)
        #number = Numbers(numbers)
        #############
        load_level(menu_page)
        #load_level(f'all_levels/Copy/{cur_level[1]}')
        sky = Sky(backgrounds)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        for i in characters:
                            i.update(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in bricks:
                        i.update(event)
                    if location == 'level':
                        for i in men:
                            i.update(event)
            screen.fill((255, 255, 255))
            backgrounds.draw(screen)
            grounds.draw(screen)
            numbers.draw(screen)
            characters.draw(screen)
            characters.update()
            prizes.draw(screen)
            monsters.draw(screen)
            monsters.update()
            prizes.update()
            co.draw(screen)
            coins(screen)
            if location == 'menu':
                others.draw(screen)
                others.update()
            men.draw(screen)
            bricks.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
    except ValueError:
        print("Неправильный формат ввода")

