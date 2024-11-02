# This file is part of Trackma.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from gi import require_version
from gi.repository import GObject, Gdk, Gtk

try:
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except ImportError:
    try:
        from gi.repository import AppIndicator3 as AppIndicator
    except ImportError:
        from gi.repository import AppIndicator

from trackma import utils

require_version("Gdk", "3.0")


class TrackmaStatusIcon(Gtk.StatusIcon):
    __gtype_name__ = "TrackmaStatusIcon"

    __gsignals__ = {
        "hide-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "about-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "quit-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        self.indicator = AppIndicator.Indicator.new(
            "Trackma GTK",
            utils.DATADIR + "/icon.png",
            AppIndicator.IndicatorCategory.OTHER,
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.set_name("Trackma GTK")
        self.menu_setup()
        self.indicator.set_menu(self.menu)
        self.menu.show_all()

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.mb_show = Gtk.MenuItem(label="Show/Hide")
        self.mb_show.connect("activate", self._tray_status_event)

        self.mb_about = Gtk.MenuItem(label="About")
        self.mb_about.connect("activate", self._on_mb_about)

        self.quit_item = Gtk.MenuItem(label="Quit")
        self.quit_item.connect("activate", self._on_mb_quit)

        self.menu.append(self.mb_show)
        self.menu.append(self.mb_about)
        self.menu.append(self.quit_item)

    def _tray_status_event(self, _widget):
        self.emit("hide-clicked")

    # def _tray_status_menu_event(self, _icon, button, time):
    #     # Called when the tray icon is right-clicked
    #     menu = Gtk.Menu()
    #     mb_show = Gtk.MenuItem("Show/Hide")
    #     mb_about = Gtk.ImageMenuItem(
    #         "About", Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
    #     )
    #     mb_quit = Gtk.ImageMenuItem(
    #         "Quit", Gtk.Image.new_from_icon_name("application-exit", Gtk.IconSize.MENU)
    #     )
    #
    #     mb_show.connect("activate", self._tray_status_event)
    #     mb_about.connect("activate", self._on_mb_about)
    #     mb_quit.connect("activate", self._on_mb_quit)
    #
    #     menu.append(mb_show)
    #     menu.append(mb_about)
    #     menu.append(Gtk.SeparatorMenuItem())
    #     menu.append(mb_quit)
    #     menu.show_all()
    #
    #     menu.popup(None, None, None, self._pos, button, time)

    def _on_mb_about(self, menu_item):
        self.emit("about-clicked")

    def _on_mb_quit(self, menu_item):
        self.emit("quit-clicked")

    def main(self):
        self.status_icon = TrackmaStatusIcon()
        Gtk.main()

    @staticmethod
    def _pos(menu, icon):
        return Gtk.StatusIcon.position_menu(menu, icon)

    @staticmethod
    def is_tray_available():
        # return not Gdk.Display.get_default().get_name().lower().startswith("wayland")
        # Icon tray isn't available in Wayland

        # Always returning true to bypass the issue
        return True
