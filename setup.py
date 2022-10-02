from setuptools import setup

setup(
    name='cleancsv',
    version='0.1.0',
    py_modules=['cli', 'cleancsv'],
    install_requires=[
        'Click',
        'psycopg2'
        # 'sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'cleancsv = cli.cli:cli',
        ],
    },
)
