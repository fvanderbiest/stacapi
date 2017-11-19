import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster-pastedeploy==0.4.1',
    'pyramid==1.9.1',
    'pyramid-debugtoolbar==4.3',
    'pyramid-jinja2==2.7',
    'pyramid-retry==0.5',
    'pyramid-tm==2.2',
    'SQLAlchemy==1.1.15',
    'transaction==2.1.2',
    'zope.sqlalchemy==0.7.7',
    'waitress==1.1.0',
    'requests==2.18.4',
    'bs4==0.0.1',
    'cornice==2.4.0',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='stacapi',
    version='0.0',
    description='stacapi',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = stacapi:main',
        ],
        'console_scripts': [
            'initialize_stacapi_db = stacapi.scripts.initializedb:main',
            'query = stacapi.scripts.query:main',
        ],
    },
)
