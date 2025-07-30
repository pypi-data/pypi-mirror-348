from setuptools import setup, find_packages

setup(
    name="updogfx",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,  # This enables inclusion of data files as per MANIFEST.in
    install_requires=[
        "Flask",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "updogfx = updogfx.app:main",
        ],
    },
    package_data={
        "updogfx": ["templates/*.html"],  # Include HTML templates
    },
)
