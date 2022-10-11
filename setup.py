from setuptools import setup

setup(
    name='cleancsv',
    version='0.1.0',
    py_modules=['cli', 'cleancsv', 'tx'],
    # py_modules=['cleancsv'],
    # packages=['cli'],
    # include_package_data=True,
    install_requires=[
        'Click',
        'psycopg2',
        'IPython' # DEBUG
        # 'sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'cleancsv = cli:cli',
        ],
    },
)
