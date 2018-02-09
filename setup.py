from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = ''.join(f.readlines())


setup(
    name='Yum4FIT_halfdeadpie',
    version='0.3.4',
    description='Level up in your cooking skills',
    long_description=long_description,
    author='Simon Stefunko',
    author_email='s.stefunko@gmail.com',
    keywords='food, yummly, instagram, recipes, game',
    license='Public Domain',
    url='https://github.com/HalfDeadPie/Yum4FIT',
    packages=['yum'],
    package_data = {'yum': ['templates/*.html' , 'static/*', 'mainwindow.ui'], },
    python_requires='~=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Framework :: Flask',
        'Environment :: Console',
        'Environment :: Web Environment'
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'yum = yum.unity:main',
        ],
    },
    install_requires=['Flask', 'click>=6', 'requests>=2.11.1', 'pyqt5-tools', 'InstagramAPI', 'PyQt5'],
    dependency_links=[
        '-e git+https://github.com/LevPasha/Instagram-API-python.git@a5a2bff6755ffa8e92b91a91ee3e5d0719a631e0#egg=instagram_api'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'betamax', 'flexmock'],
)