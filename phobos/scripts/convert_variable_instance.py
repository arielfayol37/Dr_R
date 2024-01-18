from phobos.models import VariableInstance, VariableInstance2
from deimos.models import QuestionStudent

def run():
    # QuestionStudent is expected to have both var_instances and var_instances2 attributes.
    # VariableInstance and VariableInstance2 are expected to be defined.

    for qs in QuestionStudent.objects.all():
        for varI in qs.var_instances.all():
            vi2 = VariableInstance2.objects.create(symbol=varI.variable.symbol, question=varI.variable.question, value=varI.value)
            vi2.save()
            qs.var_instances2.add(vi2)

    VariableInstance.objects.all().delete()
    
    # Now delete the var_instances2 attribute and the VariableInstance class
    # ***rename*** VariableInstance2 to VariableInstance.
