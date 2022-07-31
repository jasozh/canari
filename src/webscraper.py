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

import time
import datetime
import requests
from bs4 import BeautifulSoup

# from .tmpdata import course_data

class WebScraper():
    course_list = []

    def __init__(self, data):
        self.course_list = data

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
            elif (status == 'open-status-archive'):
                return 'archive'
            else:
                return 'error'

        except Exception as err:
            print(f'Exception thrown: {err}')

    def update_course_list(self) -> None:
        """
        Iterates through course_list and updates status and last_update for each course
        """
        print('Updating course list')

        try:
            for course in self.course_list:
                # Update prev_status
                course['prev_status'] = course['status']

                # Update status
                course['status'] = self.get_course_status(course)

                # Update last_update
                now = datetime.datetime.now()
                formatted_time = datetime.datetime.strftime(now, '%I:%M:%S')
                course['last_update'] = formatted_time

        except Exception as err:
            print(f'Exception thrown: {err}')
