# webscraper.py
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

from gi.repository import GLib, Gio
import copy as cp
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup

from .common import Common
# from .tmpdata import course_data

class WebScraper():
    _course_list = []

    def __init__(self):
        self.read_courses_from_user_dir()

    def get_course_list(self) -> list:
        return self._course_list

    def add_course(self, course: dict) -> bool:
        """
        Given a course as a dict, adds to self._course_list and saves new course
        to user data dir. Returns whether the operation has succeeded
        """
        new_dict = cp.deepcopy(course)

        # If web scraper request passes, add to course_list, otherwise send error
        if self.get_course_status(course):
            self._course_list.append(new_dict)
            self.save_courses_to_user_dir()
            return True
        else:
            return False

    def delete_course(self, index) -> bool:
        """
        Given an index of course_list, reads data from user data dir, deletes index,
        and saves new list back to user data dir. Returns whether the operation was
        successful
        """
        try:
            assert self._course_list[index]

            self.read_courses_from_user_dir()
            del self._course_list[index]
            self.save_courses_to_user_dir()

            return True

        except:
            return False

    def get_course_status(self, course: dict) -> str:
        """
        Given a course object, sends a request and returns whether the course status
        should be 'open' or 'closed'. A course object is a dict with the following
        keys:
        """
        try:
            page = requests.get(course['url'])
            soup = BeautifulSoup(page.content, "html.parser")

            # Get the <ul> HTML fragment surrounding the course_id in Class Roster
            course_id_location = soup.find(lambda tag: tag.name == 'strong' and course['course_id'] in tag.text)
            parents_gen = course_id_location.parents
            next(parents_gen)
            next(parents_gen)
            fragment = next(parents_gen)

            # Get the <span> class and read open-status
            status_fragment = fragment.find(lambda tag: tag.name == 'span' and tag.has_attr('class') and tag['class'][0] == 'fa')
            status = str(status_fragment['class'][2])

            if (status == 'open-status-open'):
                return 'open'
            elif (status == 'open-status-closed'):
                return 'closed'
            elif (status == 'open-status-warning'):
                return 'waitlist'
            elif (status == 'open-status-archive'):
                return 'archive'
            else:
                return 'error'

        except Exception as err:
            print(f'Exception thrown: {err}')

    def update_course_list(self) -> bool:
        """
        Iterates through course_list and updates status and last_update for each course.
        Returns whether the operation succeeded
        """
        print('Updating course list')

        try:
            for course in self._course_list:
                # Update prev_status
                course['prev_status'] = course['status']

                # Update status
                course['status'] = self.get_course_status(course)

                # Update last_update
                now = datetime.datetime.now()
                formatted_time = datetime.datetime.strftime(now, '%I:%M:%S')
                course['last_update'] = formatted_time

                # If status changed and the old status was not unknown, send notification
                if (course['status'] != course['prev_status'] and course['prev_status'] != 'unknown'):
                    Common.notification(f"{course['subject']} {course['course_num']} {course['label']} is {course['status']}",
                                        f"The course was previously {course['prev_status']}.",
                                        "dialog-information")

            return True

        except Exception as err:
            print(f'Exception thrown: {err}')
            return False

    def get_data_file(self) -> Gio.File:
        """
        Returns a Gio.File object for course_list.json stored in the user data directory
        """
        data_dir = GLib.get_user_data_dir()
        destination = GLib.build_filenamev([data_dir, 'canari', 'course_data.json'])
        destinationFile = Gio.File.new_for_path(destination)

        return destinationFile

    def read_courses_from_user_dir(self) -> bool:
        """
        Returns a course list after reading from a JSON file in the user data directory.
        Returns whether the operation succeeded
        """
        try:
            destinationFile = self.get_data_file()
            success, contents, tag = destinationFile.load_contents(None)
            json_data = contents.decode()
            self._course_list = json.loads(json_data)

            print(self._course_list)
            print('Data successfully loaded')

            return True

        except Exception as err:
            print(err)
            return False

    def save_courses_to_user_dir(self) -> bool:
        """
        Saves course_list as a JSON file to the user data directory:
            GLIB_DATADIR/canari/course_data.json
        """
        json_data = json.dumps(self._course_list, indent = 2)
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
                return True
            else:
                print('Error occurred when saving data')
                return False
        else:
            print('Error when creating directories for destination file')
            return False

