from setuptools import setup, find_packages


def get_readme():
    with open("./readme.md", 'r') as file:
        return file.read()


setup(
    name="project-snap",
    version="1.0.0",
    description="A utility to create Markdown snapshots of project structures for LLMs",
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/still_standing88/project-snap/',
    license='MIT',
    author="still-standing88",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "project-snap=project_snap.__main__:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
    ],
    keywords="project snapshot markdown llm documentation",
)
