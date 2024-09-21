from django.core.management.base import BaseCommand
from placement.models import Program

class Command(BaseCommand):
    help = 'Add programs to the database in bulk'

    def handle(self, *args, **kwargs):
        # List of programs to add
        programs = [
            # Single Major programs
            {'program_type': 'SINGLE_MAJOR', 'major': 'Actuarial Science'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Applied Geology'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Applied Geophysics'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Biomathematics'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Chemistry'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Computer Science'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Geology'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Geophysics'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Information Technology'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Mathematics'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Physics'},
            {'program_type': 'SINGLE_MAJOR', 'major': 'Statistics'},
            
            # Combined Major programs
            {'program_type': 'COMBINED_MAJOR', 'major': 'Chemistry', 'second_major': 'Biological Science'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Chemistry', 'second_major': 'Physics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Computer Science', 'second_major': 'Mathematics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Computer Science', 'second_major': 'Statistics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Computer Science', 'second_major': 'Physics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Mathematics', 'second_major': 'Statistics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Physics', 'second_major': 'Mathematics'},
            {'program_type': 'COMBINED_MAJOR', 'major': 'Physics', 'second_major': 'Statistics'},
            
            # Major-Minor programs
            {'program_type': 'MAJOR_MINOR', 'major': 'Geology', 'minor': 'Physics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Geology', 'minor': 'Mathematics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Mathematics', 'minor': 'Computer Science'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Mathematics', 'minor': 'Physics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Mathematics', 'minor': 'Statistics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Mathematics', 'minor': 'Geology'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Physics', 'minor': 'Computer Science'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Physics', 'minor': 'Geology'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Physics', 'minor': 'Mathematics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Statistics', 'minor': 'Computer Science'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Statistics', 'minor': 'Mathematics'},
            {'program_type': 'MAJOR_MINOR', 'major': 'Physics', 'minor': 'Statistics'},
        ]

        # Generate the 'program' field based on program_type
        for program in programs:
            if program['program_type'] == 'SINGLE_MAJOR':
                program['program'] = program['major']
            elif program['program_type'] == 'COMBINED_MAJOR':
                program['program'] = f"{program['major']} and {program['second_major']}"
            elif program['program_type'] == 'MAJOR_MINOR':
                program['program'] = f"{program['major']} with {program['minor']}"

        # Bulk create programs
        Program.objects.bulk_create(
            [Program(**program) for program in programs],
            ignore_conflicts=True  # In case some programs already exist
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully added {len(programs)} programs"))