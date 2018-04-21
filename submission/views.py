from django.shortcuts import render
from django.http import HttpResponse,Http404
from annoying.functions import get_object_or_None
from user.models import login_required_ajax
from json import dumps
from django.conf import settings
from .models import Submission
# Create your views here.

@login_required_ajax
def submit_solution(request):
    status = {
        'submission_id' : -1
    }
    try:
        if request.method == 'POST':
            problemid = request.POST.get( 'problemid' )
            code = request.POST.get( 'code' )
            lang = request.POST.get( 'language' )
            if problemid == None or code == None or lang == None:
                raise ValueError( "Some solution info missed." )
            if len( code ) > settings.MAX_SOURCECORE_LENGTH:
                raise ValueError( "Length of source code is too long." )
            if lang not in settings.SUPPORT_LANGUAGE_LIST:
                raise ValueError( "Unknown language."  )
            s = Submission(
                language = lang,
                problem_id = problemid,
                judge_status = 'Waiting',
                code = code
            )
            s.save()
            status[ 'submission_id' ] = s.submission_id
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )



def fetch_waiting_submission(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']
    if ip not in settings.JUDGE_VALID_IPPOOL:
        raise Http404( 'Permission Denied' )
#    return HttpResponse( dumps( wait_submission ) content_type = 'application/json' )