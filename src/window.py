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
from .tmpdata import course_data


@Gtk.Template(resource_path='/com/github/jasozh/Canari/window.ui')
class CanariWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CanariWindow'

    welcome_screen = Gtk.Template.Child()
    main_screen = Gtk.Template.Child()
    course_list_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.show_content(course_data)
        self.show_tracked_courses(course_data)

    def show_content(self, course_list: list) -> None:
        """
        If course_list is empty, show the Welcome Screen. Otherwise, show the
        Main Screen components
        """
        if len(course_list) > 0:
            self.welcome_screen.hide()
            self.main_screen.show()
        else:
            self.welcome_screen.show()
            self.main_screen.hide()

    def show_tracked_courses(self, course_list: list) -> None:
        """
        Adds AdwActionRow children to course_list_box to render tracked courses.
        Each element in course_list is a dict with the following keys:
            name, course_id, url, status, last_update

        The properties of the AdwActionRow are instantiated in the following order:
            icon-name, title, subtitle, child
        """
        for item in course_list:
            course_row = Adw.ActionRow()

            # icon-name
            if (item['status'] == 'closed'):
                course_row.set_icon_name('dialog-error-symbolic')
            elif (item['status'] == 'open'):
                course_row.set_icon_name('software-update-urgent-symbolic')

            # title
            course_row.set_title(item['name'])
            if (item['status'] == 'open'):
                course_row.set_css_classes(['heading'])

            # subtitle
            course_row.set_subtitle(f'Last updated at {item["last_update"]}.')

            # child
            status_label = Gtk.Label()
            if (item['status'] == 'closed'):
                status_label.set_label(item['status'].title())
            elif (item['status'] == 'open'):
                status_label.set_label(item['status'].upper())

            course_row.add_suffix(status_label)
            # course_row.add_prefix(Gtk.Button(label="Test", icon_name="open-menu-symbolic"))

            self.course_list_box.append(course_row)


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
