# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
Slaves = {
    'linux': {
        'os': 'linux',
        'compiler': '/apps/clang-3.5/bin/clang',
    },
    'win32': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'osx10.9': {
        'os': 'mac',
        'display': 'mac',
    },
}

