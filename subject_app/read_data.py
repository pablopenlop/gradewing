from .models import Qualification, Component, SubjectArea, SubjectField
from django.db import transaction


def update_subject_areas():
    with transaction.atomic():
        for subject_code, _ in SubjectField.choices:
            SubjectArea.objects.update_or_create(
                name=subject_code,
                defaults={'name': subject_code}  # You can update additional fields here if necessary
            )


def update_subject_data_old(subjects):
    with transaction.atomic():
        for subject in subjects:
            # Update or create AS Level subject
            as_subject, _ = Qualification.objects.update_or_create(
                code=subject['code'][0],
                qualification = subject['qualification'][0],
                board = subject['board'],
                first_assessment = subject['first_assessment'][0],
                defaults={
                    'name': subject['name'],
                    'board': subject['board'],
                    'maxmark': subject['max_umsmark'][0]
                }
            )
            
            # Update or create A2 Level subject
            a2_subject, _ = Qualification.objects.update_or_create(
                code=subject['code'][1],
                qualification = subject['qualification'][1],
                board = subject['board'],
                first_assessment = subject['first_assessment'][1],
                defaults={
                    'name': subject['name'],
                    'maxmark': subject['max_umsmark'][1]
                }
            )
            
            # Save or update papers and link to subjects
            for paper_data in subject['papers']:
                paper, created = Component.objects.update_or_create(
                    name=paper_data['name'],
                    code=paper_data['code'],
                    defaults={
                        'maxmark': paper_data['max_umsmark']
                    }
                )
                
                # Link paper to AS subject if eligible
                if paper_data['eligible'][0]:
                    paper.subjects.add(as_subject)
                
                # Link paper to A2 subject if eligible
                if paper_data['eligible'][1]:
                    paper.subjects.add(a2_subject)

                # Save paper to ensure max_umsmark is updated
                if not created:
                    paper.mammark = paper_data['max_umsmark']
                    paper.save()


def update_subject_data(subjects):
    with transaction.atomic():
        for subject in subjects:
            variants = []
            numvar = len(subject['code'])
            for i in range(numvar):
                variant, _ = Qualification.objects.update_or_create(
                    code=subject['code'][i],
                    qualification = subject['qualification'][i],
                    board = subject['board'],
                    first_assessment = subject['first_assessment'][i],
                    defaults={
                        'name': subject['name'],
                        'board': subject['board'],
                        'maxmark': subject['max_umsmark'][i]
                    }
                )
                variants.append(variant)
            
            # Save or update papers and link to subjects
            for paper_data in subject['papers']:
                paper, created = Component.objects.update_or_create(
                    name=paper_data['name'],
                    code=paper_data['code'],
                    defaults={
                        'maxmark': paper_data['max_umsmark']
                    }
                )
                # Link paper to subject if eligible
                for i, variant in enumerate(variants):
                    if paper_data['eligible'][i]:
                        paper.subjects.add(variant)
                    
                # Save paper to ensure max_umsmark is updated
                if not created:
                    paper.mammark = paper_data['max_umsmark']
                    paper.save()
