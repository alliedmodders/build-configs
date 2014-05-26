# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers import forcesched
from buildbot.schedulers import triggerable
from buildbot.changes import filter

def BuildersForVersion(version):
    builders = [
        'linux-' + version,
        'win32-' + version,
        'mac-' + version,
    ]
    return builders

class Scheduler(SingleBranchScheduler):
    def __init__(self, branch, builders):
        super(Scheduler, self).__init__(
            name            = 'sched-{0}'.format(branch),
            change_filter   = filter.ChangeFilter(branch = branch),
            treeStableTimer = 60,
            builderNames    = builders
        )

class ForceScheduler(forcesched.ForceScheduler):
    def __init__(self, branch, builders):
        super(ForceScheduler, self).__init__(
            name         = 'force-{0}'.format(branch),
            builderNames = builders,
            branch       = forcesched.FixedParameter(name = 'branch', default = branch),
            revision     = forcesched.FixedParameter(name = 'branch'),
            repository   = forcesched.FixedParameter(name = 'repository'),
            project      = forcesched.FixedParameter(name = 'project'),
            properties = []
        )

def CreateSchedulers(version, branch):
    builders = BuildersForVersion(version)
    return [Scheduler(branch, builders), ForceScheduler(branch, builders)]
