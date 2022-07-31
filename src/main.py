# main.py
#
# Copyright 2022 Jason Zheng
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import CanariWindow, AboutDialog
from .common import Common

class CanariApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.github.jasozh.Canari',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        # App actions
        Common.create_action(self, 'quit', self.on_quit_action)
        Common.create_action(self, 'about', self.on_about_action)
        Common.create_action(self, 'preferences', self.on_preferences_action)

        # App shortcuts
        self.set_accels_for_action("app.quit", ['<primary>q'])
        self.set_accels_for_action("win.refresh", ['<primary>r'])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = CanariWindow(application=self)
        win.present()

    def on_quit_action(self, widget, _):
        """Callback for the app.quit action."""
        self.quit()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutDialog(self.props.active_window)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    # def create_action(self, name, callback, shortcuts=None):
    #     """Add an application action.

    #     Args:
    #         name: the name of the action
    #         callback: the function to be called when the action is
    #           activated
    #         shortcuts: an optional list of accelerators
    #     """
    #     action = Gio.SimpleAction.new(name, None)
    #     action.connect("activate", callback)
    #     self.add_action(action)
    #     if shortcuts:
    #         self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = CanariApplication()
    return app.run(sys.argv)
