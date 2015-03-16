from flask import render_template, request
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

	return render_template('schools.html', **options)

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
def course_description(term, school, subject, course_num):
	
	options = {}

	options['term'] = term
	options['school'] = school
	options['subject'] = subject
	options['course_num'] = course_num
	options['course_title'] = course_title
	options['course_description'] = get_course_description(term, school, subject, course_num)
	options['sections'] = get_sections(term, school, subject, course_num)

	return render_template('course_description.html', **options)

