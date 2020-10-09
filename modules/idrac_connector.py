import os
import time

import requests
from selenium import webdriver
from splinter import Browser

from .view_set import ViewSet
from selenium.common.exceptions import ElementClickInterceptedException


class IdracConnector:
    JNLP_FILE = '/tmp/idrac_viewer.jnlp'
    DEFAULT_IDRAC_USER = 'root'
    DEFAULT_IDRAC_PASS = 'calvin'

    REQUEST_TIMEOUT = 2

    _browser = None

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__idrac_credentials = self.ensure_idrac_credentials()

    @property
    def idrac_user(self):
        return self.__idrac_credentials['idrac']['idrac_user']

    @property
    def idrac_password(self):
        return self.__idrac_credentials['idrac']['idrac_password']

    @property
    def idrac_address(self):
        return self.__idrac_credentials['asset']['ipmi_address']

    @property
    def idrac_credentials(self):
        return {
            'host': self.idrac_address,
            'user': self.idrac_user,
            'password': self.idrac_password,
        }

    def ensure_idrac_credentials(self):
        credentials = {
            'asset': {
                'ipmi_address': self.__kwargs.get('host'),
            },
            'idrac': {
                'idrac_user': self.__kwargs.get('user', self.DEFAULT_IDRAC_USER),
                'idrac_password': self.__kwargs.get('password', self.DEFAULT_IDRAC_PASS),
            }
        }

        return credentials

    @property
    def has_direct_htmlviewer(self):
        requests.packages.urllib3.disable_warnings()
        http_session = requests.session()

        try:
            http_call = http_session.get(
                "https://{}/sysmgmt/2015/bmc/info".format(self.idrac_address),
                verify=False,
                timeout=self.REQUEST_TIMEOUT,
                allow_redirects=False,
            )

            return http_call.status_code in [401, 200]

        except Exception:
            return False

    def _htmlviewer_uri(self):
        return ("https://{host}"
                "/restgui/html5viewer.html"
                "?ip={host}"
                "&kvmport=5900"
                "&title=VirtualConsole"
                "&ST1={user}"
                "&ST2={password}"
                "&F1=1"
                "&vm=1"
                "&chat=1"
                "&custom=0").format(**self.idrac_credentials)

    def open_java_console(self):
        ViewSet(
            template_file='viewer.jnlp.template',
            data=self.idrac_credentials,
            output_file=self.JNLP_FILE
        ).write()

        os.system("$(which javaws ) " + self.JNLP_FILE)

    @property
    def browser(self):
        """Uses class variable to prevent browser closing"""
        if not IdracConnector._browser:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])

            IdracConnector._browser = Browser('chrome', options=options)

        return IdracConnector._browser

    def open_html_console(self):
        if self.has_direct_htmlviewer:
            self.browser.visit(self._htmlviewer_uri())
        else:
            print(
                "The version doesn't support a direct access to KVM HTML5 viewer.\n"
                "Please try 'java' or 'ui' command"
            )

    def login_to_idrac9(self):
        try:
            self.browser.fill('username', self.idrac_user)
            self.browser.find_by_name('password').first.click()
            self.browser.fill('password', self.idrac_password)
            self.browser.find_by_css('.cux-button').click()
        except ElementClickInterceptedException:
            print("Cannot found an element")

    def login_to_idrac8(self):
        self.browser.fill('user', self.idrac_user)
        self.browser.fill('password', self.idrac_password)
        self.browser.execute_script('frmSubmit()')

    def open_idrac_ui(self):
        self.browser.visit('https://' + self.idrac_address)

        while 'iDRAC' not in self.browser.title:
            time.sleep(1)

        if 'iDRAC9' in self.browser.title:
            self.login_to_idrac9()
        elif 'iDRAC8' in self.browser.title:
            self.login_to_idrac8()
        else:
            print('Autologin is not supported for this version of WebUI')
