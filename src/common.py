# common.py
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

from gi.repository import GLib, Gio, Notify
import json

class Common():
    """Common methods shared by the application and its windows"""
    def __init__(self):
        pass

    @classmethod
    def create_action(self, object, name, callback):
        """Add an application action.

        Args:
            name: the name of the action
            object: the object that the action should be created for
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        object.add_action(action)

    @classmethod
    def notification(self, title: str, content: str, icon: str) -> None:
        """
        Sends a notification with title, content, and icon. Sample icon strings
        include: "dialog-information", "dialog-error"
        """
        notif = Notify.Notification.new(title, content, icon)
        notif.show()
