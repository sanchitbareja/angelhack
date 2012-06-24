from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from angelhack.settings import AWS_UPLOAD_DESTINATION

class Text2ImpressForm(forms.Form):
    file  = forms.FileField(required=False)
    input = forms.CharField(widget=forms.Textarea, required=False)

# General pages
def index_home(request):
    if request.method=="POST":
        print "index_home POST"
        print request.POST
    form = Text2ImpressForm()
    return render_to_response('index_home.html', {'form':form}, context_instance=RequestContext(request))

def generate_impressjs(request):
    return render_to_response('default_impressjs.html', context_instance=RequestContext(request))

def impressify_txt(request):
    print "inside impressify_txt"
    print request.POST
    return render_to_response('index_home.html', context_instance=RequestContext(request))

def handle_uploaded_file(f):
    """
    unzip the file, upload each of the files individually to s3, get the s3 urls
    """
    fileame = str(f['file'])
    if fileame.endswith('.txt'):
        file_contents = f['file'].read()
        default_storage.save(fileame, ContentFile(file_contents))
        return file_contents # success
    else:
        # throw an error syaing that it is not a text file
        return False # failure

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def upload_file(request):
    print "I am inside upload_file"
    if request.method == 'POST':
        print "inside upload_file POST request handling: "+str(request.POST)
        print "file: "+str(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            success = handle_uploaded_file(request.FILES)
            if success:
                file_contents = success
                success = True
            response = {
                'success': success,
                'content': render_to_string( 'upload_response.html', RequestContext(request) ),
                'file_contents': file_contents,
            }
            # return JsonResponse( statusCode = 200, body = response ).response
            return HttpResponse(json.dumps(response),mimetype='application/json')
            # return render_to_response('upload_response.html',{'success':success,'urls':list_of_file_urls}, context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('test_upload.html', {'submit_success': False, 'form': form}, context_instance = RequestContext(request))