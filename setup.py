from setuptools import setup

setup(
    name="i3-cycle",
    version="0.4",
    author="Pierre Wacrenier",
    author_email="mota@souitom.org",
    description="Scipt to manage i3 resources in a cycle fashion",
    url="http://github.com/mota/i3-cycle",
    license="ISC",
    install_requires=["i3-py==0.6.4"],
    py_modules=["i3_cycle"],
    entry_points={
        "console_scripts": [
            "i3-cycle=i3_cycle:main"
        ]
    }
)
