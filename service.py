#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os

from pprint import PrettyPrinter
from ruamel.yaml.scanner import ScannerError

from extractor import RegistryExtractor


class Service:

    def contextualize(self):

        extractors = self.provision_extractors()
        futures = {extractor.extract() for extractor in extractors}
        done, pending = self.loop.run_until_complete(asyncio.wait(futures))
        pp = PrettyPrinter(indent=4)
        pp.pprint([task.result() for task in done])
        return [task.result() for task in done]

    def provision_extractors(self):

        extractor_directories = os.listdir(RegistryExtractor.FILE_PATH_BASE)

        extractors = set()
        for directory in extractor_directories:
            try:
                extractor = RegistryExtractor(
                    directory, self.problem_name, self.org_name, self.geo_name)
                if extractor.is_enabled:
                    extractors.add(extractor)
            # FileNotFoundError, ScannerError, ValueError
            except Exception as e:
                print(e)  # TODO: Replace with logging

        return extractors

    def __init__(self, loop=None, problem_name=None, org_name=None, geo_name=None):
        self.loop = loop or asyncio.get_event_loop()
        self.problem_name = problem_name
        self.org_name = org_name
        self.geo_name = geo_name
