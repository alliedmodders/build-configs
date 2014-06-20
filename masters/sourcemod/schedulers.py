# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import *
from buildbot.schedulers import triggerable
from buildbot.changes import filter

def BuildersForVersion(version):
    builders = [
        'linux-' + version,
        'windows-' + version,
        'mac-' + version,
    ]
    return builders

class SMScheduler(SingleBranchScheduler):
    def __init__(self, branch, builders):
        super(SMScheduler, self).__init__(
            name            = 'sched-{0}'.format(branch),
            change_filter   = filter.ChangeFilter(branch = branch),
            treeStableTimer = 60,
            builderNames    = builders
        )

class SMForceScheduler(ForceScheduler):
    def __init__(self, branch, builders):
        super(SMForceScheduler, self).__init__(
            name         = 'force-{0}'.format(branch),
            builderNames = builders,
            branch       = FixedParameter(name = 'branch', default = branch),
            revision     = FixedParameter(name = 'branch'),
            repository   = FixedParameter(name = 'repository'),
            project      = FixedParameter(name = 'project'),
            properties = []
        )

def CreateSchedulers(version, branch):
    builders = BuildersForVersion(version)
    return [SMScheduler(branch, builders), SMForceScheduler(branch, builders)]
