# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
Slaves = {
    'linux': {
        'os': 'linux',
        'compiler': 'clang',
    },
    'win32': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'win32-msvc12': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
        'versions': ['1.6'],
    },
    'osx10.9': {
        'os': 'mac',
        'display': 'mac',
    },
}
