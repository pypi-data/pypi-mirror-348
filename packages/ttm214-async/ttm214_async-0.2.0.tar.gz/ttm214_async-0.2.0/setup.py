from setuptools import find_packages, setup

setup(
    name="ttm214_async",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "pyserial>=3.5",
        "pyserial-asyncio>=0.6",
    ],
    author="mochi534",
    author_email="lib654852@gmail.com",
    maintainer="mochi534",
    maintainer_email="lib654852@gmail.com",
    description="TTM214 device control library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mochi534/TTM214_async",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
)
