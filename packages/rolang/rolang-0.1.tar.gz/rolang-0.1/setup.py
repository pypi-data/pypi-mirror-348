from setuptools import setup, find_packages

setup(
    name="rolang",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rolang=rolang.interpreter:start_interpreter',
        ],
    },
    author="Rohan",
    author_email="ronk5811@gmail.com",
    description="A simple custom programming language interpreter",
    python_requires='>=3.6',
)
