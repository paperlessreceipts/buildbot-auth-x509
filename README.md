# buildbot-auth-x509

X.509 authentication support for Buildbot.


## Setup

    python setup.py install


## Usage

In Buildbot master.cfg:

    from buildbot_auth_x509 import X509Authz
    authz=X509Authz(
        forceBuild='auth', # only authenticated users
        pingBuilder=True, # but anyone can do this
    )
    c['status'].append(WebStatus(http_port=8080, authz=authz))

Note that `auth`, `useHttpHeader` and `httpLoginUrl` are ignored.

In nginx config:

    proxy_set_header SSL_CLIENT_S_DN $ssl_client_s_dn;
    proxy_set_header SSL_CLIENT_VERIFY $ssl_client_verify;


## Settings

Apart from the standard `Authz` settings the `X509Authz` class accepts the
following:

* `subject_dn_key` - the name of the header containing the Subject DN (default:
                     `SSL_CLIENT_S_DN`),
* `verify_key` - the name of the header containing the result of certificate
                 verification (default: `SSL_CLIENT_VERIFY`),
* `login_field` - the field of the Subject DN that will be used to identify the
                  user (default: `CN`).
