import setuptools

setuptools.setup(
    name='highlight-cli',
    version="1.1.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Highlight text within input.',
    license='MIT',
    keywords='highlight,cli,command-line',
    url='https://github.com/talwrii/highlight-cli',
    install_requires=["colorama"],
    packages=["highlight_cli"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['hlcli=highlight_cli.main:main']
    }
)
