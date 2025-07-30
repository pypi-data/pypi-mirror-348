# -*- coding: utf-8 -*-

from abc import ABC


class IRegisterable(ABC):
    """
    Interface to perform on-demand registrations.
    """

    def register(self):
        """
        Perform required registration steps.
        """
