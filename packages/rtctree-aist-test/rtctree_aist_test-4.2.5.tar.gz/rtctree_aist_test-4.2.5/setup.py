#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.build import build
from setuptools.command.install import install

build.sub_commands.append(('build_idl', None))
install.sub_commands.append(('install_idl', None))

setup()

