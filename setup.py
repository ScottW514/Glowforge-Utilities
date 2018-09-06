from setuptools import setup, find_packages

setup(
    name='gfutilities',
    description='Glowforge Utilities',
    author='Scott Wiederhold',
    author_email='s.e.wiederhold@gmail.com',
    url='https://github.com/ScottW514/Glowforge-Utilities',
    version='0.5.16',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.txt').read(),
    keywords='Glowforge OpenGlow',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Embedded Systems',
    ],
)
