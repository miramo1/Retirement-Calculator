import ctypes
import random

'''check resolution to resize app and graph'''
'''return FONTS, GRAPH_WIDTH, GRAPH_HEIGHT, SCREEN_HORIZONTAL_RES'''
def scale_app_size():
        try:
                '''get the horizontal res of user screen'''
                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()
                user_screen_horizontal = user32.GetSystemMetrics(0)
                horizontal_resolution = user_screen_horizontal
        except:
                '''when in doubt, default to 1920'''
                horizontal_resolution = 1920

        '''height adjusted to equal Calculation window, width set to 1.35 height'''

        if horizontal_resolution <= 1440:
                return {'TITLE_FONT':('Helvetica', 14, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 11, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 9, 'bold')}, 710, 505, horizontal_resolution

        elif horizontal_resolution <= 1920:
                return {'TITLE_FONT':('Helvetica', 17, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 13, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 11, 'bold')}, 790, 575, horizontal_resolution

        else:
                return {'TITLE_FONT':('Helvetica', 20, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 15, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 13, 'bold')}, 850, 625, horizontal_resolution

FONTS, GRAPH_WIDTH, GRAPH_HEIGHT, SCREEN_HORIZONTAL_RES = scale_app_size()

DEFAULT_PARAMS = {'STARTING_BALANCE': 100000,
            'INFLATION_PERCENT': 2.5,
            'INTEREST_EARNED': 9,
            'WITHDRAWAL_PERCENT': 6,
            'INITIAL_CONTRIBUTION': 6000,
            'YEARLY_CONTRIBUTION': 2400
}

COLORS = {'NEGATIVE_BAL_COLOR' : "#d41243",
        'POSITIVE_BAL_COLOR' : "#0b6b38",
        'ALT_HIGHLIGHT' : "#F0F3FF",
        'INFLATION_GRAPH_COLOR' : '#483D8B',
        'TEXT_COLOR' : '#1C1A38',
        'BACKGROUND_COLOR' : "white smoke"
}

random_list = ["Greenland Sharks", "Immortal Jellyfish", "Vampires", "Elves", "Tortoises", "Unicorns", "Zombies", "Mermaids", "Fairies", "Dragons", "Dwarves", "Androids", "Giant Sequoias", "Bowhead Whales", "Spaces Marines", "Maiar", "Necrons", "Ents", "Gnomes", "Trolls", "Daleks", "Nibblonians", "Atlanteans", "Wood Nymphs", "Vulcans", "The Borg", "Shai-Hulud", "Leto II Atreides", "Sandworms"]
