# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
import packaging.version

Slaves = {
    'debian11': {
        'os': 'linux',
    },
    'windows': {
        'os': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
}

