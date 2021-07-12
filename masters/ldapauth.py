from zope.interface import implements
from buildbot.status.web import auth

class LDAPAuth(auth.AuthBase):
    implements(auth.IAuth)
    """Implement a synchronous authentication with an LDAP directory."""

    basedn = ""
    """Base DN (Distinguished Name): the root of the LDAP directory tree

    e.g.: ou=people,dc=subdomain,dc=company,dc=com"""

    binddn = ""
    """The bind DN is the user on the external LDAP server permitted to
    search the LDAP directory.  You can leave this empty."""

    passwd = ""
    """Password required to query the LDAP server.  Leave this empty if
    you can query the server without password."""

    host = ""
    """Hostname of the LDAP server"""

    search = ""
    """Template string to use to search the user trying to login in the
    LDAP directory"""

    groupdn = ""
    """ Limit access to users in the specfified group"""

    def __init__(self, host, basedn, binddn="", passwd="",
                 groupdn="", search="(uid=%s)"):
        """Authenticate users against the LDAP server on C{host}.

        The arguments are documented above."""
        self.host = host
        self.basedn = basedn
        self.binddn = binddn
        self.passwd = passwd
        self.groupdn = groupdn
        self.search = search

        self.search_conn = None
        self.connect()

    def connect(self):
        """Setup the connections with the LDAP server."""
        import ldap
        # Close existing connections
        if self.search_conn:
            self.search_conn.unbind()
        # Connection used to locate the users in the LDAP DB.
        self.search_conn = ldap.initialize(self.host)
        self.search_conn.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
        self.search_conn.start_tls_s()
        self.search_conn.bind_s(self.binddn, self.passwd,
                                ldap.AUTH_SIMPLE)

    def authenticate(self, login, password):
        """Authenticate the C{login} / C{password} with the LDAP server."""
        import ldap
        # Python-LDAP raises all sorts of exceptions to express various
        # failures, let's catch them all here and assume that if
        # anything goes wrong, the authentication failed.
        try:
            res = self._authenticate(login, password)
            if res:
                self.err = ""
            return res
        except ldap.LDAPError, e:
            self.err = "LDAP error: " + str(e)
            return False
        except:
            self.err = "unknown error"
            return False

    def _authenticate(self, login, password):
        import ldap
        # Search the login in the LDAP DB
        try:
            result = self.search_conn.search_s(self.basedn,
                                               ldap.SCOPE_SUBTREE,
                                               self.search % login,
                                               ['objectclass'], 1)
        except ldap.SERVER_DOWN:
            self.err = "LDAP server seems down"
            # Try to reconnect...
            self.connect()
            # FIXME: Check that this can't lead to an infinite recursion
            return self.authenticate(login, password)

        # Make sure we found a single user in the LDAP DB
        if not result or len(result) != 1:
            self.err = "user not found in the LDAP DB"
            return False

        # Make sure user is in the right group
        result = self.search_conn.search_ext_s(self.basedn,
                                            ldap.SCOPE_ONELEVEL,
                                            self.search % login,
                                            ['memberOf'],
                                            sizelimit=1)

        if not result or len(result) != 1:
            self.err = "user not a member of %s" % self.groupdn
            return False                         

        grp_list = result[0][1]['memberOf']
        ingroup = False
        for dn in grp_list:
            if dn == self.groupdn:
                ingroup = True
                break

        if not ingroup:
            self.err = "user not a member of %s" % self.groupdn
            return False

        # Connection used to authenticate users with the LDAP DB.
        auth_conn = ldap.initialize(self.host)
        auth_conn.start_tls_s()
	# DN associated to this user
        ldap_dn = result[0][0]
        #log.msg('using ldap_dn = ' + ldap_dn)
        # Authenticate the user
        try:
            auth_conn.bind_s(ldap_dn, password, ldap.AUTH_SIMPLE)
        except ldap.INVALID_CREDENTIALS:
            self.err = "invalid credentials"
            return False
        auth_conn.unbind()
        return True

    def getUserInfo(self, user):
        import ldap
	try:
            result = self.search_conn.search_s(self.basedn,
                                               ldap.SCOPE_ONELEVEL,
                                               self.search % user,
                                              ['cn'])
            name = result[0][1]['cn'][0]
	    if name in [None, '', ' ']:
                name = user
        except:
            name = user
        return dict(userName=user, fullName=name, email=user, groups=[ user ])

