import pygame

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

PAUSE_MENU_WIDTH = 200
PAUSE_MENU_HEIGHT = 500

UPGRADE_WINDOW_WIDTH = 500
UPGRADE_WINDOW_HEIGHT = 650
UPGRADE_WINDOW_OFFSET_X = (SCREEN_WIDTH - UPGRADE_WINDOW_WIDTH) / 2
UPGRADE_WINDOW_OFFSET_Y = (SCREEN_HEIGHT - UPGRADE_WINDOW_HEIGHT) / 2
UPGRADE_WINDOW_FULL_WIDTH = 1000
UPGRADE_WINDOW_FULL_HEIGHT = 5000

FPS = 0

FONT = 'arial'

LOG_TEXT_SIZE = 20
LOG_MAX_LINES = 3
LOG_LINE_MARGIN = 10
LOG_Y = WINDOW_HEIGHT - ((LOG_TEXT_SIZE + LOG_LINE_MARGIN) * LOG_MAX_LINES)
LOG_X = 5

SPAWN_RATE = 5.0
SPARKLE_RATE = 0.2

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
LIGHTGREEN = pygame.Color('lightgreen')
DARKGREEN = pygame.Color('darkgreen')
GREEN = pygame.Color('green')
GREY = pygame.Color('grey')
BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
YELLOW = pygame.Color('yellow')
PURPLE = pygame.Color('purple')
CYAN = pygame.Color('cyan')

WEAPONS = [
    {'name': 'side job',
     'title': 'Side Job',
     'description': ['This is your day job, ',
                     'fire to earn $100.',
                     "Don't hit people with it."],
     'rate': 500,
     'energy': 50,
     'damage': 20},
    {'name': 'ban',
     'title': 'Ban',
     'description': ['Fire to neutralize trolls.'],
     'rate': 500,
     'energy': 5,
     'damage': 0},
    {'name': 'swears',
     'title': 'Swears',
     'description': ['Swear!'],
     'rate': 200,
     'energy': 1,
     'damage': 10},
    {'name': 'fake swears',
     'title': 'Fake Swears',
     'description': ['This is a family channel.'],
     'rate': 400,
     'energy': 2,
     'damage': 20},
    {'name': 'puns',
     'title': 'Puns',
     'description': ["Sun's out, puns out!"],
     'rate': 600,
     'energy': 3,
     'damage': 30},
    {'name': 'catch phrase',
     'title': 'Catch Phrase',
     'description': ['Hook, line, and sinker.'],
     'rate': 700,
     'energy': 7,
     'damage': 70},
    {'name': 'quality content',
     'title': 'Quality Content',
     'description': ['The best you can do, sadly.'],
     'rate': 1000,
     'energy': 10,
     'damage': 100},
]

WEAPON_LIST = [weapon['name'] for weapon in WEAPONS]

UPGRADES = {
    'puns': {'text': 'Puns',
             'log text': 'Puns unlocked!',
             'font size': 25,
             'full text': 'Unlock the "Puns" weapon',
             'status': 'available',
             'costs': {'cash': 100},
             'unlocks': ['puns speed 1', 'puns dmg 1', 'ban'],
             'rect': pygame.Rect((10, 50, 200, 100)),
             'action tags': ['weapon']},
    'puns dmg 1': {'text': 'I',
                   'log text': 'Your puns are now stronger!',
                   'font size': 15,
                   'full text': 'Double effectiveness for the "Puns" weapon',
                   'status': 'locked',
                   'costs': {'cash': 200},
                   'unlocks': ['puns dmg 2'],
                   'rect': pygame.Rect((220, 68, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'puns',
                                       'bonus': {'damage': 2}}]},
    'puns dmg 2': {'text': 'II',
                   'log text': 'Your puns are now super strong!!',
                   'font size': 15,
                   'full text': 'Double effectiveness for the "Puns" weapon',
                   'status': 'locked',
                   'costs': {'cash': 300},
                   'rect': pygame.Rect((262, 68, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'puns',
                                       'bonus': {'damage': 2}}]},
    'puns speed 1': {'text': 'I',
                     'log text': 'Punning at super speed!',
                     'font size': 15,
                     'full text': 'Double speed of the "Puns" weapon',
                     'status': 'locked',
                     'costs': {'cash': 200},
                     'unlocks': ['puns speed 2'],
                     'rect': pygame.Rect((220, 118, 32, 32)),
                     'action tags': ['bonus'],
                     'weapon bonuses': [{'name': 'puns',
                                         'bonus': {'rate': 0.5}}]},
    'puns speed 2': {'text': 'II',
                     'log text': 'Punning at full speed!',
                     'font size': 15,
                     'full text': 'Double speed of the "Puns" weapon',
                     'status': 'locked',
                     'costs': {'cash': 300},
                     'rect': pygame.Rect((262, 118, 32, 32)),
                     'action tags': ['bonus'],
                     'weapon bonuses': [{'name': 'puns',
                                         'bonus': {'rate': 0.5}}]},
    'ban': {'text': 'Ban',
            'log text': 'You can now ban trolls!',
            'font size': 25,
            'full text': 'Unlock the "Ban" weapon',
            'status': 'locked',
            'costs': {'cash': 100},
            'rect': pygame.Rect((10, 160, 200, 100)),
            'action tags': ['weapon']},
    'swears': {'text': 'Swears',
               'log text': 'This is no longer a family channel!',
               'font size': 25,
               'full text': 'Unlock the "Swears" weapon',
               'status': 'available',
               'costs': {'cash': 100},
               'unlocks': ['swears speed 1', 'swears dmg 1'],
               'rect': pygame.Rect((10, 270, 200, 100)),
               'action tags': ['weapon']},
    'swears dmg 1': {'text': 'I',
                     'log text': 'You swear even harder!',
                     'font size': 15,
                     'full text': 'Double effectiveness for the "Swears" weapon',
                     'status': 'locked',
                     'costs': {'cash': 200},
                     'unlocks': ['swears dmg 2'],
                     'rect': pygame.Rect((220, 288, 32, 32)),
                     'action tags': ['bonus'],
                     'weapon bonuses': [{'name': 'swears',
                                         'bonus': {'damage': 2}}]},
    'swears dmg 2': {'text': 'II',
                     'log text': 'Your swears are $%&*ing devastating!',
                     'font size': 15,
                     'full text': 'Double effectiveness for the "Swears" weapon',
                     'status': 'locked',
                     'costs': {'cash': 300},
                     'rect': pygame.Rect((262, 288, 32, 32)),
                     'action tags': ['bonus'],
                     'weapon bonuses': [{'name': 'swears',
                                         'bonus': {'damage': 2}}]},
    'swears speed 1': {'text': 'I',
                       'log text': 'You can swear even faster!',
                       'font size': 15,
                       'full text': 'Double speed of the "Swears" weapon',
                       'status': 'locked',
                       'costs': {'cash': 200},
                       'unlocks': ['swears speed 2'],
                       'rect': pygame.Rect((220, 338, 32, 32)),
                       'action tags': ['bonus'],
                       'weapon bonuses': [{'name': 'swears',
                                           'bonus': {'rate': 0.5}}]},
    'swears speed 2': {'text': 'II',
                       'log text': 'Your swears are $%&*ing fast!',
                       'font size': 15,
                       'full text': 'Double speed of the "Swears" weapon',
                       'status': 'locked',
                       'costs': {'cash': 300},
                       'rect': pygame.Rect((262, 338, 32, 32)),
                       'action tags': ['bonus'],
                       'weapon bonuses': [{'name': 'swears',
                                           'bonus': {'rate': 0.5}}]},
    'fake swears': {'text': 'Fake Swears',
                    'log text': 'This is (sometimes) a family channel!',
                    'font size': 25,
                    'full text': 'Unlock the "Fake Swears" weapon',
                    'status': 'available',
                    'costs': {'cash': 100},
                    'unlocks': ['FS speed 1', 'FS dmg 1'],
                    'rect': pygame.Rect((10, 380, 200, 100)),
                    'action tags': ['weapon']},
    'FS dmg 1': {'text': 'I',
                 'log text': 'Your fake swears are now stronger!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Fake Swears" weapon',
                 'status': 'locked',
                 'costs': {'cash': 200},
                 'unlocks': ['FS dmg 2'],
                 'rect': pygame.Rect((220, 398, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'fake swears',
                                     'bonus': {'damage': 2}}]},
    'FS dmg 2': {'text': 'II',
                 'log text': 'Your fake swears are now futching strong!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Fake Swears" weapon',
                 'status': 'locked',
                 'costs': {'cash': 300},
                 'rect': pygame.Rect((262, 398, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'fake swears',
                                     'bonus': {'damage': 2}}]},
    'FS speed 1': {'text': 'I',
                   'log text': 'Your fake swears are now faster!',
                   'font size': 15,
                   'full text': 'Double speed of the "Fake Swears" weapon',
                   'status': 'locked',
                   'costs': {'cash': 200},
                   'unlocks': ['FS speed 2'],
                   'rect': pygame.Rect((220, 448, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'fake swears',
                                       'bonus': {'rate': 0.5}}]},
    'FS speed 2': {'text': 'II',
                   'log text': 'Your fake swears are now ducking fast!',
                   'font size': 15,
                   'full text': 'Double speed of the "Fake Swears" weapon',
                   'status': 'locked',
                   'costs': {'cash': 300},
                   'rect': pygame.Rect((262, 448, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'fake swears',
                                       'bonus': {'rate': 0.5}}]},
    'catch phrase': {'text': 'Catch Phrases',
                     'log text': 'You have unlocked catch phrases!',
                     'font size': 25,
                     'full text': 'Unlock the "Catch Phrase" weapon',
                     'status': 'available',
                     'costs': {'cash': 100},
                     'unlocks': ['CP speed 1', 'CP dmg 1'],
                     'rect': pygame.Rect((10, 490, 200, 100)),
                     'action tags': ['weapon']},
    'CP dmg 1': {'text': 'I',
                 'log text': 'Your catch phrases are now catchier!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Catch Phrase" weapon',
                 'status': 'locked',
                 'costs': {'cash': 200},
                 'unlocks': ['CP dmg 2'],
                 'rect': pygame.Rect((220, 508, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'catch phrase',
                                     'bonus': {'damage': 2}}]},
    'CP dmg 2': {'text': 'II',
                 'log text': 'Your catch phrases are super catchy! Yowzers!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Catch Phrase" weapon',
                 'status': 'locked',
                 'costs': {'cash': 300},
                 'rect': pygame.Rect((262, 508, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'catch phrase',
                                     'bonus': {'damage': 2}}]},
    'CP speed 1': {'text': 'I',
                   'log text': 'Your catch phrases are now faster!',
                   'font size': 15,
                   'full text': 'Double speed of the "Catch Phrase" weapon',
                   'status': 'locked',
                   'costs': {'cash': 200},
                   'unlocks': ['CP speed 2'],
                   'rect': pygame.Rect((220, 558, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'catch phrase',
                                       'bonus': {'rate': 0.5}}]},
    'CP speed 2': {'text': 'II',
                   'log text': 'Your catch phrases are super fast! Jinkies!',
                   'font size': 15,
                   'full text': 'Double speed of the "Catch Phrase" weapon',
                   'status': 'locked',
                   'costs': {'cash': 300},
                   'rect': pygame.Rect((262, 558, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'catch phrase',
                                       'bonus': {'rate': 0.5}}]},
    'quality content': {'text': 'Quality Content',
                        'log text': 'Quality content unlocked!',
                        'font size': 25,
                        'full text': 'Unlock the "Quality Content" weapon',
                        'status': 'available',
                        'costs': {'cash': 1000},
                        'unlocks': ['QC speed 1', 'QC dmg 1'],
                        'rect': pygame.Rect((10, 600, 200, 100)),
                        'action tags': ['weapon']},
    'QC dmg 1': {'text': 'I',
                 'log text': 'Your quality content is even better!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Quality Content" weapon',
                 'status': 'locked',
                 'costs': {'cash': 2000},
                 'unlocks': ['QC dmg 2'],
                 'rect': pygame.Rect((220, 618, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'quality content',
                                     'bonus': {'damage': 2}}]},
    'QC dmg 2': {'text': 'II',
                 'log text': 'Your quality content is the best!',
                 'font size': 15,
                 'full text': 'Double effectiveness for the "Quality Content" weapon',
                 'status': 'locked',
                 'costs': {'cash': 3000},
                 'rect': pygame.Rect((262, 618, 32, 32)),
                 'action tags': ['bonus'],
                 'weapon bonuses': [{'name': 'quality content',
                                     'bonus': {'damage': 2}}]},
    'QC speed 1': {'text': 'I',
                   'log text': 'You can crank out quality content even faster!',
                   'font size': 15,
                   'full text': 'Double speed of the "Quality Content" weapon',
                   'status': 'locked',
                   'costs': {'cash': 2000},
                   'unlocks': ['QC speed 2'],
                   'rect': pygame.Rect((220, 668, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'quality content',
                                       'bonus': {'rate': 0.5}}]},
    'QC speed 2': {'text': 'II',
                   'log text': 'You can crank out quality content super fast!',
                   'font size': 15,
                   'full text': 'Double speed of the "Quality Content" weapon',
                   'status': 'locked',
                   'costs': {'cash': 3000},
                   'rect': pygame.Rect((262, 668, 32, 32)),
                   'action tags': ['bonus'],
                   'weapon bonuses': [{'name': 'quality content',
                                       'bonus': {'rate': 0.5}}]},
    'analytics': {'text': 'Analytics',
                  'log text': 'Analytics unlocked! Keep an eye on those numbers!',
                  'font size': 25,
                  'full text': 'Track market sentiments.',
                  'status': 'available',
                  'costs': {'cash': 200},
                  'rect': pygame.Rect((10, 750, 200, 100)),
                  'action tags': ['analytics']},
    'gaming chair': {'text': 'Gaming Chair',
                     'log text': 'You have a sweet gaming chair! It does nothing!',
                     'font size': 25,
                     'full text': 'Buy yourself a sweet gaming chair.',
                     'status': 'available',
                     'costs': {'cash': 500},
                     'unlocks': ['GC size 1'],
                     'rect': pygame.Rect((10, 860, 200, 100)),
                     'action tags': ['chair']},
    'GC size 1': {'text': 'I',
                  'log text': 'Your gaming chair is now bigger!',
                  'font size': 15,
                  'full text': 'Double the size of your gaming chair.',
                  'status': 'locked',
                  'costs': {'cash': 600},
                  'unlocks': ['GC size 2'],
                  'rect': pygame.Rect((220, 928, 32, 32)),
                  'action tags': ['bonus'],
                  'chair bonus': True},
    'GC size 2': {'text': 'II',
                  'log text': 'Your gaming chair is even bigger!',
                  'font size': 15,
                  'full text': 'Double the size of your gaming chair.',
                  'status': 'locked',
                  'costs': {'cash': 1200},
                  'unlocks': ['GC size 3'],
                  'rect': pygame.Rect((262, 928, 32, 32)),
                  'action tags': ['bonus'],
                  'chair bonus': True},
    'GC size 3': {'text': 'III',
                  'log text': 'Your gaming chair is so big you had to cut a hole in the ceiling!',
                  'font size': 15,
                  'full text': 'Double the size of your gaming chair.',
                  'status': 'locked',
                  'costs': {'cash': 2400},
                  'unlocks': ['GC size 4'],
                  'rect': pygame.Rect((304, 928, 32, 32)),
                  'action tags': ['bonus'],
                  'chair bonus': True},
    'GC size 4': {'text': 'IV',
                  'log text': "You now stream in two different time zones because of the size of your chair!",
                  'font size': 15,
                  'full text': 'Double the size of your gaming chair.',
                  'status': 'locked',
                  'costs': {'cash': 4800},
                  'rect': pygame.Rect((346, 928, 32, 32)),
                  'action tags': ['bonus'],
                  'chair bonus': True},
    'eat something': {'text': 'Eat Something, Tony!',
                      'log text': 'You work hard and eat hard!',
                      'font size': 25,
                      'full text': 'Spend more on food, but gain energy faster.',
                      'status': 'available',
                      'costs': {'cash': 100},
                      'unlocks': ['ES rate 1'],
                      'rect': pygame.Rect((10, 970, 200, 100)),
                      'action tags': ['eat']},
    'ES rate 1': {'text': 'I',
                  'log text': 'You work harder and eat harder!',
                  'font size': 15,
                  'full text': 'Eat even more, Tony!',
                  'status': 'locked',
                  'costs': {'cash': 200},
                  'unlocks': ['ES rate 2'],
                  'rect': pygame.Rect((220, 1038, 32, 32)),
                  'action tags': ['eat']},
    'ES rate 2': {'text': 'II',
                  'log text': 'People love it when you eat next to the microphone!',
                  'font size': 15,
                  'full text': 'Eat even more, Tony!',
                  'status': 'locked',
                  'costs': {'cash': 300},
                  'unlocks': ['ES rate 3'],
                  'rect': pygame.Rect((262, 1038, 32, 32)),
                  'action tags': ['eat']},
    'ES rate 3': {'text': 'III',
                  'log text': 'You now have a live-in chef! Bon ape tit!',
                  'font size': 15,
                  'full text': 'Eat even more, Tony!',
                  'status': 'locked',
                  'costs': {'cash': 400},
                  'rect': pygame.Rect((304, 1038, 32, 32)),
                  'action tags': ['eat']},
    'green screen': {'text': 'Green Screen',
                     'log text': 'You now have all the broadcasting technology of...the weather channel!',
                     'font size': 25,
                     'full text': 'Make your content better with a green screen.',
                     'status': 'available',
                     'costs': {'cash': 500},
                     'unlocks': ['guest host'],
                     'rect': pygame.Rect((10, 1080, 200, 100)),
                     'action tags': ['green screen']},
    'self stirring mug': {'text': 'Self-stirring Mug',
                          'log text': "What's in the mug?",
                          'font size': 25,
                          'full text': 'Increase your max energy and recharge rate!',
                          'status': 'available',
                          'costs': {'cash': 1000},
                          'rect': pygame.Rect((10, 1190, 200, 100)),
                          'action tags': ['mug']},
    'channel art': {'text': 'Channel Art',
                    'log text': 'Your channel page looks a bit fancier!',
                    'font size': 25,
                    'full text': 'Up your conversion rate with fancy channel art.',
                    'status': 'available',
                    'costs': {'cash': 500},
                    'unlocks': ['CA 1'],
                    'rect': pygame.Rect((10, 1300, 200, 100)),
                    'action tags': ['art']},
    'CA 1': {'text': 'I',
             'log text': 'Your channel page is super fancy, now!',
             'font size': 15,
             'full text': 'Buy fancier channel art.',
             'status': 'locked',
             'costs': {'cash': 1000},
             'unlocks': ['CA 2'],
             'rect': pygame.Rect((220, 1368, 32, 32)),
             'action tags': ['art']},
    'CA 2': {'text': 'II',
             'log text': 'Your channel page is basically the Louvre!',
             'font size': 15,
             'full text': 'Buy fancier channel art.',
             'status': 'locked',
             'costs': {'cash': 2000},
             'rect': pygame.Rect((262, 1368, 32, 32)),
             'action tags': ['art']},
    'fake subscribers': {'text': 'Buy Fake Subscribers',
                         'log text': 'You bought 1,000 fake subs! You may regret that...',
                         'font size': 25,
                         'full text': 'Buy 1,000 fake subscribers. Increases sketchiness. (5 day cooldown)',
                         'status': 'available',
                         'base cooldown': 5,
                         'cooldown': 0,
                         'costs': {'cash': 100},
                         'rect': pygame.Rect((10, 1450, 200, 100)),
                         'action tags': ['repeatable', 'fake subs']},
    'partner': {'text': 'Partner w/ Advertiser',
                'log text': "You've sold out! Good for you!",
                'font size': 25,
                'full text': 'Partner with an advertiser. Lose 5% of subs, but get $1 for each. (5 day cooldown)',
                'status': 'available',
                'base cooldown': 5,
                'cooldown': 0,
                'costs': {'subs'},
                'rect': pygame.Rect((10, 1560, 200, 100)),
                'action tags': ['repeatable', 'partner']},
    'guest host': {'text': 'Guest Host',
                   'log text': "'Corporate' sends you a guest host! Your ego takes a hit!",
                   'font size': 25,
                   'full text': "Just hope Fluff doesn't screw up your OBS setting! This reduces ego.",
                   'status': 'locked',
                   'base cooldown': 5,
                   'cooldown': 0,
                   'costs': {},
                   'rect': pygame.Rect((10, 1670, 200, 100)),
                   'action tags': ['repeatable', 'fluff']},
}
