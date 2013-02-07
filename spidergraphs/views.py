from spidergraphs.models import Institution, Program, Course, ProgramOutcome, CourseToProgram, CourseOutcome
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

def institution(request, institution):
    current_institution = get_object_or_404(Institution, shortname=institution)
    programs = get_list_or_404(Program, institution=current_institution)
    return render_to_response('institution.html', {
        'current_institution' : current_institution,
        'programs' : programs,
    })

def program(request, institution, program_id):
    current_program = get_object_or_404(Program, id=program_id)
    courses = Course.objects.all().select_related().filter(program=current_program)
    for course in courses:
        course.weight = CourseToProgram.objects.get(program_id=program_id, course_id=course.id).weight
        dqp_scores = course.get_dqp_scores()
        course.applied = dqp_scores['applied']
        course.specialized = dqp_scores['specialized']
        course.intellectual = dqp_scores['intellectual']
        course.broad = dqp_scores['broad']
        course.civic = dqp_scores['civic']
    program_outcomes = ProgramOutcome.objects.all().filter(program=current_program)
    return render_to_response('program.html', {
        'current_institution' : current_program.institution,
        'current_program' : current_program,
        'courses' : courses,
        'program_outcomes' : program_outcomes,
    })

def course(request, institution, program_id, course_id):
    current_program = get_object_or_404(Program, id=program_id)
    current_course = get_object_or_404(Course, id=course_id)
    course_outcomes = CourseOutcome.objects.filter(course=current_course)
    return render_to_response('course.html', {
        'current_institution' : current_program.institution,
        'current_program' : current_program,
        'current_course' : current_course,
        'course_outcomes' : course_outcomes
    })

def index(request):
    institutions = Institution.objects.extra(order_by = ['name'])#get_list_or_404(Institution)
    return  render_to_response('index.html', {
        'institutions' : institutions,
    })
