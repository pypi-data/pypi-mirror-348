from setuptools import setup, find_packages

setup(
    name="updogfx",
    version="0.1.0",
    description="A simple file server inspired by Updog, with reverse SSH support.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="EFXTv",
    author_email="efxtve@gmail.com",
    url="https://github.com/efxtv/updogfx",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.26.0"
    ],
    entry_points={
        "console_scripts": [
            "updogfx=updogfx.app:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
