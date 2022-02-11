from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


"""These are defined for the project status in a list"""

status = (
    ('1','Stuck'),
    ('2','Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)

class Project(models.Model):
    """Creating Database table for Project"""


    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    assign = models.ManyToManyField(User)
    efforts = models.DurationField()
    status = models.CharField(max_length=7, choices=status, default=1)
    dead_line = models.DateField()
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE)
    complete_per = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)

    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Returing name of the project to display"""

        return (self.name)


class Task(models.Model):
    """This class is created for the task table in database"""


    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)
    status = models.CharField(max_length=7, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        """Returning the task name to display"""

        return(self.task_name)
