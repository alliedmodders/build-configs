# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
Slaves = {
    'linux': {
        'os': 'linux',
        'cc': 'clang-3.8',
        'cxx': 'clang++-3.8',
    },
    'win32-msvc12': {
        'os': 'windows',
        'display': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'osx10.9': {
        'os': 'mac',
        'display': 'mac',
    },
}
