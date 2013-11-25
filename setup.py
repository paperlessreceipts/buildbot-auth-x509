from setuptools import find_packages
from setuptools import setup


setup(name='buildbot-auth-x509',
      version='0.0.1',
      description='X.509 authentication support for Buildbot',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      setup_requires=['ez-setup'],
      install_requires=['buildbot', 'repoze.who-x509'],
      )
