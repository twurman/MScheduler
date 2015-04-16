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

@app.route('/backpack_course/<term>/<school>/<subject>/<course_num>')
def backpack_course(term, school, subject, course_num):

    if not 'backpack' in session:
        backpack = []
        session['backpack'] = backpack

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

@app.route('/backpack')
def getbackpack():
	return json.dumps(session['backpack'])

@app.route('/clear_backpack')
def clear_backpack():
    del session['backpack']
    return ''


API_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
colors = ["#43735D", "#B8CA0C", "#1D3833", "#626589", "#ddaa44"];
NUM_RET = 6

@app.route('/get_schedules')
def get_scheds():
    current_week = datetime.today()
    current_week = current_week.replace(day=(current_week.day - current_week.weekday()),hour=0,minute=0)

    options = []

    to_backpack = []
    for c in session['backpack']:
        sections = [ dict(s.items()+c.items()) for s in get_sections(**c) ]
        for section in sections:
            if 'Meeting' not in section:
                continue
            if not isinstance(section['Meeting'], list):
                section['Meeting'] = [section['Meeting']]
            meetings = []
            for meeting in section['Meeting']:
                days = [meeting['Days'][i:i+2] for i in range(0, len(meeting['Days']), 2)]
                times = [ time.strptime(i.strip(), "%I:%M%p") for i in meeting['Times'].split('-') ]
                for day in days:
                    start = current_week + timedelta(days=API_DAYS.index(day), hours=times[0].tm_hour, minutes=times[0].tm_min)
                    end   = current_week + timedelta(days=API_DAYS.index(day), hours=times[1].tm_hour, minutes=times[1].tm_min)

                    meetings.append((start,end))
            section['meetings'] = meetings

        to_backpack.append( sections )

    ret = []

    options = list(itertools.product(*to_backpack))
    for i in options[0:NUM_RET]:
        option = []
        for modder, course in enumerate(i):
            for meeting in course['meetings']:
                option.append({
                    'id': 0,
                    'title': ' '.join((course['subject'],course['course_num'])),
                    'allDay': False,
                    'start': meeting[0].isoformat(),
                    'end': meeting[1].isoformat(),
                    'backgroundColor': colors[modder % NUM_RET],
                })
        ret.append(option)

    return json.dumps(ret,indent=4, separators=(',', ': '))

@app.route('/filter/<earliestClass>/<latestEndTime>/<sortBy>/<mon>/<tues>/<wed>/<thurs>/<fri>')
def send_filters(earliestClass, latestEndTime, sortBy, mon, tues, wed, thurs, fri):

    if not 'filters' in session:
        filters =[]
        session['filters'] = filters

    filter_item = {}
    filter_item['earliestClass'] = earliestClass
    filter_item['latestEndTime'] = latestEndTime
    filter_item['sortBy'] = sortBy
    filter_item['monClass'] = mon
    filter_item['tuesClass'] = tues
    filter_item['wedClass'] = wed
    filter_item['thursClass'] = thurs
    filter_item['friClass'] = fri


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

