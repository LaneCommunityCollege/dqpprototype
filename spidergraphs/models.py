from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,MaxLengthValidator,RegexValidator,ValidationError
from django.db.models import Sum,Avg
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def dqpscore(score):
    return str(round(score*100,1))

class CommonOutcome(models.Model):
    class Meta:
        abstract = True

    applied = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        blank=True, null=True,
        help_text="Enter a decimal such as 0.15"
    )
    specialized = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        blank=True, null=True,
        help_text="Enter a decimal such as 0.15"
    )
    intellectual = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        blank=True, null=True,
        help_text="Enter a decimal such as 0.15"
    )
    broad = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        blank=True, null=True,
        help_text="Enter a decimal such as 0.15"
    )
    civic = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        blank=True, null=True,
        help_text="Enter a decimal such as 0.15"
    )
    weight = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        default=1.0,
        help_text="Enter a decimal such as 0.15"
    )
    outcome = models.TextField()
    comments = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.outcome

    def get_dqp_scores_graphs(self):
        return json.dumps({
            'scores': [
                dqpscore(self.applied),
                dqpscore(self.specialized),
                dqpscore(self.intellectual),
                dqpscore(self.broad),
                dqpscore(self.civic)
            ],
            'fields': [
                'applied', 'specialized', 'intellectual', 'broad', 'civic'
            ]
        })

    def sparkdata(self):
        return ','.join(map(dqpscore,(self.applied, self.specialized, self.intellectual, self.broad, self.civic)))

    def clean(self):
        if None in (self.applied, self.specialized, self.intellectual, self.broad, self.civic) and any((self.applied, self.specialized, self.intellectual, self.broad, self.civic)):
            raise ValidationError("DQP Scores must either be completely filled out or completely empty")
        if all((self.applied, self.specialized, self.intellectual, self.broad, self.civic)):
            sumdqp = sum((self.applied, self.specialized, self.intellectual, self.broad, self.civic))
            if sumdqp != 1:
                raise ValidationError("The sum of your DQP Scores MUST be 1.0, currently it is %s" % sumdqp)


class Institution(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    shortname = models.CharField(
        max_length=10,
        unique=True,
        validators=[MaxLengthValidator(10),RegexValidator(regex=r'[a-z_]+',message="You can only use lowercase letters and underscoes")],
        help_text="This will be used to view your institution's graphs, for example http://dqp.lanecc.edu/lcc/ would be the DQP landing page for LCC"
    )

    def __unicode__(self):
        return self.name

class Program(models.Model):
    #TODO validate that a program/institution combination are unique
    institution = models.ForeignKey(Institution)
    name = models.CharField(max_length=255)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('institution', 'name')

    def get_dqp_scores_graphs(self):
        outcomes = ProgramOutcome.objects.filter(program=self)
        if not outcomes:
            return False
        sums = {'applied':0, 'specialized':0, 'intellectual':0, 'broad':0, 'civic':0}
        for outcome in outcomes:
            sums['applied'] += outcome.applied * outcome.weight
            sums['specialized'] += outcome.specialized * outcome.weight
            sums['intellectual'] += outcome.intellectual * outcome.weight
            sums['broad'] += outcome.broad * outcome.weight
            sums['civic'] += outcome.civic * outcome.weight
        for k,v in sums.iteritems():
            sums[k] = dqpscore(v)

        return json.dumps({
            'scores':[
                sums['applied'], sums['specialized'], sums['intellectual'], sums['broad'], sums['civic']
            ],
            'fields':[
                'Applied', 'Specialized', 'Intellectual', 'Broad', 'Civic'
            ]
        })

    def get_course_dqp_scores(self):
        courses = Course.objects.all().select_related().filter(program=self)
        if not courses:
            return False
        sums = {'applied':0, 'specialized':0, 'intellectual':0, 'broad':0, 'civic':0}
        for course in courses:
            course.weight = float(CourseToProgram.objects.get(program_id=self.id, course_id=course.id).weight)
            dqp_scores = course.get_dqp_scores()
            sums['applied']+= course.weight*dqp_scores['applied']
            sums['specialized']+= course.weight*dqp_scores['specialized']
            sums['intellectual']+= course.weight*dqp_scores['intellectual']
            sums['broad']+= course.weight*dqp_scores['broad']
            sums['civic']+= course.weight*dqp_scores['civic']
        return sums

    def get_course_dqp_scores_graphs(self):
        sums = self.get_course_dqp_scores()
        if not sums:
            return False
        for k, v in sums.iteritems():
            sums[k] = dqpscore(v)
        return json.dumps({
            'scores':[
                sums['applied'], sums['specialized'], sums['intellectual'], sums['broad'], sums['civic']
            ],
            'fields':[
                'Applied', 'Specialized', 'Intellectual', 'Broad', 'Civic'
            ]
        })

    def sparkdata(self):
        data = self.get_course_dqp_scores()
        if not data:
            return ""
        return ','.join(map(dqpscore,(data['applied'], data['specialized'], data['intellectual'], data['broad'], data['civic'])))

    def __unicode__(self):
        return self.name

class ProgramOutcome(CommonOutcome):
    program = models.ForeignKey(Program)
    class Meta:
        unique_together = ('program', 'outcome')

class Course(models.Model):
    program = models.ManyToManyField(Program, through='CourseToProgram')
    course_number = models.CharField(max_length=255,help_text="For example: psych 101")
    comments = models.TextField(blank=True, null=True)
    institution = models.ForeignKey(Institution)
    class Meta:
        unique_together = ('institution', 'course_number')

    def get_dqp_scores(self):
        outcomes = CourseOutcome.objects.filter(course=self)
        if not outcomes:
            return False
        sums = {'applied':0, 'specialized':0, 'intellectual':0, 'broad':0, 'civic':0}
        for outcome in outcomes:
            sums['applied'] += outcome.applied * outcome.weight
            sums['specialized'] += outcome.specialized * outcome.weight
            sums['intellectual'] += outcome.intellectual * outcome.weight
            sums['broad'] += outcome.broad * outcome.weight
            sums['civic'] += outcome.civic * outcome.weight
        for k,v in sums.iteritems():
            sums[k] = round(v,3)
        return sums

    def get_dqp_scores_graphs(self):
        sums = self.get_dqp_scores()
        if not sums:
            return False
        for k,v in sums.iteritems():
            sums[k] = dqpscore(v)
        return json.dumps({
            'scores':[
                sums['applied'], sums['specialized'], sums['intellectual'], sums['broad'], sums['civic']
            ],
            'fields':[
                'Applied', 'Specialized', 'Intellectual', 'Broad', 'Civic'
            ]
        })

    def sparkdata(self):
        data = self.get_dqp_scores()
        if not data:
            return ""
        return ','.join(map(dqpscore,(data['applied'], data['specialized'], data['intellectual'], data['broad'], data['civic'])))

    def __unicode__(self):
        return self.course_number

class CourseToProgram(models.Model):
    course = models.ForeignKey(Course)
    program = models.ForeignKey(Program)
    weight = models.DecimalField(
        max_digits=4, decimal_places=3,
        validators=[MaxValueValidator(1),MinValueValidator(0)],
        default=1.0
    )

    class Meta:
        unique_together = ('course', 'program')

    def __unicode__(self):
        return Program.objects.get(id=self.program_id).__unicode__() + "-" + Course.objects.get(id=self.course_id).__unicode__()

    def clean(self):
        try:
            self.course.get_dqp_scores_graphs()
        except:
            raise ValidationError("You cannot add a course to a program until that course has had DQP scores set (Edit this course first)")


class CourseOutcome(CommonOutcome):
    course = models.ForeignKey(Course)
    class Meta:
        unique_together = ('course', 'outcome')

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    institution = models.ForeignKey(Institution,blank=True, null=True)
