from flask import render_template, request, jsonify
from app import app
from schedule_api import *

@app.route('/')
def index():
    options = {}

    options['terms'] = get_terms()

    return render_template('index.html', **options)

@app.route('/schools/<term>')
def schools(term):
	
	options = {}

	options['term'] = term
	options['schools'] = get_schools(term);

	return jsonify(options)

@app.route('/subjects/<term>/<school>')
def subjects(term, school):
	
	options = {}

	options['term'] = term
	options['school'] = school
	options['subjects'] = get_subjects(term, school)

	return render_template('subjects.html', **options)

@app.route('/catalog_numbers/<term>/<school>/<subject>')
def catalog_numbers(term, school, subject):
	
	options = {}

	options['term'] = term
	options['school'] = school
	options['subject'] = subject
	options['catalog_numbers'] = get_catalog_numbers(term, school, subject)

	return render_template('catalog_numbers.html', **options)

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

