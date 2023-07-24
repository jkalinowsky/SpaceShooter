import os
import random
import pygame
import asyncio

pygame.font.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SpaceShooter')

# load assets
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))
# ships
player_img = pygame.image.load(os.path.join("assets", "space_ship.png"))
green_img = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'enemy_ship_green.png')), 180)
red_img = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'enemy_ship_red.png')), 180)
# lasers
yellow_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))
green_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
red_laser = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
# obstacles
meteorite = pygame.image.load(os.path.join('assets', 'meteorite.png'))
# explosions
explosions = [pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion1.png')), (60, 60)),
              pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion2.png')), (60, 60)),
              pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion3.png')), (60, 60))]


# classes

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def p_draw(self, window):
        window.blit(self.img, (self.x - 20, self.y - 40))

    def e_draw(self, window):
        window.blit(self.img, (self.x - 20, self.y + 40))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not height > self.y > 0

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.counter = 0
        self.velocity = 1

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 100
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_img
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs, obst):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 100
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                for obs in obst:
                    if laser.collision(obs):
                        self.lasers.remove(laser)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.p_draw(window)


class Enemy(Ship):
    color_map = {
        'red': (red_img, red_laser),
        'green': (green_img, green_laser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel_y, vel_x):
        self.y += self.velocity
        # self.x += vel_x

    def draw(self, window):

        for laser in self.lasers:
            laser.e_draw(window)
        if self.health != 0:
            window.blit(self.ship_img, (self.x, self.y))


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = meteorite
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.img.get_width()

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


async def main():
    run = True

    lost = False
    lost_count = 0

    fps = 60
    lives = 5
    level = 0
    main_font = pygame.font.SysFont('comics', 50)
    lost_font = pygame.font.SysFont('comics', 60)

    enemies = []
    obstacles = []
    wave_length = 5
    enemy_vel = 1
    obs_vel = 2

    p_laser_vel = 15
    e_laser_vel = 8

    player_velocity = 10

    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        screen.blit(background, (0, 0))
        # draw lives
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255))
        screen.blit(lives_label, lives_label.get_rect(center=(WIDTH // 2, 30)))
        levels_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))
        screen.blit(levels_label, levels_label.get_rect(center=(WIDTH // 2, 70)))

        for en in enemies:
            en.draw(screen)
            if en.health == 0:
                en.velocity = 0
                if 0 <= en.counter < 9:
                    screen.blit(explosions[0], (en.x, en.y))
                if 9 <= en.counter < 18:
                    screen.blit(explosions[1], (en.x, en.y))
                if 18 <= en.counter < 27:
                    screen.blit(explosions[2], (en.x, en.y))
                en.counter += 1
                if en.counter == 27:
                    enemies.remove(en)
                    en.counter = 0

        for obs in obstacles:
            obs.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render('You lost!', 1, (255, 255, 255))
            screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(fps)

        redraw_window()

        if player.health == 0:
            lives -= 1
            player.health += 100

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 50), random.randrange(-1500, -100),
                              random.choice(['red', 'green']))
                enemies.append(enemy)
            for i in range(random.randrange(1, wave_length)):
                obstacle = Obstacle(random.randrange(50, WIDTH - 50), random.randrange(-3000, -100))
                obstacles.append(obstacle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel, 0)
            enemy.move_lasers(e_laser_vel, player)
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                lives -= 1
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        for obstacle in obstacles[:]:
            obstacle.move(obs_vel)

            if collide(obstacle, player):
                lives -= 1
                obstacles.remove(obstacle)
            if obstacle.y + obstacle.get_height() > HEIGHT:
                obstacles.remove(obstacle)

        player.move_lasers(-p_laser_vel, enemies, obstacles)

        await asyncio.sleep(0)  # Very important, and keep it 0


asyncio.run(main())
