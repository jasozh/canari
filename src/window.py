# window.py
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

from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/com/github/jasozh/Canari/window.ui')
class CanariWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CanariWindow'

    welcome_screen = Gtk.Template.Child()
    main_screen = Gtk.Template.Child()
    actionrow = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.welcome_screen.hide()
        self.main_screen.show()
        # self.actionrow.add_suffix(Gtk.Label(label="Test"))
        # self.actionrow.add_prefix(Gtk.Button(label="Test", icon_name="open-menu-symbolic"))


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'canari'
        self.props.version = "0.1.0"
        self.props.authors = ['Jason Zheng']
        self.props.copyright = '2022 Jason Zheng'
        self.props.logo_icon_name = 'com.github.jasozh.Canari'
        self.props.modal = True
        self.set_transient_for(parent)
