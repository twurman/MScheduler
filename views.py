from flask import render_template, session, request, jsonify
from app import app
from schedule_api import *

@app.route('/')
def index():
    options = {}

    options['terms'] = get_terms()

    return render_template('index.html', **options)

@app.route('/backpack_course/<term>/<school>/<subject>/<course_num>/<course_title>')
def backpack_course(term, school, subject, course_num, course_title):

	if not 'backpack' in session:
		backpack = []
		session['backpack'] = backpack

	backpack_item = {}

	backpack_item['term'] = term
	backpack_item['school'] = school
	backpack_item['subject'] = subject
	backpack_item['course_num'] = course_num
	backpack_item['course_title'] = course_title
	# backpack_item['course_description'] = get_course_description(term, school, subject, course_num)
	# backpack_item['sections'] = get_sections(term, school, subject, course_num)

	session['backpack'].append(backpack_item)
	print session['backpack']

	options= {}
	return render_template('index.html', **options)

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

