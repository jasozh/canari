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
    course_list_box = Gtk.Template.Child()
    course_data = [
        {
            'name': 'ENGRG 1028 (CS 2800 AEW) SEM 101',
            'course_id': '19233',
            'next_id': '19234',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/ENGRG/1028',
            'status': 'open',
            'last_update': 'time obj here'
        },
        {
            'name': 'ENGRG 1028 (CS 2800 AEW) SEM 102',
            'course_id': '19234',
            'next_id': 'end',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/ENGRG/1028',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'FREN 1220 DIS 204',
            'course_id': '4064',
            'next_id': '4065',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/FREN/1220',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'CS 2800 DIS 205',
            'course_id': '10595',
            'next_id': '10596',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/CS/2800',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'CS 2800 DIS 212',
            'course_id': '10603',
            'next_id': '10604',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/CS/2800',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'CS 2800 DIS 211 (test of open class)',
            'course_id': '10602',
            'next_id': '10603',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/CS/2800',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'AAS 2620 (test of open class)',
            'course_id': '17500',
            'next_id': 'end',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/AAS/2620',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        {
            'name': 'CS 2110 DIS 214',
            'course_id': '10269',
            'next_id': '10271',
            'url': 'https://classes.cornell.edu/browse/roster/SP22/class/CS/2110',
            'status': 'closed',
            'last_update': 'time obj here'
        },
        # {
        #     'name': '',
        #     'course_id': '',
        #     'next_id': '',
        #     'url': '',
        #     'status': 'open',
        #     'last_update': 'time obj here'
        # },
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.show_content(self.course_data)
        self.show_tracked_courses(self.course_data)

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
