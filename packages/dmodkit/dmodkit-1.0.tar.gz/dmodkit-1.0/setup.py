from setuptools import setup, find_packages

setup(
    name='dmodkit',
    version='1.0',
    description='Lightweight Discord moderation toolkit for discord.py bots',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Mocha',
    author_email='ohplot@gmail.com',
    url='https://github.com/mochathehuman/dmodkit',
    packages=find_packages(),
    install_requires=[
        'discord.py>=2.0.0',
        'loggingutil==1.2.2'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
    ],
    include_package_data=True,
    zip_safe=False
)