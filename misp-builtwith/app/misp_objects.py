#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file should contain any MISP Object classes required by the bot.
# Each class must follow the standard format used by PyMISP for constructing the object.

from pymisp.tools.abstractgenerator import AbstractMISPObjectGenerator

class TrackingIDObject(AbstractMISPObjectGenerator):

    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(TrackingIDObject, self).__init__('tracking-id', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Description of the tracking id.
        if 'description' in self._parameters:
            self.add_attribute('description', value=self._parameters['description'])
        # First time the tracking code was seen.
        first = self._sanitize_timestamp(self._parameters.pop('first-seen', None))
        self.add_attribute('first-seen', value=first)
        # Last time the tracking code was seen.
        last = self._sanitize_timestamp(self._parameters.pop('last-seen', None))
        self.add_attribute('last-seen', value=last)
        # Hostname where the tracking id was found.
        if 'hostname' in self._parameters:
            if isinstance(self._parameters['hostname'], list):
                for i in self._parameters['hostname']:
                    self.add_attribute('hostname', value=i)
            else:
                self.add_attribute('hostname', value=self._parameters['hostname'])
        # Tracking code.
        if 'id' in self._parameters:
            self.add_attribute('id', value=self._parameters['id'])
        # Name of the tracker - organisation doing the tracking and/or analytics.
        if 'tracker' in self._parameters:
            self.add_attribute('tracker', value=self._parameters['tracker'])
        # URL where the tracking id was found.
        if 'url' in self._parameters:
            if isinstance(self._parameters['url'], list):
                for i in self._parameters['url']:
                    self.add_attribute('url', value=i)
            else:
                self.add_attribute('url', value=self._parameters['url'])