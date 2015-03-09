# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from am.factory import PathBuilder
from am.factory import ShellCommand
from buildbot import locks
from buildbot.config import BuilderConfig
from buildbot.process import factory
from buildbot.steps.source.git import Git
from am.amxmodx.slaves import Slaves

pdb_lock = locks.MasterLock("symbolstore")

def CreateBuilder(slave, version, branch):
    name = slave
    if 'display' in Slaves[slave]:
        name = Slaves[slave]['display']

    return BuilderConfig(
        name = '{0}-{1}'.format(name, version),
        builddir = '{0}-{1}'.format(name, version),
        slavename = slave,
        factory = Factory(slave, branch)
    )

def Factory(slave, branch):
    os = Slaves[slave]['os']
    paths = PathBuilder(os)

    bootstrap_argv = ['perl', paths.join('support', 'buildbot', 'bootstrap.pl')]
    build_argv = ['perl', paths.join('support', 'buildbot', 'startbuild.pl')]
    upload_argv = [
        'perl',
        paths.join('support', 'buildbot', 'package.pl'),
        paths.join('..', '..', 'amxxdrop_info'),
    ]

    if 'compiler' in Slaves[slave]:
        bootstrap_argv.append(Slaves[slave]['compiler'])
        build_argv.append(Slaves[slave]['compiler'])

    f = factory.BuildFactory()
    f.addStep(Git(
        repourl = 'https://github.com/alliedmodders/amxmodx.git',
        branch = branch,
        mode = 'incremental',
        submodules = True
    ))
    f.addStep(ShellCommand(
        name            = "bootstrap",
        command         = bootstrap_argv,
        description     = "bootstrapping",
        descriptionDone = "bootstrapped"
    ))
    f.addStep(ShellCommand(
        name            = 'build',
        command         = build_argv,
        description     = 'compiling',
        descriptionDone = 'compiled',
        timeout         = 2400
    ))
    f.addStep(ShellCommand(
        name            = 'upload',
        command         = upload_argv,
        description     = 'packaging',
        descriptionDone = 'uploaded'
    ))
    if os == 'windows':
        symstore_argv = ['perl', paths.join('support', 'buildbot', 'symstore.pl')]
        f.addStep(ShellCommand(
            name            = "symstore",
            command         = symstore_argv,
            description     = "symstore",
            descriptionDone = "symstore",
            locks           = [pdb_lock.access('exclusive')]
        ))
    return f

