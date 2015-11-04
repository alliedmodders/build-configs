# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
from am import ldapauth, amauthz
from buildbot.status import html
from buildbot.status import mail
from buildbot.status.builder import SUCCESS, FAILURE

def WebStatus(cfg):
    ldap_conf = cfg.get('ldap')
    ldap = ldapauth.LDAPAuth(
        ldap_conf['host'],
        ldap_conf['basedn'],
        groupdn = ldap_conf['groupdn'],
        search = ldap_conf['search']
    )

    master_admins = cfg.get('master-admins')
    slave_admins = master_admins + cfg.get('slave-admins')

    auth = amauthz.AMAuthz(
        auth = ldap,
        forceBuild = 'auth',
        forceAllBuilds = 'auth',
        pingBuilder = 'auth',
        stopBuild = 'auth',
        stopAllBuilds = 'auth',
        cancelPendingBuild = 'auth',
        gracefulShutdown = lambda u, s: u in slave_admins,
        cleanShutdown = lambda u: u in master_admins
    )
    auth.setCookiePath(cfg.get('url-path'))

    web_conf = cfg.get('web')
    web_args = {}
    if 'github' in web_conf:
        web_args['change_hook_dialects'] = { 'github': {} }
        web_args['change_hook_auth'] = ['file:{0}'.format(web_conf['github'])]

    return html.WebStatus(
        http_port = 'tcp:{0}'.format(web_conf['port']),
        authz = auth,
        **web_args
    )

def MailStatus(cfg, project, **kwargs):
    mail_conf = cfg.get('mail')
    notifier = mail.MailNotifier(
        fromaddr = mail_conf['from'],
        extraRecipients = mail_conf['to'],
        mode = ['failing', 'change'],
        **kwargs
    )

    oldFormatter = notifier.messageFormatter
    def subject_injector(mode, name, build, results, master_status):
        obj = oldFormatter(mode, name, build, results, master_status)
        if results == FAILURE:
            subject = '{0} build broke: {1}'.format(project, name)
        else:
            subject = '{0} build restored: {1}'.format(project, name)
        obj['subject'] = subject
        return obj
    notifier.messageFormatter = subject_injector

    return notifier
