"""
Written by John Cooper http://choffee.co.uk
Copyright 2010 John Cooper
See copyright file that comes with this software for full licence

Modified by cgw 2011/11/06
Modified by aramboi 2016/08/16
"""
import gtk
import urllib
import terminatorlib.plugin as plugin
import re

try:
    from searchplugin_config import *
except ImportError:
    SEARCH_ENGINE = 'Google'
    SEARCH_ENGINE_URI = 'https://www.google.com/search?q={}'

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['SearchPlugin']

_spaces = re.compile(" +")


class SearchPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def do_search(self, searchMenu):
        """Launch search for string"""
        if not self.searchstring:
            return
        uri = SEARCH_ENGINE_URI.format(
            urllib.quote_plus(self.searchstring.encode("utf-8")))
        gtk.show_uri(None, uri, gtk.gdk.CURRENT_TIME)

    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.connect('activate', self.do_search)
        if terminal.vte.get_has_selection():
            clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 40:
                displaystring = self.searchstring[:37] + "..."
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
