# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
import packaging.version

Version1_12 = packaging.version.parse('1.12')

Slaves = {
    'debian8': {
        'os': 'linux',
        'matcher': lambda version: version < Version1_12,
    },
    'debian11': {
        'os': 'linux',
        'matcher': lambda version: version >= Version1_12,
    },
    'windows': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
}

