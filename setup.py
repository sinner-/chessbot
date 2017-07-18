""" chessbot
"""

from setuptools import setup, find_packages

setup(
    name='chessbot',
    version='1.0',
    url='https://github.com/sinner-/chessbot',
    author='Sina Sadeghi',
    description='IRC chess bot',
    packages=find_packages(),
    install_requires=[
        'PyNaCl>=1.1.2'
    ],
    entry_points={
        'console_scripts': [
            'chessbot = chessbot.cmd.cli:main',
            'chessbot-admin = chessbot.cmd.admin:main'
        ]},
)
