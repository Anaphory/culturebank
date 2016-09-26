from setuptools import setup, find_packages


requires = [
    'clld>=2.1.1',
    'clldmpg>=2.0.0',
    'clld-glottologfamily-plugin>=1.2',
    'pyglottolog>=0.1',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock==1.0',
]


setup(name='culturebank',
      version='0.0',
      description='culturebank',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="culturebank",
      entry_points="""\
[paste.app_factory]
main = culturebank:main
""",
      )
