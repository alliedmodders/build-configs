# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
Slaves = {
    'linux': {
        'os': 'linux',
        'cc': 'clang-8',
        'cxx': 'clang++-8',
    },
    'win32-msvc12': {
        'os': 'windows',
        'display': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'macos-10.14': {
        'os': 'mac',
        'display': 'mac',
    },
}
