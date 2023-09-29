# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers import forcesched
from buildbot.schedulers import triggerable
from buildbot.changes import filter
import packaging.version

Version2_0 = packaging.version.parse('2.0')

def BuildersForVersion(version):
    builders = [
        'windows-{}'.format(version),
    ]
    if version < Version2_0:
        builders += [
            'linux-{}'.format(version),
            'mac-{}'.format(version),
        ]
    else:
        builders += ['linux-2.x-{}'.format(version)]
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
