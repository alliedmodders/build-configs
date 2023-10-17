# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from am.factory import PathBuilder
from am.factory import ShellCommand
from buildbot import locks
from buildbot.config import BuilderConfig
from buildbot.process import factory
from buildbot.steps.source.git import Git
from am.sourcemod.slaves import Slaves

pdb_lock = locks.MasterLock("symbolstore")

def CreateBuilder(slave, version, branch):
    name = slave
    if 'display' in Slaves[slave]:
        name = Slaves[slave]['display']

    return BuilderConfig(
        name = '{0}-{1}'.format(name, version),
        builddir = '{0}-{1}'.format(name, version),
        slavename = slave,
        factory = SMFactory(slave, branch)
    )

def SMFactory(slave, branch):
    os = Slaves[slave]['os']
    paths = PathBuilder(os)

    if os == 'windows':
        python_cmd = 'C:\\Python38\\Python.exe'
        hl2sdk_root = 'H:\\'
        common = 'D:\\Scripts\\common'
    elif os == 'linux':
        python_cmd = 'python3'
        hl2sdk_root = '/hgshare'
        common = '/home/builds/common'
    elif os == 'mac':
        python_cmd = 'python3'
        hl2sdk_root = '/Volumes/hgshare'
        common = '/Users/builds/slaves/common'

    bootstrap_argv = [
        python_cmd,
        paths.join('tools', 'buildbot', 'bootstrap.py'),
        '--config', slave,
        '--hl2sdk-root', hl2sdk_root,
        '--python-cmd', python_cmd,
        '--mms-path', paths.join(common, 'mmsource-master'),
    ]
    build_argv = ['perl', paths.join('tools', 'buildbot', 'startbuild.pl')]
    upload_argv = [
        'perl',
        paths.join('tools', 'buildbot', 'package.pl'),
        paths.join('..', '..', 'smdrop_info'),
    ]

    f = factory.BuildFactory()
    f.addStep(Git(
        repourl = 'https://github.com/alliedmodders/sourcemod',
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
        symstore_argv = ['perl', paths.join('tools', 'buildbot', 'symstore.pl')]
        f.addStep(ShellCommand(
            name            = "symstore",
            command         = symstore_argv,
            description     = "symstore",
            descriptionDone = "symstore",
            locks           = [pdb_lock.access('exclusive')]
        ))
    return f
