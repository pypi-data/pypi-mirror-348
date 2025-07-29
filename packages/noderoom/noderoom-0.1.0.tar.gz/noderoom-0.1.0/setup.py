from setuptools import setup, find_packages

setup(
    name="noderoom",
    version="0.1.0",
    author="Henry Jones",
    description="A multi-AI terminal chatroom powered by local models via Ollama.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # or pick another if you're more specific
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'noderoom=noderoom.__main__:main',
        ],
    },
)
