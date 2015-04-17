from flask import render_template, session, request, jsonify
from app import app
from schedule_api import *
from datetime import datetime
from datetime import timedelta
import itertools

@app.route('/')
def index():
    options = {}

    options['terms'] = get_terms()

    if not 'backpack' in session:
		backpack = []
		session['backpack'] = backpack

    options['backpack'] = session['backpack']

    return render_template('index.html', **options)

def has_assigned_sections(sections):
    for section in sections:
        if 'Meeting' in section and section['Meeting']['Days']!='TBA' and section['Meeting']['Times']!='TBA':
            return True
    return False

@app.route('/backpack_course/<term>/<school>/<subject>/<course_num>')
def backpack_course(term, school, subject, course_num):

    if not 'backpack' in session:
        backpack = []
        session['backpack'] = backpack

    if not has_assigned_sections(get_sections(term,school,subject,course_num)):
        return 'Class has no assigned sections', 400

    backpack_item = {}
    backpack_item['term'] = term
    backpack_item['school'] = school
    backpack_item['subject'] = subject
    backpack_item['course_num'] = course_num
    # backpack_item['course_title'] = course_title
    # backpack_item['course_description'] = get_course_description(term, school, subject, course_num)
    # backpack_item['sections'] = get_sections(term, school, subject, course_num)

    inBackpack = False;
    for item in session['backpack']:
        if item['course_num'] == backpack_item['course_num'] and item['subject'] == backpack_item['subject'] and item['school'] == backpack_item['school']:
            inBackpack = True
    if not inBackpack:
        session['backpack'].append(backpack_item)
    print session['backpack']

    return ''

@app.route('/backpack_course/delete/<subject>/<course_num>')
def delete_backpack_item(subject, course_num):

    if not 'backpack' in session:
        return ''

    for item in session['backpack']:
        if item['course_num'] == course_num and item['subject'] == subject:
        	session['backpack'].remove(item)
        	print(session['backpack'])
        	return ''

    return ''

@app.route('/get_session/<key>')
def get_session(key):
	return json.dumps(session[key])

@app.route('/clear_backpack')
def clear_backpack():
    del session['backpack']
    return ''

def default(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

API_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
colors = ["#43735D", "#B8CA0C", "#1D3833", "#626589", "#ddaa44"];
NUM_RET = 6

def passes_filters(option):
    # check to make sure section types are unique
    for course in option:
        if len(set([section['SectionType'] for section in course])) != len(course):
            return False

    meetings = []
    for course in option:
        for section in course:
            for meeting in section['meetings']:
                meetings.append(meeting)

    for meeting in meetings:
        if meeting[0].weekday() in session['filters']['no_class_days']:
            return False
        if meeting[0].hour < int(session['filters']['earliestClass']):
            return False
        if meeting[1].hour > int(session['filters']['latestEndTime']):
            return False

    for pair in itertools.combinations(meetings, 2):
        if pair[0][0] == pair[1][1] or pair[0][1] == pair[1][0]:
            pass
        elif (pair[0][0] <= pair[1][0] <= pair[0][1]) or (pair[1][0] <= pair[0][0] <= pair[1][1]):
            return False

    return True

@app.route('/get_schedules')
def get_scheds():
    # datetime equal to midnight on Monday of current week
    current_week = datetime.today()
    current_week = current_week.replace(day=(current_week.day - current_week.weekday()),hour=0,minute=0,second=0,microsecond=0)

    # create list holding sections with meetings containing date_time objects
    to_backpack = []
    for c in session['backpack']:
        sections = [ dict(s.items()+c.items()) for s in get_sections(**c) ]
        section_types = set()
        for section in sections:
            if 'Meeting' not in section:
                continue
            section_types.add(section['SectionType'])
            if not isinstance(section['Meeting'], list):
                section['Meeting'] = [section['Meeting']]
            meetings = []
            for meeting in section['Meeting']:
                days = [meeting['Days'][i:i+2] for i in range(0, len(meeting['Days']), 2)]
                times = [ time.strptime(i.strip(), "%I:%M%p") for i in meeting['Times'].split('-') ]
                for day in days:
                    start = current_week + timedelta(days=API_DAYS.index(day), hours=times[0].tm_hour, minutes=times[0].tm_min)
                    end   = current_week + timedelta(days=API_DAYS.index(day), hours=times[1].tm_hour, minutes=times[1].tm_min)

                    meetings.append((start,end,meeting['Location']))
            section['meetings'] = meetings
        to_backpack.append( list(itertools.combinations(sections, len(section_types))) )

    # create list containing valid course pairing options
    ret = []
    for i in itertools.product(*to_backpack):
        if not passes_filters(i):
            continue

        option = []
        for modder,course in enumerate(i):
            for section in course:
                for meeting in section['meetings']:
                    option.append({
                        'id': 0,
                        'title': '{} {} - {}'.format(section['subject'],section['course_num'],section['SectionNumber']),
                        'description': '{} @ {}'.format(section['SectionType'], meeting[2]),
                        'allDay': False,
                        'start': meeting[0].isoformat(),
                        'end': meeting[1].isoformat(),
                        'backgroundColor': colors[modder % 5],
                    })
        ret.append(option)
        if len(ret) == NUM_RET:
            break

    return json.dumps(ret,indent=4, separators=(',', ': '),sort_keys=True)

@app.route('/filter/<earliestClass>/<latestEndTime>/<sortBy>/<mon>/<tues>/<wed>/<thurs>/<fri>')
def send_filters(earliestClass, latestEndTime, sortBy, mon, tues, wed, thurs, fri):

    if not 'filters' in session:
        filters =[]
        session['filters'] = filters

    filter_item = {}
    filter_item['earliestClass'] = earliestClass
    filter_item['latestEndTime'] = latestEndTime
    filter_item['sortBy'] = sortBy
    filter_item['no_class_days'] = [i for i,d in enumerate((mon,tues,wed,thurs,fri)) if d != 'false']

    session['filters'] = filter_item
    print session['backpack']

    return ''

@app.route('/course_description/<term>/<school>/<subject>/<course_num>/<course_title>')
def course_description(term, school, subject, course_num, course_title):

    options = {}

    options['term'] = term
    options['school'] = school
    options['subject'] = subject
    options['course_num'] = course_num
    options['course_title'] = course_title
    options['course_description'] = get_course_description(term, school, subject, course_num)
    options['sections'] = get_sections(term, school, subject, course_num)

    return render_template('course_description.html', **options)

@app.route('/section/<term>/<school>/<subject>/<course_num>/<course_title>/<section_num>')
def section(term, school, subject, course_num, course_title, section_num):

    options = {}

    options['term'] = term
    options['school'] = school
    options['subject'] = subject
    options['course_num'] = course_num
    options['course_title'] = course_title
    options['course_description'] = get_course_description(term, school, subject, course_num)
    options['section'] = section_num
    options['section_details'] = get_section_details(term, school, subject, course_num, section_num)
    options['meetings'] = get_meetings(term, school, subject, course_num, section_num)
    options['textbook'] = get_textbook(term, school, subject, course_num, section_num)
    options['instructors'] = get_instructors(term, school, subject, course_num, section_num)

    return render_template('section.html', **options)

