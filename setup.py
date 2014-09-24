from setuptools import setup, find_packages


setup(
    name='scalafn',
    version='0.0.12',
    author='Konstantin Potapov',
    author_email='phpconf@gmail.com',
    packages=find_packages(),
    license='BSD',
    url='https://github.com/Frozen/scalafn',
    description='Scala like list',
    install_requires=[
        "future",
        "fn"
    ],
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite="tests"
)