import json
import time
import requests

class ScheduleApiError(Exception):
    '''
    Raised if there is an error with the schedule API.
    '''
    def __init__(self, message=None):
        self.message = message

# The base API endpoint
base_url = 'http://umich-schedule-api.herokuapp.com'

# the amount of time to wait for the schedule API
timeout_duration = 25


def get_data(relative_path):
    '''
    Gets data from the schedule API at the specified path.
    Will raise a ScheduleApiError if unsuccessful.
    Assumes API will return JSON, returns as a dictionary.
    '''

    timeout_at = time.time() + timeout_duration

    while time.time() < timeout_at:
        r = requests.get(base_url + relative_path)
        if r.status_code == 200:
            return json.loads(r.text)

    raise ScheduleApiError("schedule api error for url: {0}".format(relative_path))

def get_terms():
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('TermCode', 'TermDescr', 'TermShortDescr')
    '''
    return get_data('/get_terms')

def get_schools(term):
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('SchoolDescr', 'SchoolCode', 'SchoolShortDescr')
    '''
    return get_data('/get_schools?term_code=' + term)

def get_subjects(term, school):
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('SubjectShortDescr', 'SubjectCode', 'SubjectDescr')
    '''
    return get_data('/get_subjects?term_code=' + term + '&school=' + school)

def get_catalog_numbers(term, school, subject):

    return get_data('/get_catalog_numbers?term_code=' + term + '&school=' + school + '&subject=' + subject)

def get_course_description(term, school, subject, catalog_num):

    return get_data('/get_course_description?term_code=' + term + '&school=' + school
                        + '&subject=' + subject + '&catalog_num=' + catalog_num)

def get_sections(term, school, subject, course_num):

    return get_data('/get_sections?term_code=' + term + '&school=' + school
                        + '&subject=' + subject + '&catalog_num=' + course_num)

def get_section_details(term, school, subject, catalog_num, section_num):

    return get_data('/get_sections?term_code=' + term + '&school=' + school + '&subject=' + subject
                        + '&catalog_num=' + catalog_num + '&section_num=' + section_num)

def get_meetings(term, school, subject, catalog_num, section_num):

    return get_data('/get_meetings?term_code=' + term + '&school=' + school + '&subject=' + subject
                        + '&catalog_num=' + catalog_num + '&section_num=' + section_num)

def get_textbook(term, school, subject, catalog_num, section_num):

    return get_data('/get_textbooks?term_code=' + term + '&school=' + school + '&subject=' + subject
                        + '&catalog_num=' + catalog_num + '&section_num=' + section_num)

def get_instructors(term, school, subject, catalog_num, section_num):

    return get_data('/get_instructors?term_code=' + term + '&school=' + school + '&subject=' + subject
                        + '&catalog_num=' + catalog_num + '&section_num=' + section_num)




