from setuptools import setup, find_packages

setup(
    name="blackspammerbd-xd",
    version="1.0.0",
    description="BLACK SPAMMER BD official backup tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="BLACK SPAMMER BD",
    author_email="shawponsp6@gmail.com",
    url="https://github.com/BlackSpammerBd/blackspammerbd-xd",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
