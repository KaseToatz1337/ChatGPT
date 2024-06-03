from setuptools import setup

setup(
    name="ChatGPT",
    version="1.3",
    description="ChatGPT Playwright",
    author="KaseToatz1337",
    packages=["chatgpt"],
    install_requires=["playwright", "html2text"]
)