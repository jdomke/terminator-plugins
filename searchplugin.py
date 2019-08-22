"""
Written by John Cooper http://choffee.co.uk
Copyright 2010 John Cooper
See copyright file that comes with this software for full licence

Modified by cgw 2011/11/06
Modified by aramboi 2016/08/16
Modified by jdomke 2017/09/01
"""
from urllib import quote_plus
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
    #SEARCH_ENGINE = 'Google'
    #SEARCH_ENGINE_URI = 'https://www.google.com/search?q={}'
    #SEARCH_ENGINE = 'SearX'
    #SEARCH_ENGINE_URI = 'https://searx.me/?q={}&preferences=eJx1Vcuu00AM_RqyiYp4LFhlgQDBlZBA3MJ25Mw4yZDJOIwnbcPX42mTZnpvWTRVXPv4-PjRgDy5yIq88nhUEepqHyYsDFkVkMkdMFSs7a6b6pfxWDjw7QQtVuh3Px8LRxpceimMZagdGjW6qbWeq1922Dnbo-oo9jhzYQeJU2Og03zJAVMkTcPoMGJlJt2nT0sFQ4OMEHRXvSpihwNWxBpCgf42xbcRfWIpFShnfX8tow50ZAypHH7x5sODb6y3ERXrQM6J5ct-__1RQo9BzPK-D6B7Cfj546tYB5KqxfqIrlESTGGAaMnz2ZaIpUQaIrYUZsXoUEf57cznvdbIrD5-e1jxN23QC2_kqre6B3FSjXWYUJuAWDI18QgBS2ODACZoZRPugSAqxaQtuHJAY0GM1oNSB2uQEkBAY-xzp8nz6IA7AUrqJ8-WqHVYinkuYRwzEh8nI_xVix4DJJW01rt4yLK0tpVCgGPutaYW4c-lmEDWbKh-BsjSb33OMa6CbKkymsPEVit1_pKfZvAGT_cobJYWsY92QF4kvLBYEYxt65glA90yTf_LTgeLObXXp6weRjQjyuhcwQf6LclzMiv8NYhkUAKOlIm_4Tzr6abdhfYagjLlSektUQOB6NqJDuoA6bFokAbXHrC0fI_cSr-2sZb-YFyiZujopldNkFWzoDNikfqZInFHPfgNaqGzhWKcB_KyqphbL725lt0EGMDZOuDCYJgHWckwlzGAZydrZ-4VsMqSQkG8kwff1vrnCP5mTLZpLC_F3O3s7Sivb0-KvvJfurSK8MRt6_dfD0POhY-WWcvhyjlo8KHkGCYdp5DoyS1Gr_GMkBqqyWCZHotYGcoG_frt23enmz2ODuo1IkKIY7rNuTCmLQ2ez2Y6fHd39Vzh9Sivt60YMHZkqs-f9sVyImV9qiW-OF_yHcdZ_jYctTZRP-wMhP4fZaJ3Yw=='
    SEARCH_ENGINE = 'DuckDuckGo'
    SEARCH_ENGINE_URI = 'https://duckduckgo.com/?q={}&kae=t&kax=-1&kp=-2&kav=1&kn=1&k1=-1&kk=-1&kaj=m&kam=osm&kak=-1&kaq=-1&kap=-1&kao=-1&kau=-1&kah=wt-wt&kl=wt-wt&k9=81ea4a&kt=n&ka=n&ia=web'

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
            quote_plus(self.searchstring.encode("utf-8")))
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
