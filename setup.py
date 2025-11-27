from setuptools import setup

setup(
    name='Password-Security-Analyzer',
    version='1.0.0',
    description='A comprehensive password security analyzer with breach detection',
    author='Your Name',
    license='MIT',
    packages=[''],
    install_requires=[
        'customtkinter==5.2.2',
        'pyperclip==1.8.2',
        'requests==2.31.0',
    ],
    entry_points={
        'console_scripts': [
            'password-analyzer=main:root.mainloop',
        ],
    },
    python_requires='>=3.8',
)
