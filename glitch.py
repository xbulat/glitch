#!/usr/bin/env python

import fire

from modules import IdracConnector


class GlitchLauncher(object):
    """
    Glitch's command line tool. It brings html and java access to
    any server, also it supports fast login to iDRAC UI and presents asset's details.

    HOST argument may be [ IPMI_ADDRESS ]


    :param host: (required)
    :param user: (optional)
    :param password: (optional)
    """

    @staticmethod
    def java(host, **kwargs):
        """
        This command opens a java-applet with VirtualConsole.
        :param host: (required)
        :param user: (optional)
        :param password: (optional)
        """
        IdracConnector(host=host, **kwargs).open_java_console()

    @staticmethod
    def html(host, **kwargs):
        """
        This command opens a html5 viewer with VirtualConsole.

        There are versions of Idrac that doesn't support a direct access to html5 viewer

        :param host: (required)
        :param user: (optional)
        :param password: (optional)
        """
        IdracConnector(host=host, **kwargs).open_html_console()

    @staticmethod
    def ui(host, **kwargs):
        """
        This command opens a Idrac login page for fast access to the WebUI.

        :param host: (required)
        :param user: (optional)
        :param password: (optional)
        """
        IdracConnector(host=host, **kwargs).open_idrac_ui()


if __name__ == '__main__':
    fire.Fire(GlitchLauncher)
