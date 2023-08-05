from phobos.models import SubTopic
from django.db.models import Count, Subquery, OuterRef
def run():
    # Step 1: Identify duplicate subtopics and their counts
    duplicate_subtopics = SubTopic.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)

    # Step 2: Create a subquery to get the IDs of duplicates to be deleted
    duplicates_to_delete = SubTopic.objects.filter(name=OuterRef('name')).values('id')[1:]

    # Step 3: Delete duplicate subtopics
    SubTopic.objects.filter(id__in=Subquery(duplicates_to_delete)).delete()
