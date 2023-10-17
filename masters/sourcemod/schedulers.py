# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import *
from buildbot.schedulers import triggerable
from buildbot.changes import filter
import packaging.version

Version1_11 = packaging.version.parse('1.11')

def BuildersForVersion(version):
    builders = [
        'windows-{}'.format(version),
    ]
    if version > Version1_11:
        builders += ['debian11-{}'.format(version)]
    else:
        builders += ['debian9-{}'.format(version)]
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
