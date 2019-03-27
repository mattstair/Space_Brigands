import pygame
from os import path
import random
from settings import *
from RandomName import get_random_name
from utils import draw_text

vec = pygame.math.Vector2


class Tony(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 3
        game.all_sprites.add(self)
        self.game = game
        self.image = pygame.transform.scale(self.game.player_img, (64, 64))
        self.image.set_colorkey((20, 52, 100))
        self.fluff = False
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 25
        self.pos = vec(self.rect.topleft)
        self.vel = vec(0, 0)

    def update_size(self, size):
        midbottom = self.rect.midbottom

        if self.fluff:
            if size < 50:
                self.image = pygame.transform.scale(self.game.fluff_img, (64, 64))
            elif size < 75:
                self.image = pygame.transform.scale(self.game.fluff_img, (128, 128))
            elif size < 100:
                self.image = pygame.transform.scale(self.game.fluff_img, (256, 256))
            else:
                self.image = pygame.transform.scale(self.game.fluff_img, (512, 512))

        else:
            if size < 50:
                self.image = pygame.transform.scale(self.game.player_img, (64, 64))
            elif size < 75:
                self.image = pygame.transform.scale(self.game.player_img, (128, 128))
            elif size < 100:
                self.image = pygame.transform.scale(self.game.player_img, (256, 256))
            else:
                self.image = pygame.transform.scale(self.game.player_img, (512, 512))

            self.image.set_colorkey((20, 52, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom
        self.pos = vec(self.rect.topleft)
        self.vel = vec(0, 0)

    def update(self):
        self.vel.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -300
        if keys[pygame.K_RIGHT]:
            self.vel.x = 300
        self.pos.x += self.vel.x * self.game.dt
        self.rect.x = self.pos.x
        if self.pos.x < 0:
            self.pos.x = 0
            self.rect.x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.pos.x = self.rect.x


class Chair(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 2
        self.groups = game.all_sprites, game.chairs
        for group in self.groups:
            group.add(self)
        self.game = game
        self.size_factor = 0
        self.image = pygame.transform.scale(self.game.chair_img, (64, 64))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.game.tony.rect.midbottom

    def update(self):
        self.rect.midbottom = self.game.tony.rect.midbottom

    def update_size(self):
        if self.size_factor == 0:
            self.image = pygame.Surface((64, 64))
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
        else:
            new_size = (64 * self.size_factor, 64 * self.size_factor)
            self.image = pygame.transform.scale(self.game.chair_img, new_size)
            self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type, damage):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 3
        self.groups = game.all_sprites, game.all_bullets
        for group in self.groups:
            group.add(self)
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.pos = vec(self.rect.topleft)
        self.vel = vec(0, -500)
        self.type = type
        self.damage = damage

    def update(self):
        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = self.pos.y
        if self.rect.bottom < 0:
            self.kill()


class Person(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 3
        self.groups = game.all_sprites, game.all_people
        for group in self.groups:
            group.add(self)
        self.game = game
        self.type = random.choices(['nobody', 'small', 'medium', 'large', 'huge'], [100, 20, 10, 5, 1])[0]
        self.troll = random.choices([True, False], [1, 49])[0]
        self.orig_image = pygame.Surface((50, 50))
        if self.troll:
            self.orig_image.fill(GREEN)
        else:
            self.orig_image.fill(PURPLE)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = -10
        self.rect.centerx = random.randrange(self.rect.w / 2, SCREEN_WIDTH - self.rect.w / 2)
        self.pos = vec(self.rect.topleft)
        self.vel = vec(0, 50)
        self.progress = 0
        self.hit_tony = False
        self.generate()
        self.redraw()

    def generate(self):
        self.name = get_random_name()

        self.affinities = {}
        flavors = ['puns', 'swears', 'fake swears', 'catch phrase']
        for flavor in flavors:
            trend = self.game.affinity_trends[flavor]
            self.affinities[flavor] = random.choices([-1, 0, 1], [100-trend, 50, trend])[0]

        if self.type == 'nobody':
            self.sub_count = random.choice([0, 5])
            self.sub_text = str(self.sub_count)
            self.max_progress = 100
        elif self.type == 'small':
            self.sub_count = random.choice([25, 50])
            self.sub_text = str(self.sub_count)
            self.max_progress = 200
        elif self.type == 'medium':
            self.sub_count = random.choice([1000, 5000])
            d = {1000: '1 k', 5000: '5 k'}
            self.sub_text = d[self.sub_count]
            self.max_progress = 300
        elif self.type == 'large':
            self.sub_count = random.choice([10000, 50000])
            d = {10000: '10 k', 50000: '50 k'}
            self.sub_text = d[self.sub_count]
            self.max_progress = 500
        elif self.type == 'huge':
            self.sub_count = random.choices([1000000, 50000000], [19, 1])[0]
            d = {1000000: '1 mil', 50000000: '50 mil'}
            self.sub_text = d[self.sub_count]
            self.max_progress = 1000

        if self.troll:
            self.progress = -self.max_progress

    def hit(self, flavor, damage):
        progress = 0
        if self.troll and self.progress < 0:
            if flavor == 'ban':
                progress = self.max_progress
        else:
            if not self.troll:
                if flavor == 'ban':
                    progress = -1 * self.max_progress
                elif flavor == 'quality content':
                    progress = damage
                elif flavor == 'side job':
                    progress = -damage
                else:
                    progress = damage * self.affinities[flavor]

        self.progress += progress
        if self.progress > self.max_progress:
            self.progress = self.max_progress
        if self.progress < -self.max_progress:
            self.progress = -self.max_progress

        self.redraw()

    def die(self):
        death_message = ""
        prog_percent = self.progress / self.max_progress
        subs = self.game.subscribers
        sub_dif = 0
        if prog_percent >= 1:
            patron = random.choices([True, False], [1, 4])[0]
            if patron:
                death_message = "became a patron"
                self.game.patrons += 1
            else:
                death_message = "liked and subscribed"
            sub_dif = round(int(self.sub_count * 0.2) * self.game.eff_conversion_rate / 100)
            self.game.subscribers += 1
            if sub_dif > 0:
                self.game.subscribers += sub_dif
                death_message = "praised your channel! You got " + "{:,}".format(sub_dif) + " more subscribers"
            self.game.likes += 1
        elif prog_percent >= 0.5:
            death_message = "liked and subscribed"
            sub_dif = round(int(self.sub_count * 0.05) * self.game.eff_conversion_rate / 100)
            self.game.subscribers += 1
            if sub_dif > 0:
                self.game.subscribers += sub_dif
                death_message = "mentioned your channel! You got " + "{:,}".format(sub_dif) + " more subscribers"
            self.game.likes += 1
        elif prog_percent >= 0.2:
            self.game.likes += 1
            death_message = "liked your content"
        elif 0 > prog_percent > -0.5:
            self.game.likes -= 1
            death_message = "disliked your content"
        elif prog_percent <= -0.5:
            death_message = "disliked your content and unsubscribed"
            sub_dif = -int(self.sub_count * 0.05)
            self.game.subscribers -= 1
            if sub_dif < 0:
                self.game.subscribers += sub_dif
                death_message = death_message + ", convincing " + "{:,}".format(-sub_dif) + \
                                                " of your subscribers to unsubscribe from you"
            self.game.likes -= 1
        if len(death_message) > 0:
            self.game.log.add_text(self.name + " " + death_message)

        if subs == 0:
            subs = 1

        if abs(sub_dif) > 100:
            sub_rate = sub_dif / subs
            if sub_rate >= 1:
                self.game.ego_size += 100
            elif sub_rate >= .5:
                self.game.ego_size += 50
            elif sub_rate >= .1:
                self.game.ego_size += 10
            elif -.1 >= sub_rate > -.25:
                self.game.ego_size -= 10
            elif -.25 >= sub_rate > -.5:
                self.game.ego_size -= 50
            elif -.5 >= sub_rate:
                self.game.ego_size -= 100

            self.game.ego_size = max(0, min(100, self.game.ego_size))
            self.game.tony.update_size(self.game.ego_size)

    def redraw(self):
        prog_percent = self.progress / self.max_progress
        self.image = self.orig_image.copy()
        if self.progress != 0:
            if prog_percent >= 1:
                color = BLUE
            elif prog_percent >= 0.5:
                color = GREEN
            elif prog_percent >= 0.2:
                color = YELLOW
            elif prog_percent > 0:
                color = WHITE
            else:
                color = RED

            pygame.draw.rect(self.image, color, (0, 0, abs(prog_percent)*self.rect.w, 5))
        draw_text(self.image, self.sub_text, 20, alignment='center', x=self.rect.w/2, y=self.rect.h/2)

    def update(self):
        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = self.pos.y

        if self.rect.y > SCREEN_HEIGHT:
            self.die()
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 0
        self.groups = game.all_sprites, game.all_stars
        for group in self.groups:
            group.add(self)
        self.game = game
        self.closeness = random.choice([1, 2, 3])
        self.size = self.closeness
        self.twinkle = random.randrange(20, 230)
        self.twinkle_direction = random.choice([-20, 20])
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.image.set_alpha(self.twinkle)
        self.rect = self.image.get_rect()
        if x != 0 and y != 0:
            self.rect.topleft = (x, y)
        else:
            x_rand = random.randrange(0, SCREEN_WIDTH - self.size)
            y_rand = random.randrange(0, SCREEN_HEIGHT - self.size)
            self.rect.topleft = (x_rand, y_rand)
        self.pos = vec(self.rect.topleft)
        self.vel = vec(0, 0)
        if self.closeness == 1:
            self.vel.y = random.randrange(5.0, 10.0)
        elif self.closeness == 2:
            self.vel.y = random.randrange(10.0, 15.0)
        elif self.closeness == 3:
            self.vel.y = random.randrange(15.0, 20.0)

    def sparkle(self):
        if self.twinkle > 230:
            self.twinkle = 230
            self.twinkle_direction *= -1
        elif self.twinkle < 20:
            self.twinkle = 20
            self.twinkle_direction *= -1
        else:
            self.twinkle += self.twinkle_direction
        self.image.set_alpha(self.twinkle)

    def update(self):
        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = self.pos.y
        if self.rect.top > SCREEN_HEIGHT:
            rand_x = random.randrange(0, SCREEN_WIDTH - self.size)
            self.rect.topleft = (rand_x, -10)
            self.pos.y = self.rect.y



