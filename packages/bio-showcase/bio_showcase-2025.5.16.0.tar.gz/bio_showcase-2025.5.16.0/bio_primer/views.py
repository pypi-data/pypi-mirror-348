import json
import django.views.generic
import django.utils.timezone
from .models import PCRResult, ResultObject
from .primer import get_primer_result
# Create your views here.


class IndexView(django.views.generic.ListView):
    template_name = 'primer/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return []


def design(request):
    try:
        seq_start = request.GET['seq_start']
        seq_end = request.GET['seq_end']
        sequence = request.GET['sequence']
    except KeyError:
        # Redisplay the question voting form.
        return django.shortcuts.render(
            request=request,
            template_name='primer/index.html',
            context={
                'error_message': 'parameter error',
            },
        )
    else:
        sequence = sequence.replace("'", '').replace(' ', '')

        primer_result = get_primer_result(sequence, int(seq_start), int(seq_end))

        result = PCRResult(
            seq_start=seq_start,
            result=primer_result,
            seq_end=seq_end,
            sequence=sequence,
        )
        return django.shortcuts.render(
            request=request,
            template_name='primer/index.html',
            context={'result': result, 'r': ResultObject(primer_result)},
        )
