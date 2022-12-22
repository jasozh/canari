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
from .common import Common

import json
import time


@Gtk.Template(resource_path='/com/github/jasozh/Canari/window.ui')
class CanariWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CanariWindow'

    # UI component bindings
    toast_overlay          = Gtk.Template.Child()
    welcome_screen         = Gtk.Template.Child()
    main_screen            = Gtk.Template.Child()
    refresh_tracker        = Gtk.Template.Child()
    add_course_button      = Gtk.Template.Child()
    refresh_courses_button = Gtk.Template.Child()
    select_courses_button  = Gtk.Template.Child()
    delete_course_button   = Gtk.Template.Child()
    course_list_box        = Gtk.Template.Child()

    course_list_box_children = []

    def __init__(self, scraper, **kwargs):
        super().__init__(**kwargs)

        # Window actions
        Common.create_action(self, 'refresh', self.on_refresh_action)
        Common.create_action(self, 'select', self.on_select_action)
        Common.create_action(self, 'delete', self.on_delete_action)

        # Initialize the web scraper
        self.scraper = scraper

        # Initialize last refresh time
        self.last_refresh_time = 0

        # Add persistent timer that checks the time status every second
        GLib.timeout_add_seconds(1, self.periodic_refresh)

        # Initialize screen
        self.refresh_courses(toast=False)

        # Initially hide the delete course button
        self.delete_course_button.hide()

    def on_delete_action(self, widget, _) -> None:
        """
        Callback for the win.delete action
        """
        row = self.course_list_box.get_selected_row()
        if (row):
            if (self.scraper.delete_course(self.course_list_box_children.index(row))):
                self.refresh_courses(toast=False)
            else:
                self.toast_overlay.add_toast(Adw.Toast(title=f"An error occurred while deleting the course"))

    def on_select_action(self, widget, _) -> None:
        """
        Callback for the win.select action. Toggles between "View" and "Edit"
        mode for the course list.
        """
        mode = self.course_list_box.get_selection_mode()
        if (mode == Gtk.SelectionMode.SINGLE):
            self.course_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
            self.delete_course_button.hide()
            self.select_courses_button.set_active(False)
        else:
            self.course_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
            self.delete_course_button.show()
            self.select_courses_button.set_active(True)

    def on_refresh_action(self, widget, _) -> None:
        """Callback for the win.refresh action."""
        self.refresh_courses()

    def periodic_refresh(self) -> bool:
        """
        Callback for the persistent refresh action. Every second, checks to see whether
        the difference in time since the last refresh exceeds 10 minutes. Refreshes if
        this condition is true.

        Returns True to facilitate GLib.timeout_add_seconds()
        """
        # Default limit set to 5 minutes (300 seconds)
        limit = 20

        time_diff = time.time() - self.last_refresh_time
        if time_diff > limit:
            self.refresh_courses()
        else:
            num = int(limit - time_diff)
            mins = str(num // 60)
            secs = str(num % 60)
            if len(secs) < 2:
                secs = f'0{secs}'
            self.refresh_tracker.set_text(f'Next refresh in {mins}:{secs}')

        return True

    def refresh_courses(self, toast=True) -> None:
        """
        Refreshes course statuses in course_list.

        Args:
            toast: a bool, whether or not to show a toast when refreshing
        """
        # Reset last refresh time
        self.last_refresh_time = time.time()

        # Refresh courses
        if (self.scraper.update_course_list()):
            self.show_content(self.scraper.get_course_list())
            self.show_tracked_courses(self.scraper.get_course_list())

            if toast:
                self.toast_overlay.add_toast(Adw.Toast(title=f"Courses refreshed"))
        else:
            self.toast_overlay.add_toast(Adw.Toast(title=f"Error occurred when refreshing courses"))
            Common.notification("Refresh error", "Error occurred when refreshing courses", "dialog-warning")

    def show_content(self, course_list: list) -> None:
        """
        If course_list is empty, show the Welcome Screen. Otherwise, show the
        Main Screen components and relevant headerbar buttons.
        """
        if len(course_list) > 0:
            self.welcome_screen.hide()

            self.main_screen.show()
            self.refresh_courses_button.show()
            self.select_courses_button.show()
        else:
            self.welcome_screen.show()

            self.main_screen.hide()
            self.refresh_courses_button.hide()
            self.select_courses_button.hide()
            self.delete_course_button.hide()

    def show_tracked_courses(self, course_list: list) -> None:
        """
        Adds AdwActionRow children to course_list_box to render tracked courses.
        Each element in course_list is a dict with the following keys:
            name, course_id, url, status, last_update

        The properties of the AdwActionRow are instantiated in the following order:
            icon-name, title, subtitle, child
        """
        # Remove all existing children of course_list_box, reset course_list_box_children
        if len(self.course_list_box_children) > 0:
            for child in self.course_list_box_children:
                self.course_list_box.remove(child)
                # print('Removed child')

            self.course_list_box_children = []

        # Add new children from course_list
        for item in course_list:
            course_row = Adw.ActionRow()

            # icon-name
            if (item['status'] == 'open'):
                course_row.set_icon_name('software-update-urgent-symbolic')
            else:
                course_row.set_icon_name('dialog-error-symbolic')

            # title
            course_row.set_title(f"{item['subject']} {item['course_num']} {item['label']}")
            if (item['status'] == 'open'):
                course_row.set_css_classes(['heading'])

            # subtitle
            course_row.set_subtitle(f"Last updated at {item['last_update']} ({item['prev_status']}).")

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


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Canari'
        self.props.version = "0.1.2"
        self.props.authors = ['Jason Zheng']
        self.props.copyright = '2022 Jason Zheng'
        self.props.logo_icon_name = 'com.github.jasozh.Canari'
        self.props.modal = True
        self.set_transient_for(parent)


@Gtk.Template(resource_path='/com/github/jasozh/Canari/course-editor-dialog.ui')
class CourseEditorDialog(Gtk.ApplicationWindow):
    __gtype_name__ = 'CourseEditorDialog'

    # UI component bindings
    user_list_box = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    subject       = Gtk.Template.Child()
    course_num    = Gtk.Template.Child()
    semester      = Gtk.Template.Child()
    label         = Gtk.Template.Child()
    course_id     = Gtk.Template.Child()

    def __init__(self, parent, scraper):
        super().__init__()

        # Set parent
        self.parent = parent
        self.set_transient_for(self.parent)

        # Window actions
        Common.create_action(self, 'destroy', self.on_destroy_action)
        Common.create_action(self, 'save', self.on_save_action)

        # Initialize the web scraper
        self.scraper = scraper

    def on_destroy_action(self, widget, _) -> None:
        """Callback for the win.destroy action."""
        self.destroy()

    def on_save_action(self, widget, _) -> None:
        """Callback for the win.save action."""
        subject    = self.subject.get_buffer().get_text()
        course_num = self.course_num.get_buffer().get_text()
        semester   = self.semester.get_buffer().get_text()
        label      = self.label.get_buffer().get_text()
        course_id  = self.course_id.get_buffer().get_text()

        course = {
            'subject': subject,
            'course_num': course_num,
            'semester': semester,
            'label': label,
            'course_id': course_id,
            'url': f'https://classes.cornell.edu/browse/roster/{semester}/class/{subject}/{course_num}',
            'status': 'unknown',
            'prev_status': 'unknown',
            'last_update': 'unknown'
        }

        if self.scraper.add_course(course):
            self.destroy()
            self.parent.refresh_courses(toast=False)
        else:
            self.toast_overlay.add_toast(Adw.Toast(title=f"Invalid course data, please try again"))
