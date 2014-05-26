# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from buildbot import buildslave
from buildbot.steps import shell

# Create a slave given a configuration file and name.
def BuildSlave(cfg, name, **kwargs):
    password = kwargs.pop('password', None)
    if password is None:
        password = cfg.slave_password(name)

    return buildslave.BuildSlave(name, password, **kwargs)

# Create a list of slaves from a dictionary.
def CreateSlaves(cfg, slaves):
    slaveList = []
    for name, options in slaves.items():
        kwargs = options.get('flags', {})
        slaveList += [BuildSlave(cfg, name, **kwargs)]
    return slaveList

# Version of os.path given an arbitrary OS.
class PathBuilder(object):
    def __init__(self, os):
        if os == 'windows':
            self.sep_ = '\\'
        else:
            self.sep_ = '/'

    def join(self, *parts):
        return self.sep_.join(parts)

# Helper for ShellCommand() that defaults options like haltOnFailure.
def ShellCommand(name, command, description, descriptionDone, **kwargs):
    if 'haltOnFailure' not in kwargs:
        kwargs['haltOnFailure'] = True

    return shell.ShellCommand(
        name = name,
        command = command,
        description = description,
        descriptionDone = descriptionDone,
        **kwargs
    )
