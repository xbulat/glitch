### Description ###

Glitch is a tiny command line tool that can help you deal with repetitive work:

* Open and log in to iDrac UI
* Open iDrac virtual console (java or html)

### Usage ###

Launch a VirtualConsole with credentials that are stored in Gartner:
* `glitch.py java <IPMI_ADDRESS>`
* `glitch.py html <IPMI_ADDRESS>`

Also you can specify your own credentials:
* `glitch.py html <IPMI_ADDRESS> --user <USER> --password <PASSWORD>`

Open iDrac UI and login in:
* `glitch.py ui <IPMI_ADDRESS>`

Don't forget to use help:
* `glitch.py --help`
* `glitch.py <CMD> --help`

Due to the `HOST` is required argument the flag `--host` before a value might be skipped.

### Installation ###

#### Python modules ####
It is supporting Python2 and Python3 as well.

```bash
pip install -r requirements.txt
```

#### WebDriver ####
It is using the WebDriver for automatization Browser routines.
In current moment is support only Google Chrome browser.
In this way it has to be presented in the OS.

##### Mac OS X ######
The recommended way is by using [Homebrew](https://brew.sh/):

```bash
brew cask install chromedriver
```

##### Linux #####
Go to the [download page](https://sites.google.com/a/chromium.org/chromedriver/downloads)
on the Chromium project and choose the correct version for your Linux installation


WARNING: You should use the same version of `chromedriver` as your version of the ChromeBrowser

```bash
cd $HOME/Downloads
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

mkdir -p $HOME/bin
mv chromedriver $HOME/bin
echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bash_profile`
```

#### Windows ####
Doesn't support Windows `=(`

### Contacts ####

* [GitHub](https://github.com/xbulat)
