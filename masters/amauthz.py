from twisted.internet import defer
from buildbot.status.web.auth import IAuth
from buildbot.status.web.authz import Authz
from buildbot.status.web.session import SessionManager

COOKIE_KEY = "BuildBotSession"

class AMAuthz(Authz):
    def __init__(self, *args, **kwargs):
        Authz.__init__(self, *args, **kwargs)

    def setCookiePath(self, path):
        self.cookiePath = path

    def login(self, request):
        """Login one user, and return session cookie"""
        if self.authenticated(request):
            return defer.succeed(False)

        user = request.args.get("username", ["<unknown>"])[0]
        passwd = request.args.get("passwd", ["<no-password>"])[0]
        if user == "<unknown>" or passwd == "<no-password>":
            return defer.succeed(False)
        if not self.auth:
            return defer.succeed(False)
        d = defer.maybeDeferred(self.auth.authenticate, user, passwd)
        def check_authenticate(res):
            if res:
                cookie, s = self.sessions.new(user, self.auth.getUserInfo(user))
                request.addCookie(COOKIE_KEY, cookie, expires=s.getExpiration(), secure=True, path=self.cookiePath)
                request.received_cookies = {COOKIE_KEY:cookie}
                return cookie
            else:
                return False
        d.addBoth(check_authenticate)
        return d

