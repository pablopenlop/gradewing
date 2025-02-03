from .models import YearGroup
from choices import YearGroupLevel



def load_yeargroups(school=None):
    return None
    for system, yeargroups in YEARGROUP_SYSTEMS.items():
        for yeargroup in yeargroups:
            YearGroup.objects.update_or_create(
                system= system,
                level = yeargroup['level'],
                defaults={
                    'name': yeargroup['name'],
                }
            )
    print("Preset YearGroups loaded successfully.")


# Usage example:
# Specify a school instance or leave it as None if not associating with a specific school.
# school_instance = School.objects.get(name="Example School")
# load_yeargroup_presets(school=school_instance)
