from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="gptsubtitler",
    version="0.0.10",
    author="extremq",
    author_email="extremqcontact@gmail.com",
    description="Automatically subtitle any video spoken in any language to a language of your choice.",
    install_requires=[
        "transformers>=4.29.1",
        "pywhispercpp>=1.0.8"
    ],
    packages=["gptsubtitler"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts": [
            "gptsubtitler = gptsubtitler.cli:main"
        ]
    },
    long_description=readme(),
    long_description_content_type = "text/markdown"
)