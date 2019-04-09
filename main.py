import pygame
from os import path
import random
import copy
import math
from settings import *
from sprites import *
from utils import *
from scrollwindow import ScrollWindow


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = self.window.subsurface(((WINDOW_WIDTH - SCREEN_WIDTH) / 2, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Brigands!')
        self.clock = pygame.time.Clock()
        self.running = True
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.player_img = pygame.image.load(path.join(self.img_dir, 'LPWB.png')).convert()
        self.chair_img = pygame.image.load(path.join(self.img_dir, 'chair.png')).convert()
        self.fluff_img = pygame.image.load(path.join(self.img_dir, 'fluffinspace1.png')).convert_alpha()
        self.troll_img = pygame.image.load(path.join(self.img_dir, 'troll.png')).convert_alpha()
        self.weapons = copy.deepcopy(WEAPONS)
        self.weapons_unlocked = {'side job'}
        # self.weapons_unlocked = {weapon['name'] for weapon in self.weapons}
        self.weapon_index = 0
        self.fire_rate = self.weapons[self.weapon_index]['rate']
        self.last_shot = 0  # timer
        self.recent_shots = []  # history of recent shots
        self.burn_out = 0  # out of 100
        self.ego_size = 0  # out of 100
        self.days = 0
        self.likes = 0
        self.subscribers = 0
        self.fake_subscribers = 0
        self.patrons = 0
        self.cash = 0
        self.revenue = 0
        self.energy = 0
        self.max_energy = 0
        self.energy_bonus = 1.0
        self.eat_rate = 0
        self.conversion_rate = 10  # out of 100
        self.sketchiness = 0  # out of 100
        self.eff_conversion_rate = 10  # out of 100
        self.spawn_timer = 0.0
        self.sparkle_timer = 0
        self.update_timer = 0.0
        self.flash_timer = 0.0
        self.affinity_trends = {}
        self.analytics = False
        self.energy_flash = False
        self.paused = False
        self.upgrading = False

        self.icons = None
        self.upgrade_button_images = None
        self.pause_background = None
        self.pause_button_images = None
        self.load_images()

        self.pause_buttons = [
            Button(bg_img=self.pause_button_images['resume'], return_value='resume'),
            Button(bg_img=self.pause_button_images['upgrades'], return_value='upgrades'),
            Button(bg_img=self.pause_button_images['save'], return_value='save'),
            Button(bg_img=self.pause_button_images['retire'], return_value='retire'),
            Button(bg_img=self.pause_button_images['restart'], return_value='restart'),
            Button(bg_img=self.pause_button_images['quit'], return_value='quit')
        ]
        y = (SCREEN_HEIGHT - PAUSE_MENU_HEIGHT) / 2 + 63
        for button in self.pause_buttons:
            button.rect.center = (WINDOW_WIDTH / 2, y)
            y += 75

        self.upgrades = copy.deepcopy(UPGRADES)
        self.upgrade_window = ScrollWindow((UPGRADE_WINDOW_FULL_WIDTH, UPGRADE_WINDOW_FULL_HEIGHT),
                                           (UPGRADE_WINDOW_WIDTH, UPGRADE_WINDOW_HEIGHT), WHITE)
        self.upgrade_window.full_surf.fill(LIGHTBLUE)
        draw_text(self.upgrade_window.full_surf, 'Strategies:', 30, BLACK, 'topleft', 10, 10)
        draw_text(self.upgrade_window.full_surf, 'Perks:', 30, BLACK, 'topleft', 10, 710)
        draw_text(self.upgrade_window.full_surf, 'Activities (repeatable):', 30, BLACK, 'topleft', 10, 1410)

        self.upgrade_buttons = []
        for upgrade in self.upgrades:
            upgrade_dict = self.upgrades[upgrade]
            bg_img = None
            textlines = None
            o_color = None
            if upgrade in self.upgrade_button_images:
                bg_img = self.upgrade_button_images[upgrade][self.upgrades[upgrade]['status']]
            else:
                textlines = [TextLine(upgrade_dict['text'], size=upgrade_dict['font size'])]
                o_color = BLACK
            self.upgrade_buttons.append(Button(textlines, auto_size=False, o_color=o_color, bg_img=bg_img,
                                               rect=upgrade_dict['rect'], return_value=upgrade))

    def load_images(self):
        self.icons = {
            'burnout': pygame.image.load(path.join(self.img_dir, 'icon-burnout_24x24.png')).convert(),
            'costs': pygame.image.load(path.join(self.img_dir, 'icon-costs_24x24.png')).convert(),
            'days': pygame.image.load(path.join(self.img_dir, 'icon-days_24x24.png')).convert(),
            'ego': pygame.image.load(path.join(self.img_dir, 'icon-ego_24x24.png')).convert(),
            'energy': pygame.image.load(path.join(self.img_dir, 'icon-energy_24x24.png')).convert(),
            'fire': pygame.image.load(path.join(self.img_dir, 'icon-fire_24x24.png')).convert(),
            'likes': pygame.image.load(path.join(self.img_dir, 'icon-likes_24x24.png')).convert(),
            'money': pygame.image.load(path.join(self.img_dir, 'icon-money_24x24.png')).convert(),
            'move': pygame.image.load(path.join(self.img_dir, 'icon-move_24x24.png')).convert(),
            'net': pygame.image.load(path.join(self.img_dir, 'icon-net_24x24.png')).convert(),
            'patrons': pygame.image.load(path.join(self.img_dir, 'icon-patrons_24x24.png')).convert(),
            'pause': pygame.image.load(path.join(self.img_dir, 'icon-pause_24x24.png')).convert(),
            'quit': pygame.image.load(path.join(self.img_dir, 'icon-quit_24x24.png')).convert(),
            'revenue': pygame.image.load(path.join(self.img_dir, 'icon-revenue_24x24.png')).convert(),
            'sketchiness': pygame.image.load(path.join(self.img_dir, 'icon-sketchiness_24x24.png')).convert(),
            'subscribers': pygame.image.load(path.join(self.img_dir, 'icon-subscribers_24x24.png')).convert(),
        }

        upgrade_icons = {
            'effectiveness 1': {
                'locked': pygame.image.load(path.join(self.img_dir, 'effectiveness_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'effectiveness_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'effectiveness_32x32.png')).convert(),
            },
            'effectiveness 2': {
                'locked': pygame.image.load(path.join(self.img_dir, 'effectivenessx2_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'effectivenessx2_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'effectivenessx2_32x32.png')).convert(),
            },
            'size 1': {
                'locked': pygame.image.load(path.join(self.img_dir, 'size_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'size_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'size_32x32.png')).convert(),
            },
            'size 2': {
                'locked': pygame.image.load(path.join(self.img_dir, 'sizex2_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'sizex2_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'sizex2_32x32.png')).convert(),
            },
            'size 3': {
                'locked': pygame.image.load(path.join(self.img_dir, 'sizex3_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'sizex3_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'sizex3_32x32.png')).convert(),
            },
            'size 4': {
                'locked': pygame.image.load(path.join(self.img_dir, 'sizex4_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'sizex4_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'sizex4_32x32.png')).convert(),
            },
            'speed 1': {
                'locked': pygame.image.load(path.join(self.img_dir, 'speed_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'speed_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'speed_32x32.png')).convert(),
            },
            'speed 2': {
                'locked': pygame.image.load(path.join(self.img_dir, 'speedx2_32x32.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'speedx2_32x32.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'speedx2_32x32.png')).convert(),
            },
        }

        self.upgrade_button_images = {
            'analytics': {
                'available': pygame.image.load(path.join(self.img_dir, 'analytics-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'analytics-200x100.png')).convert()},
            'ban': {
                'locked': pygame.image.load(path.join(self.img_dir, 'ban-unavailable-200x100.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'ban-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'ban-active-200x100.png')).convert()},
            'catch phrase': {
                'available': pygame.image.load(path.join(self.img_dir, 'catch-phrases-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'catch-phrases-200x100.png')).convert()},
            'CP dmg 1': {
                'locked': upgrade_icons['effectiveness 1']['locked'],
                'available': upgrade_icons['effectiveness 1']['available'],
                'bought': upgrade_icons['effectiveness 1']['bought']},
            'CP dmg 2': {
                'locked': upgrade_icons['effectiveness 2']['locked'],
                'available': upgrade_icons['effectiveness 2']['available'],
                'bought': upgrade_icons['effectiveness 2']['bought']},
            'CP speed 1': {
                'locked': upgrade_icons['speed 1']['locked'],
                'available': upgrade_icons['speed 1']['available'],
                'bought': upgrade_icons['speed 1']['bought']},
            'CP speed 2': {
                'locked': upgrade_icons['speed 2']['locked'],
                'available': upgrade_icons['speed 2']['available'],
                'bought': upgrade_icons['speed 2']['bought']},
            'channel art': {
                'available': pygame.image.load(path.join(self.img_dir, 'channel-art-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'channel-art-200x100.png')).convert()},
            'eat something': {
                'available': pygame.image.load(path.join(self.img_dir, 'eat-something-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'eat-something-200x100.png')).convert()},
            'fake subscribers': {
                'available': pygame.image.load(path.join(self.img_dir, 'subscribers-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'subscribers-200x100.png')).convert()},
            'fake swears': {
                'available': pygame.image.load(path.join(self.img_dir, 'fake-swears-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'fake-swears-200x100.png')).convert()},
            'FS dmg 1': {
                'locked': upgrade_icons['effectiveness 1']['locked'],
                'available': upgrade_icons['effectiveness 1']['available'],
                'bought': upgrade_icons['effectiveness 1']['bought']},
            'FS dmg 2': {
                'locked': upgrade_icons['effectiveness 2']['locked'],
                'available': upgrade_icons['effectiveness 2']['available'],
                'bought': upgrade_icons['effectiveness 2']['bought']},
            'FS speed 1': {
                'locked': upgrade_icons['speed 1']['locked'],
                'available': upgrade_icons['speed 1']['available'],
                'bought': upgrade_icons['speed 1']['bought']},
            'FS speed 2': {
                'locked': upgrade_icons['speed 2']['locked'],
                'available': upgrade_icons['speed 2']['available'],
                'bought': upgrade_icons['speed 2']['bought']},
            'gaming chair': {
                'available': pygame.image.load(path.join(self.img_dir, 'gaming-chair-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'gaming-chair-200x100.png')).convert()},
            'GC size 1': {
                'locked': upgrade_icons['size 1']['locked'],
                'available': upgrade_icons['size 1']['available'],
                'bought': upgrade_icons['size 1']['bought']},
            'GC size 2': {
                'locked': upgrade_icons['size 2']['locked'],
                'available': upgrade_icons['size 2']['available'],
                'bought': upgrade_icons['size 2']['bought']},
            'GC size 3': {
                'locked': upgrade_icons['size 3']['locked'],
                'available': upgrade_icons['size 3']['available'],
                'bought': upgrade_icons['size 3']['bought']},
            'GC size 4': {
                'locked': upgrade_icons['size 4']['locked'],
                'available': upgrade_icons['size 4']['available'],
                'bought': upgrade_icons['size 4']['bought']},
            'green screen': {
                'available': pygame.image.load(path.join(self.img_dir, 'greenscreen-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'greenscreen-200x100.png')).convert()},
            'guest host': {
                'locked': pygame.image.load(path.join(self.img_dir, 'guest-host-unavailable-200x100.png')).convert(),
                'available': pygame.image.load(path.join(self.img_dir, 'guest-host-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'guest-host-active-200x100.png')).convert()},
            'live stream': {
                'available': pygame.image.load(path.join(self.img_dir, 'live-stream-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'live-stream-200x100.png')).convert()},
            'partner': {
                'available': pygame.image.load(path.join(self.img_dir, 'advertisers-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'advertisers-200x100.png')).convert()},
            'puns': {
                'available': pygame.image.load(path.join(self.img_dir, 'puns-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'puns-200x100.png')).convert()},
            'puns dmg 1': {
                'locked': upgrade_icons['effectiveness 1']['locked'],
                'available': upgrade_icons['effectiveness 1']['available'],
                'bought': upgrade_icons['effectiveness 1']['bought']},
            'puns dmg 2': {
                'locked': upgrade_icons['effectiveness 2']['locked'],
                'available': upgrade_icons['effectiveness 2']['available'],
                'bought': upgrade_icons['effectiveness 2']['bought']},
            'puns speed 1': {
                'locked': upgrade_icons['speed 1']['locked'],
                'available': upgrade_icons['speed 1']['available'],
                'bought': upgrade_icons['speed 1']['bought']},
            'puns speed 2': {
                'locked': upgrade_icons['speed 2']['locked'],
                'available': upgrade_icons['speed 2']['available'],
                'bought': upgrade_icons['speed 2']['bought']},
            'quality content': {
                'available': pygame.image.load(path.join(self.img_dir, 'quality-content-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'quality-content-200x100.png')).convert()},
            'QC dmg 1': {
                'locked': upgrade_icons['effectiveness 1']['locked'],
                'available': upgrade_icons['effectiveness 1']['available'],
                'bought': upgrade_icons['effectiveness 1']['bought']},
            'QC dmg 2': {
                'locked': upgrade_icons['effectiveness 2']['locked'],
                'available': upgrade_icons['effectiveness 2']['available'],
                'bought': upgrade_icons['effectiveness 2']['bought']},
            'QC speed 1': {
                'locked': upgrade_icons['speed 1']['locked'],
                'available': upgrade_icons['speed 1']['available'],
                'bought': upgrade_icons['speed 1']['bought']},
            'QC speed 2': {
                'locked': upgrade_icons['speed 2']['locked'],
                'available': upgrade_icons['speed 2']['available'],
                'bought': upgrade_icons['speed 2']['bought']},
            'self stirring mug': {
                'available': pygame.image.load(path.join(self.img_dir, 'mug-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'mug-200x100.png')).convert()},
            'swears': {
                'available': pygame.image.load(path.join(self.img_dir, 'swears-inactive-200x100.png')).convert(),
                'bought': pygame.image.load(path.join(self.img_dir, 'swears-200x100.png')).convert()},
            'swears dmg 1': {
                'locked': upgrade_icons['effectiveness 1']['locked'],
                'available': upgrade_icons['effectiveness 1']['available'],
                'bought': upgrade_icons['effectiveness 1']['bought']},
            'swears dmg 2': {
                'locked': upgrade_icons['effectiveness 2']['locked'],
                'available': upgrade_icons['effectiveness 2']['available'],
                'bought': upgrade_icons['effectiveness 2']['bought']},
            'swears speed 1': {
                'locked': upgrade_icons['speed 1']['locked'],
                'available': upgrade_icons['speed 1']['available'],
                'bought': upgrade_icons['speed 1']['bought']},
            'swears speed 2': {
                'locked': upgrade_icons['speed 2']['locked'],
                'available': upgrade_icons['speed 2']['available'],
                'bought': upgrade_icons['speed 2']['bought']},

        }

        self.pause_button_images = {
            'quit': pygame.image.load(path.join(self.img_dir, 'options-quit-150x50.png')).convert(),
            'restart': pygame.image.load(path.join(self.img_dir, 'options-restart-150x50.png')).convert(),
            'resume': pygame.image.load(path.join(self.img_dir, 'options-resume-150x50.png')).convert(),
            'retire': pygame.image.load(path.join(self.img_dir, 'options-retire-150x50.png')).convert(),
            'save': pygame.image.load(path.join(self.img_dir, 'options-save-150x50.png')).convert(),
            'upgrades': pygame.image.load(path.join(self.img_dir, 'options-upgrades-150x50.png')).convert(),
        }

        self.pause_background = pygame.image.load(path.join(self.img_dir, 'option-200x500.png')).convert()

    def star_field(self):
        for i in range(50):
            Star(self)

    def flash_energy(self):
        self.flash_timer = 0.2
        self.energy_flash = True

    def can_unlock(self, upgrade):
        unlockable = True
        if self.upgrades[upgrade]['status'] != 'available':
            unlockable = False
        else:
            for cost in self.upgrades[upgrade]['costs']:
                if cost == 'cash' and self.upgrades[upgrade]['costs']['cash'] > self.cash:
                    unlockable = False
        if 'cooldown' in self.upgrades[upgrade] and self.upgrades[upgrade]['cooldown'] > 0:
            unlockable = False
        return unlockable

    def upgrade(self, upgrade):
        upgrade_dict = self.upgrades[upgrade]
        tags = upgrade_dict['action tags']
        if 'weapon' in tags:
            self.weapons_unlocked.add(upgrade)
        if 'eat' in tags:
            self.eat_rate += 10
        if 'art' in tags:
            self.conversion_rate *= 2
            self.update_conversion()
        if 'analytics' in tags:
            self.analytics = True
        if 'chair' in tags:
            self.chair.size_factor = 1
            self.chair.update_size()
        if 'mug' in tags:
            self.max_energy *= 1.5
            self.energy_bonus = 1.5
        if 'green screen' in tags:
            for weapon in self.weapons:
                if weapon != 'side job':
                    weapon['damage'] = int(weapon['damage'] * 1.5)
        if 'fake subs' in tags:
            self.fake_subscribers += 1000
            self.sketchiness += 10
            self.update_conversion()
        if 'partner' in tags:
            self.cash += int(self.subscribers * 0.05)
        if 'fluff' in tags:
            self.ego_size -= 10
            self.ego_size = max(0, self.ego_size)
            self.tony.fluff = True
            self.tony.update_size(self.ego_size)

        for cost in upgrade_dict['costs']:
            if cost == 'cash':
                self.cash -= upgrade_dict['costs']['cash']
            elif cost == 'subs':
                self.subscribers = int(self.subscribers * 0.95)
                self.update_conversion()

        if 'bonus' in tags:
            if 'weapon bonuses' in upgrade_dict:
                for bonus_dict in upgrade_dict['weapon bonuses']:
                    if 'rate' in bonus_dict['bonus']:
                        self.weapons[WEAPON_LIST.index(bonus_dict['name'])]['rate'] *= bonus_dict['bonus']['rate']
                    if 'damage' in bonus_dict['bonus']:
                        self.weapons[WEAPON_LIST.index(bonus_dict['name'])]['damage'] *= bonus_dict['bonus']['damage']
            if 'chair bonus' in upgrade_dict:
                self.chair.size_factor *= 2
                self.chair.update_size()

        if 'unlocks' in upgrade_dict:
            for unlock in upgrade_dict['unlocks']:
                self.upgrades[unlock]['status'] = 'available'

        if 'cooldown' in upgrade_dict:
            self.upgrades[upgrade]['cooldown'] = self.upgrades[upgrade]['base cooldown']

        self.upgrades[upgrade]['status'] = 'bought'

        self.log.add_text(self.upgrades[upgrade]['log text'])
        self.switch_weapon(0)
        self.update_upgrades()

    def update_conversion(self):
        conversion_bonus = min(20, max(0, (round(math.log(self.subscribers + self.fake_subscribers + 1, 10) * 2) - 2)))
        self.eff_conversion_rate = round(self.conversion_rate * (100 - self.sketchiness) / 100) + conversion_bonus

    def update_upgrades(self):
        on_cooldown = False
        for button in self.upgrade_buttons:
            if self.upgrades[button.return_value]['status'] == 'locked':
                if button.bg_img is None:
                    button.change('bg_color', GREY)
            elif ('cooldown' in self.upgrades[button.return_value]
                  and self.upgrades[button.return_value]['cooldown'] > 0):
                on_cooldown = True
                if button.bg_img is None:
                    button.change('bg_color', GREEN)
            elif self.upgrades[button.return_value]['status'] == 'available':
                if button.bg_img is None:
                    button.change('bg_color', WHITE)
            elif self.upgrades[button.return_value]['status'] == 'bought':
                if button.bg_img is None:
                    button.change('bg_color', GREEN)

            # if button has a background, set its background according to its status
            if button.return_value in self.upgrade_button_images:
                new_img = self.upgrade_button_images[button.return_value][self.upgrades[button.return_value]['status']]
                button.change('bg_img', new_img)

            self.upgrade_window.full_surf.blit(button.image, button.rect)

            textlist = [TextLine(self.upgrades[button.return_value]['full text'])]
            if on_cooldown:
                textlist.append(TextLine('(on cooldown)', RED))

            if (self.upgrades[button.return_value]['status'] != 'bought' and
                    'costs' in self.upgrades[button.return_value]):
                textlist.append(TextLine('costs:'))
                for cost in self.upgrades[button.return_value]['costs']:
                    if cost == 'subs':
                        if button.return_value == 'partner':
                            text = "  " + str(int(self.subscribers * 0.05)) + " subs"
                            textlist.append(TextLine(text))
                    if cost == 'cash':
                        text = "  $" + str(self.upgrades[button.return_value]['costs'][cost])
                        if self.cash >= self.upgrades[button.return_value]['costs']['cash']:
                            color = BLACK
                        else:
                            color = RED
                        textlist.append(TextLine(text, color))
            button.tooltip = ToolTip(textlist)

    def switch_weapon(self, d):
        self.weapon_index += d
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0
        elif self.weapon_index < 0:
            self.weapon_index = len(self.weapons) - 1
        while self.weapons[self.weapon_index]['name'] not in self.weapons_unlocked:
            self.weapon_index += d
            if self.weapon_index >= len(self.weapons):
                self.weapon_index = 0
            elif self.weapon_index < 0:
                self.weapon_index = len(self.weapons) - 1

        self.fire_rate = self.weapons[self.weapon_index]['rate']

    def shoot(self):
        weapon_dict = self.weapons[self.weapon_index]
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            if self.energy >= weapon_dict['energy']:
                Bullet(self, self.tony.rect.centerx, self.tony.rect.y, weapon_dict['name'], weapon_dict['damage'])
                self.last_shot = now
                self.energy -= weapon_dict['energy']
                if weapon_dict['name'] == 'side job':
                    self.cash += 100

                self.recent_shots.append(weapon_dict['name'])
                if len(self.recent_shots) > 20:
                    del self.recent_shots[0]
                self.burn_out = 0
                for item in self.recent_shots:
                    self.burn_out = max(0, self.burn_out, self.recent_shots.count(item) - 10)

                return True
            else:
                return False
        return True

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_bullets = pygame.sprite.LayeredUpdates()
        self.all_people = pygame.sprite.LayeredUpdates()
        self.all_stars = pygame.sprite.LayeredUpdates()
        self.chairs = pygame.sprite.LayeredUpdates()
        self.star_field()
        self.tony = Tony(self)
        self.chair = Chair(self)
        self.log = Log(self)
        self.weapons = copy.deepcopy(WEAPONS)
        self.weapon_index = 0
        self.fire_rate = self.weapons[self.weapon_index]['rate']
        self.weapons_unlocked = {'side job'}
        self.last_shot = 0
        self.recent_shots = []
        self.burn_out = 0
        self.ego_size = 0
        self.days = 0
        self.likes = 0
        self.subscribers = 1000
        self.fake_subscribers = 0
        self.patrons = 0
        self.cash = 1000000
        self.revenue = 0
        self.energy = 100
        self.max_energy = 100
        self.energy_bonus = 1.0
        self.eat_rate = 10
        self.conversion_rate = 10
        self.sketchiness = 0
        self.eff_conversion_rate = 10
        self.spawn_timer = 0
        self.sparkle_timer = 0
        self.update_timer = 0
        self.flash_timer = 0.0
        self.affinity_trends = {'puns': 50, 'swears': 50, 'fake swears': 50, 'catch phrase': 50}
        self.analytics = False
        self.energy_flash = False
        self.upgrades = copy.deepcopy(UPGRADES)
        self.update_upgrades()

        self.chair.size_factor = 0
        self.chair.update_size()

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        self.sparkle_timer += self.dt
        if self.sparkle_timer > SPARKLE_RATE:
            for star in self.all_stars:
                star.sparkle()
            self.sparkle_timer = 0.0

        self.spawn_timer += self.dt
        if self.spawn_timer > SPAWN_RATE:
            if len(self.all_people) < 5:
                Person(self)
                self.spawn_timer = 0.0

        if self.flash_timer > 0:
            self.flash_timer -= self.dt
            if self.flash_timer <= 0:
                self.flash_timer = 0.0
                self.energy_flash = False

        # hit mobs with bullets
        mob_hits = pygame.sprite.groupcollide(self.all_people, self.all_bullets, False, True,
                                              pygame.sprite.collide_mask)
        for mob in mob_hits:
            for bullet in mob_hits[mob]:
                mob.hit(bullet.type, bullet.damage)

        # hit tony with mobs
        tony_hits = pygame.sprite.spritecollide(self.tony, self.all_people, False, pygame.sprite.collide_mask)
        for mob in tony_hits:
            if not mob.hit_tony:
                mob.progress -= 0.5 * mob.max_progress
                mob.hit_tony = True
                mob.redraw()

        self.all_sprites.update()
        self.chair.update()

        if self.likes < 0:
            self.likes = 0
        if self.subscribers < 0:
            self.subscribers = 0
        if self.patrons < 0:
            self.patrons = 0

        self.update_conversion()

        self.revenue = int((self.patrons * 2) + (self.subscribers / 1000))

        self.update_timer += self.dt
        if self.update_timer > 5.0:
            self.days += 1
            for upgrade in self.upgrades:
                if 'cooldown' in self.upgrades[upgrade] and self.upgrades[upgrade]['cooldown'] > 0:
                    self.upgrades[upgrade]['cooldown'] -= 1
                    if self.upgrades[upgrade]['cooldown'] == 0:
                        self.upgrades[upgrade]['status'] = 'available'
                        if 'fluff' in self.upgrades[upgrade]['action tags']:
                            self.tony.fluff = False
                            self.tony.update_size(self.ego_size)

            self.tony.update_size(self.ego_size)
            self.likes += self.subscribers // 100
            self.cash += self.revenue

            if self.cash >= self.eat_rate:
                burnout_penalty = self.burn_out / 20
                self.energy = min(self.max_energy, self.energy +
                                  (self.eat_rate * (1 - burnout_penalty)) * self.energy_bonus)
                self.cash -= self.eat_rate

            for trend in self.affinity_trends:
                if self.affinity_trends[trend] > 80:
                    self.affinity_trends[trend] -= 5
                elif self.affinity_trends[trend] < 20:
                    self.affinity_trends[trend] += 5
                else:
                    self.affinity_trends[trend] += random.choice([5, -5])

            self.update_timer = 0.0

    def events(self):
        if self.paused and not self.upgrading:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    self.running = False
                    self.playing = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.paused = False
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False
                    for button in self.pause_buttons:
                        if button.rect.collidepoint(mouse):
                            clicked = button.return_value
                    if clicked:
                        if clicked == 'resume':
                            self.paused = False
                        elif clicked == 'upgrades':
                            self.upgrading = True
                            self.update_upgrades()
                        elif clicked == 'save':
                            pass
                        elif clicked == 'retire':
                            pass
                        elif clicked == 'restart':
                            self.playing = False
                            self.paused = False
                        elif clicked == 'quit':
                            self.paused = False
                            self.running = False
                            self.playing = False
        elif self.upgrading:
            mouse = pygame.mouse.get_pos()
            screen_offset = self.screen.get_offset()
            offset = (screen_offset[0] + UPGRADE_WINDOW_OFFSET_X, screen_offset[1] + UPGRADE_WINDOW_OFFSET_Y)
            rel_mouse = get_rel_mouse(mouse, offset)
            win = self.upgrade_window
            upgrade_mouse = get_rel_mouse(rel_mouse, (-win.xpos, -win.ypos))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.upgrading = False
                        self.paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if win.view_surf.get_rect().collidepoint(rel_mouse):
                            for button in self.upgrade_buttons:
                                if button.rect.collidepoint(upgrade_mouse):
                                    if self.can_unlock(button.return_value):
                                        self.upgrade(button.return_value)

                        if win.has_h_sb:
                            if win.h_sb.collidepoint(rel_mouse):
                                win.moving_h = True
                                win.start_mouse = rel_mouse
                                win.start_x = win.h_sb.left
                        if win.has_v_sb:
                            if win.v_sb.collidepoint(rel_mouse):
                                win.moving_v = True
                                win.start_mouse = rel_mouse
                                win.start_y = win.v_sb.top
                    elif event.button == 4:
                        if win.window_surf.get_rect().collidepoint(rel_mouse):
                            win.scroll(-10)
                    elif event.button == 5:
                        if win.window_surf.get_rect().collidepoint(rel_mouse):
                            win.scroll(10)

                if event.type == pygame.MOUSEBUTTONUP:
                    win.moving_h = False
                    win.moving_v = False

            if win.moving_h:
                win.h_sb.left = min(win.view_size[0] - win.h_sb.w,
                                    max(0, win.start_x - (win.start_mouse[0] - rel_mouse[0])))
                win.xpos = win.h_sb.left / (win.view_size[0] - win.h_sb_size) * (win.full_size[0] - win.view_size[0])
            if win.moving_v:
                win.v_sb.top = min(win.view_size[1] - win.v_sb.h,
                                   max(0, win.start_y - (win.start_mouse[1] - rel_mouse[1])))
                win.ypos = win.v_sb.top / (win.view_size[1] - win.v_sb_size) * (win.full_size[1] - win.view_size[1])

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.playing = False
                    if event.key == pygame.K_UP:
                        self.switch_weapon(1)
                    if event.key == pygame.K_DOWN:
                        self.switch_weapon(-1)
                    if event.key == pygame.K_p:
                        self.paused = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if not self.shoot():
                    # shot didn't fire
                    self.flash_energy()

    def draw(self):
        # pygame.display.set_caption(str(self.clock.get_fps()))
        self.window.fill(BLACK)
        # self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.log.draw()

        # PLAYER STATS
        y = 5
        screen_offset = self.screen.get_offset()[0] - 5
        draw_text(self.window, 'STATS:', 30, WHITE, 'topleft', 5, y)
        y += 35
        self.window.blit(self.icons['days'], (5, y, 24, 24))
        draw_text(self.window, 'Days: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, "{:,}".format(self.days), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['likes'], (5, y, 24, 24))
        draw_text(self.window, 'Likes: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, "{:,}".format(self.likes), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['subscribers'], (5, y, 24, 24))
        draw_text(self.window, 'Subscribers: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, "{:,}".format(self.subscribers + self.fake_subscribers), 20, WHITE, 'topright',
                  screen_offset, y)
        y += 25
        self.window.blit(self.icons['patrons'], (5, y, 24, 24))
        draw_text(self.window, 'Patrons: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, "{:,}".format(self.patrons), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['money'], (5, y, 24, 24))
        draw_text(self.window, 'Money: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, '$ ' + "{:,}".format(self.cash), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['revenue'], (5, y, 24, 24))
        draw_text(self.window, 'Revenue: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, '$ ' + "{:,}".format(self.revenue), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['costs'], (5, y, 24, 24))
        draw_text(self.window, 'Costs: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, '$ ' + "{:,}".format(self.eat_rate), 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['net'], (5, y, 24, 24))
        draw_text(self.window, 'Net: ', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, '$ ' + "{:,}".format(self.revenue - self.eat_rate), 20, WHITE, 'topright', screen_offset,
                  y)
        y += 35
        self.window.blit(self.icons['energy'], (5, y, 24, 24))
        draw_text(self.window, 'Energy:', 20, WHITE, 'topleft', 30, y)

        y += 25
        if self.energy_flash:
            pygame.draw.rect(self.window, RED, (5, y, self.max_energy, 20))
        else:
            if self.energy > 0:
                pygame.draw.rect(self.window, GREEN, (5, y, self.energy, 20))
        pygame.draw.rect(self.window, WHITE, (5, y, self.max_energy, 20), 1)

        y += 25
        self.window.blit(self.icons['burnout'], (5, y, 24, 24))
        draw_text(self.window, 'Burnout:', 20, WHITE, 'topleft', 30, y)

        y += 25
        if self.burn_out > 0:
            pygame.draw.rect(self.window, RED, (5, y, self.burn_out * 10, 20))
        pygame.draw.rect(self.window, WHITE, (5, y, 100, 20), 1)

        y += 25
        self.window.blit(self.icons['ego'], (5, y, 24, 24))
        draw_text(self.window, 'Ego:', 20, WHITE, 'topleft', 30, y)

        y += 25
        if self.ego_size > 0:
            pygame.draw.rect(self.window, RED, (5, y, self.ego_size, 20))
        pygame.draw.rect(self.window, WHITE, (5, y, 100, 20), 1)

        y += 25
        self.window.blit(self.icons['sketchiness'], (5, y, 24, 24))
        draw_text(self.window, 'Sketchiness:', 20, WHITE, 'topleft', 30, y)

        y += 25
        if self.sketchiness > 0:
            pygame.draw.rect(self.window, RED, (5, y, self.sketchiness, 20))
        pygame.draw.rect(self.window, WHITE, (5, y, 100, 20), 1)

        # INSTRUCTIONS
        y = WINDOW_HEIGHT - 265
        draw_text(self.window, 'CONTROLS:', 30, WHITE, 'topleft', 5, y)
        y += 35
        self.window.blit(self.icons['pause'], (5, y, 24, 24))
        draw_text(self.window, 'Pause Menu:', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, 'P', 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['move'], (5, y, 24, 24))
        draw_text(self.window, 'Move:', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, 'Left/Right', 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['fire'], (5, y, 24, 24))
        draw_text(self.window, 'Fire:', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, 'SPACE', 20, WHITE, 'topright', screen_offset, y)
        y += 25
        self.window.blit(self.icons['quit'], (5, y, 24, 24))
        draw_text(self.window, 'Quit:', 20, WHITE, 'topleft', 30, y)
        draw_text(self.window, 'ESC', 20, WHITE, 'topright', screen_offset, y)

        # WEAPON STATS
        draw_text(self.window, self.weapons[self.weapon_index]['title'], 50, WHITE, 'bottomright',
                  WINDOW_WIDTH - 5, WINDOW_HEIGHT - 50)
        y = WINDOW_HEIGHT - 300
        draw_text(self.window, "STRATEGY:", 30, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y - 35)
        for line in self.weapons[self.weapon_index]['description']:
            draw_text(self.window, line, 20, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y)
            y += 25
        draw_text(self.window, 'Energy:', 20, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y + 25)
        draw_text(self.window, str(self.weapons[self.weapon_index]['energy']), 20, WHITE, 'topright',
                  WINDOW_WIDTH - 5, y + 25)
        if self.weapons[self.weapon_index]['name'] != 'ban':
            draw_text(self.window, 'Effectiveness:', 20, WHITE,
                      'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y + 50)
            draw_text(self.window, str(self.weapons[self.weapon_index]['damage']), 20, WHITE,
                      'topright', WINDOW_WIDTH - 5, y + 50)

        # Analytics
        if self.analytics:
            draw_text(self.window, "ANALYTICS: ", 30, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, 5)
            draw_text(self.window, "Strategies:", 25, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, 55)
            draw_text(self.window, "Interest:", 25, WHITE, 'topright', WINDOW_WIDTH - 5, 55)

            y = 95

            for trend in self.affinity_trends:
                draw_text(self.window, trend + ": ", 20, WHITE, 'topleft', (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y)
                draw_text(self.window, str(self.affinity_trends[trend]), 20, WHITE, 'topright', WINDOW_WIDTH - 5, y)
                y += 25

            draw_text(self.window, "Subscriber conversion rate:", 25, WHITE, 'topleft',
                      (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y + 5)
            if self.sketchiness > 0:
                draw_text(self.window, "(affected by sketchiness)", 25, WHITE, 'topleft',
                          (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y + 35)
                y += 30
            draw_text(self.window, str(self.eff_conversion_rate) + "%", 20, WHITE, 'topleft',
                      (WINDOW_WIDTH + SCREEN_WIDTH) / 2 + 5, y + 35)

        pygame.draw.rect(self.window, WHITE, self.screen.get_rect(topleft=self.screen.get_offset()), 1)
        tooltip = None
        mouse = pygame.mouse.get_pos()

        if self.paused and not self.upgrading:
            menu_rect = pygame.Rect((0, 0, PAUSE_MENU_WIDTH, PAUSE_MENU_HEIGHT))
            menu_rect.centerx = self.window.get_rect().centerx
            menu_rect.centery = self.screen.get_rect().centery
            self.window.blit(self.pause_background, menu_rect)
            # pygame.draw.rect(self.window, LIGHTBLUE, menu_rect)
            for button in self.pause_buttons:
                self.window.blit(button.image, button.rect)

        elif self.upgrading:
            self.upgrade_window.draw(self.screen, (UPGRADE_WINDOW_OFFSET_X, UPGRADE_WINDOW_OFFSET_Y))
            screen_offset = self.screen.get_offset()
            offset = (screen_offset[0] + UPGRADE_WINDOW_OFFSET_X, screen_offset[1] + UPGRADE_WINDOW_OFFSET_Y)
            rel_mouse = get_rel_mouse(mouse, offset)
            win = self.upgrade_window
            upgrade_mouse = get_rel_mouse(rel_mouse, (-win.xpos, -win.ypos))

            if win.view_surf.get_rect().collidepoint(rel_mouse):
                for button in self.upgrade_buttons:
                    if button.rect.collidepoint(upgrade_mouse):
                        tooltip = button.tooltip
        if tooltip:
            tooltip.draw(self.window, mouse)

        pygame.display.flip()


g = Game()
while g.running:
    g.new()

pygame.quit()
quit()
