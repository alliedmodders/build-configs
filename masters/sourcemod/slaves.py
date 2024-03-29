# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
import packaging.version

Version1_10 = packaging.version.parse('1.10')
Version1_11 = packaging.version.parse('1.11')

Slaves = {
    'debian9': {
        'os': 'linux',
        'matcher': lambda version: version <= Version1_11,
    },
    'debian11': {
        'os': 'linux',
        'matcher': lambda version: version > Version1_11,
    },
    'win32-msvc12': {
        'os': 'windows',
        'display': 'windows',
        'flags': {
            'max_builds': 1,
        },
    },
}
