from functools import partial

from buildbot.status.web.auth import AuthBase
from buildbot.status.web.auth import IAuth
from buildbot.status.web.authz import Authz
from repoze.who.plugins.x509 import X509Identifier
from zope.interface import implements

SUBJECT_DN_KEY = 'SSL_CLIENT_S_DN'
VERIFY_KEY = 'SSL_CLIENT_VERIFY'
LOGIN_FIELD = 'CN'


class _DummyAuth(AuthBase):
    implements(IAuth)

    def authenticate(self, user, passwd):
        return False


def _env(request, subject_dn_key=SUBJECT_DN_KEY, verify_key=VERIFY_KEY,
         **kwargs):
    env = {}
    for header in [subject_dn_key, verify_key]:
        env[header] = request.requestHeaders.getRawHeaders(header, [None])[-1]
    return env


def _get_user(request, **kwargs):
    identifier = X509Identifier(**kwargs)
    credentials = identifier.identify(_env(request, **kwargs))
    if credentials:
        return credentials['login']
    return ''


def _patch_request(f, **kwargs):
    def wrapped(request):
        getUser = request.getUser
        try:
            request.getUser = partial(_get_user, request, **kwargs)
            return f(request)
        finally:
            request.getUser = getUser
    return wrapped


class X509Authz(Authz):
    def __init__(self, subject_dn_key=SUBJECT_DN_KEY, verify_key=VERIFY_KEY,
                 login_field=LOGIN_FIELD, **kwargs):
        kwargs['auth'] = _DummyAuth()
        kwargs['useHttpHeader'] = True
        kwargs['httpLoginUrl']= False

        super(X509Authz, self).__init__(**kwargs)

        kwargs = {
            'subject_dn_key': subject_dn_key,
            'verify_key': verify_key,
            'login_field': login_field,
        }

        self.authenticated = _patch_request(self.authenticated, **kwargs)
        self.getUsername = _patch_request(self.getUsername, **kwargs)
        self.getUsernameHTML = _patch_request(self.getUsernameHTML, **kwargs)
        self.getUsernameFull = _patch_request(self.getUsernameFull, **kwargs)
