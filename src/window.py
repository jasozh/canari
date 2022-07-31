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

from gi.repository import Gtk, Adw, GLib, Gio
from .webscraper import WebScraper

import json


@Gtk.Template(resource_path='/com/github/jasozh/Canari/window.ui')
class CanariWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CanariWindow'

    welcome_screen = Gtk.Template.Child()
    main_screen = Gtk.Template.Child()
    course_list_box = Gtk.Template.Child()
    course_list_box_children = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scraper = WebScraper()

        self.show_content(scraper.course_list)
        self.show_tracked_courses(scraper.course_list)
        self.show_tracked_courses(scraper.course_list)

        # self.save_courses_to_user_dir(scraper.course_list)
        self.read_courses_from_user_dir()

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
        # Remove all existing children of course_list_box
        if len(self.course_list_box_children) > 0:
            for child in self.course_list_box_children:
                self.course_list_box.remove(child)
                # print('Removed child')

        # Add new children from course_list
        for item in course_list:
            course_row = Adw.ActionRow()

            # icon-name
            if (item['status'] == 'closed'):
                course_row.set_icon_name('dialog-error-symbolic')
            elif (item['status'] == 'open'):
                course_row.set_icon_name('software-update-urgent-symbolic')

            # title
            course_row.set_title(f"{item['subject']} {item['class_num']} {item['label']}")
            if (item['status'] == 'open'):
                course_row.set_css_classes(['heading'])

            # subtitle
            course_row.set_subtitle(f'Last updated at {item["last_update"]}.')

            # child
            status_label = Gtk.Label()
            if (item['status'] == 'open'):
                status_label.set_label(item['status'].upper())
            else:
                status_label.set_label(item['status'].title())

            course_row.add_suffix(status_label)
            # course_row.add_prefix(Gtk.Button(label="Test", icon_name="open-menu-symbolic"))

            self.course_list_box.append(course_row)
            self.course_list_box_children.append(course_row)

    def get_data_file(self) -> Gio.File:
        """
        Returns a Gio.File object for course_list.json stored in the user data directory
        """
        data_dir = GLib.get_user_data_dir()
        destination = GLib.build_filenamev([data_dir, 'canari', 'course_data.json'])
        destinationFile = Gio.File.new_for_path(destination)

        return destinationFile

    def read_courses_from_user_dir(self) -> list:
        """
        Returns a course list after reading from a JSON file in the user data directory
        """
        destinationFile = self.get_data_file()
        success, contents, tag = destinationFile.load_contents(None)
        json_data = contents.decode()
        course_list = json.loads(json_data)

        print(course_list)
        print('Data successfully loaded')

        return course_list

    def save_courses_to_user_dir(self, course_list: list) -> None:
        """
        Saves course_list as a JSON file to the user data directory:
            /home/<username>/.local/share/canari/course_data.json
            /home/<username>/.var/app/com.github.jasozh.Canari/data/canari/course_data.json
        """
        json_data = json.dumps(course_list, indent = 2)
        print(json_data)
        destinationFile = self.get_data_file()

        # Permissions for any created directories
        # 744 in octal notation means read/write/execute permission for owner,
        # read permissions only for group and world
        PERMISSIONS_MODE = 0o744

        # Creates directories along the way to the destination path file
        if (GLib.mkdir_with_parents(destinationFile.get_parent().get_path(), PERMISSIONS_MODE) == 0):
            success, tag = destinationFile.replace_contents(bytearray(json_data, 'utf-8'), None, False, Gio.FileCreateFlags.REPLACE_DESTINATION, None)

            if success:
                print("Data successfully saved!")
            else:
                print('Error occurred when saving data')
        else:
            print('Error when creating directories for destination file')


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
