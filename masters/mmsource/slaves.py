# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
import packaging.version

Version2_0 = packaging.version.parse('2.0')

Slaves = {
    'linux': {
        'os': 'linux',
        'compiler': 'clang-3.8',
        'matcher': lambda version: version < Version2_0,
    },
    'linux-2.x': {
        'os': 'linux',
        'compiler': 'clang-8',
        'matcher': lambda version: version >= Version2_0,
    },
    'windows': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
    'macos-10.14': {
        'os': 'mac',
        'display': 'mac',
        'matcher': lambda version: version < Version2_0,
    },
}

