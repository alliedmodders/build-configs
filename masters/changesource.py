# vim: set ts=4 sw=4 sts=4 tw=99 et ft=python :
from buildbot.changes.pb import PBChangeSource

# This hides some descriptive information that Buildbot exposes.
class AMChangeSource(PBChangeSource):
    def __init__(self, *args, **kwargs):
        PBChangeSource.__init__(self, *args, **kwargs)

    def describe(self):
        return "PBChangeSource listener on all-purpose slaveport"
