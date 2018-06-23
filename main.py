from IgnScraper import IgnScraper
from Game import Game

platforms = [
    'ps4', 'xbox-one', 'ps3', 'pc',
    'xbox-360', 'wii', 'wii-u', '3ds',
    'new-nintendo-3ds', 'nds', 'nintendo-switch',
    'vita', 'psp', 'iphone', 'ipad', 'xbox', 'gb', 'gba',
    'n64', 'mac', 'gcn', 'dc', 'ps', 'ps2', 'nng'
]

scraper = IgnScraper('ps4')

scraper.run()

