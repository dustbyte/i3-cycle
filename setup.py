from setuptools import setup

setup(
    name="i3-cycle",
    version="0.6",
    author="Pierre Wacrenier",
    author_email="mota@souitom.org",
    description="Cycle focus through i3 containers",
    url="http://github.com/mota/i3-cycle",
    license="ISC",
    install_requires=["i3-tree"],
    py_modules=["i3_cycle"],
    entry_points={
        "console_scripts": [
            "i3-cycle=i3_cycle:main"
        ]
    }
)
