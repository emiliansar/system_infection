types = [
    'good',
    'bad'
]

colors = {
    'good': (46, 213, 115),
    'bad': (255, 107, 107)
}

names = {
    'good': [
        'delete',
        'antivirus_delete',
        'antivirus_hp',
        'antivirus_heal'
    ],
    'bad': [
        'yandex',
        'pc_virus',
        'keyboard',
        'miner',
        'wot',
        'wow'
    ]
}

figures = {
    'one_cell': [
        ['X']
    ],
    'I': [
        ['X', 'X', 'X', 'X']
    ],
    'O': [
        ['X', 'X'],
        ['X', 'X']
    ],
    'T': [
        ['X', 'X', 'X'],
        ['0', 'X', '0']
    ],
    'L': [
        ['X', '0'],
        ['X', '0'],
        ['X', 'X']
    ],
    'J': [
        ['0', 'X'],
        ['0', 'X'],
        ['X', 'X']
    ],
    'S': [
        ['0', 'X', 'X'],
        ['X', 'X', '0']
    ],
    'Z': [
        ['X', 'X', '0'],
        ['0', 'X', 'X']
    ]
}

# icons = {
#     'good': [
#         'Antivirus-delete.png',
#         'Antivirus-HP.png',
#         'Antivirus-treatment.png',
#         'Delete.png',
#     ],
#     'bad': [
#         'Keyboard.png',
#         'Miner.png',
#         'PC-virus.png',
#         'WoT.png',
#         'WoW.png',
#         'Yandex.png',
#     ]
# }

icons = {
    'delete':           'Antivirus-delete.png',
    'antivirus_delete': 'Delete.png',
    'antivirus_hp':     'Antivirus-HP.png',
    'antivirus_heal':   'Antivirus-treatment.png',
    'yandex':           'Yandex.png',
    'pc_virus':         'PC-virus.png',
    'keyboard':         'Keyboard.png',
    'miner':            'Miner.png',
    'wot':              'WoT.png',
    'wow':              'WoW.png'
}

hp = {
    'delete': 1,
    'antivirus_delete': 1,
    'antivirus_hp': 5,
    'antivirus_heal': 1,
    'yandex': 1,
    'pc_virus': 1,
    'keyboard': 1,
    'miner': 1,
    'wot': 1,
    'wow': 1
}

# size = {
#     'delete': False,
#     'antivirus_delete': True,
#     'antivirus_hp': True,
#     'antivirus_heal': True,
#     'yandex': False,
#     'pc_virus': True,
#     'keyboard': True,
#     'miner': True,
#     'wot': False,
#     'wow': False
# }