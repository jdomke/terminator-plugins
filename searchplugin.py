"""
Written by John Cooper http://choffee.co.uk
Copyright 2010 John Cooper
See copyright file that comes with this software for full licence

Modified by cgw 2011/11/06
Modified by aramboi 2016/08/16
Modified by jdomke 2017/09/01
"""
from urllib import quote
from sys import exit
try:
    from gi import require_version
    require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except ImportError:
    print('You need Gtk 3.0+ to run this SearchPlugin.')
    exit(1)
from terminatorlib.plugin import MenuItem
from re import compile

try:
    from searchplugin_config import *
except ImportError:
    SEARCH_ENGINE = 'Google'
    SEARCH_ENGINE_URI = 'https://www.google.com/search?q={}'

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['SearchPlugin']

_spaces = compile(" +")


class SearchPlugin(MenuItem):
    capabilities = ['terminal_menu']

    def do_search(self, searchMenu):
        """Launch search for string"""
        if not self.searchstring:
            return
        uri = SEARCH_ENGINE_URI.format(
            urllib.quote_plus(self.searchstring.encode("utf-8")))
        Gtk.show_uri(None, uri, Gdk.CURRENT_TIME)

    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = Gtk.ImageMenuItem(Gtk.STOCK_FIND)
        item.connect('activate', self.do_search)
        if terminal.vte.get_has_selection():
            clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 16:
                displaystring = self.searchstring[:13] + "..."
            else:
                displaystring = self.searchstring
            item.set_label(
                "Search {} for \"{}\"".format(SEARCH_ENGINE, displaystring))
            item.set_sensitive(True)
        else:
            item.set_label("Search {}".format(SEARCH_ENGINE))
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        menuitems.append(item)
