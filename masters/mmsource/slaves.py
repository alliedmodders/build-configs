# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
Slaves = {
    'linux': {
        'os': 'linux',
        'compiler': 'clang-3.8',
    },
    'win32': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'macos-10.14': {
        'os': 'mac',
        'display': 'mac',
        'versions' : [
            '1.11',
            '1.12',
        ]
    },
}

