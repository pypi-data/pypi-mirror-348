from setuptools import setup, find_packages

setup(
    name="hume_api",
    version="0.1.0",
    description="Simple client for Hume API with audio support",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        "websocket-client",
        "pyaudio"
    ],
    python_requires=">=3.7",
    url="https://github.com/yourusername/hume_api",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
