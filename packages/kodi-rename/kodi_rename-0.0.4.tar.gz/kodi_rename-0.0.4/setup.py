# -*- coding: utf-8 -*-
import versioneer
from setuptools import setup

setup(
    packages=["kodiRename"],
    package_data={"kodiRename": ["py.typed"]},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
