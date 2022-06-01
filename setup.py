from setuptools import setup, find_packages

setup(
    name="fsa",
    description="financial services app",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=[
        "click==8.1.3",
        "loguru==0.6.0",
        "pendulum==2.1.2",
        "requests==2.27.1",
        "email-validator==1.2.1",
    ],
    extras_require={
        "dev": [
            "black",
            "jupyterlab",
            "mkdocs-material==8.2.15",
            "mkdocstrings[python]>=0.18",
            "pytest",
            "pylint",
        ]
    },
    entry_points={"console_scripts": ["pcmd=fsa.cli_tests.entrypoint:cli_tests"]},
)
