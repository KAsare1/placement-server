from django.db import models

class Program(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('SINGLE_MAJOR', 'Single Major'),
        ('COMBINED_MAJOR', 'Combined Major'),
        ('MAJOR_MINOR', 'Major Minor'),
    ]
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES)
    major = models.CharField(max_length=250)
    second_major = models.CharField(max_length=250, blank=True, null=True)  # For combined major
    minor = models.CharField(max_length=250, blank=True, null=True)  # For major-minor
    program = models.CharField(max_length=500, blank=True)  # This field will be generated

    def save(self, *args, **kwargs):
            # Define a dictionary to map program types to formatting functions
        format_program = {
            'SINGLE_MAJOR': lambda: self.major,
            'COMBINED_MAJOR': lambda: f"{self.major} and {self.second_major}" if self.second_major else self._raise_missing_field('second_major'),
            'MAJOR_MINOR': lambda: f"{self.major} with {self.minor}" if self.minor else self._raise_missing_field('minor'),
        }


        if self.program_type in format_program:
            self.program = format_program[self.program_type]()
        else:
            raise ValueError("Invalid program type.")
        super().save(*args, **kwargs)

    def _raise_missing_field(self, field_name):
        raise ValueError(f"A {field_name.replace('_', ' ')} must be provided for the selected program type.")

    def __str__(self):
        return self.program


class Choice(models.Model):
    student = models.OneToOneField("UserAuth.User", verbose_name=("Students"), on_delete=models.CASCADE)
    first_choice = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='first_choice_students', null=True, blank=True)
    second_choice = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='second_choice_students', null=True, blank=True)
    third_choice = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='third_choice_students', null=True, blank=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} Choices"


class Results(models.Model):
    student = models.CharField(max_length=250)
    students_id = models.CharField(max_length=250, unique=True)
    
    results = models.CharField(max_length=100)  #Will Adjust as needed to different courses along with the corresponding grade
    CGPA = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.students_id}"


class ConsiderationRequest(models.Model):
    student = models.OneToOneField("UserAuth.User", verbose_name=("Students"), on_delete=models.CASCADE)
    Results = models.CharField(max_length=250)
    CGPA = models.CharField(max_length=250)
    choice = models.CharField(max_length=250)
    explanation = models.CharField(max_length=1000)


class Placement(models.Model):
    student = models.OneToOneField("UserAuth.User", verbose_name=("Students"), on_delete=models.CASCADE)
    placement = models.OneToOneField("placement.Program", verbose_name=("Student's placements"), on_delete=models.CASCADE)