from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django import forms
from django.http import HttpResponseRedirect

class Text2ImpressForm(forms.Form):
    file  = forms.FileField()
    subject = forms.CharField(widget=forms.Textarea)

# General pages
def index_home(request):
    form = Text2ImpressForm()
    return render_to_response('index_home.html', {'form':form}, context_instance=RequestContext(request))

def generate_impressjs(request):
    return render_to_response('default_impressjs.html', context_instance=RequestContext(request))

def handle_uploaded_file(f):
    """
    unzip the file, upload each of the files individually to s3, get the s3 urls
    """
    list_of_file_urls = []
    try:
        if zipfile.is_zipfile(f):
            zippedfile = zipfile.ZipFile(f)
            if not zippedfile.testzip(): # checks each of the archived file's CRC and file headers. returns the first bad file if any
                extracted_files = zippedfile.namelist()
                for extracted_file_name in extracted_files:
                    fileinfo = zippedfile.getinfo(extracted_file_name)
                    print "FileInfo: "+str(fileinfo.filename)
                    filename = fileinfo.filename
                    isDir = filename[-1] == '/' # this is a hack, we need a more concrete method of determining files
                    isHidden = filename[0] == '.' or filename[0] == '_'
                    print "isDir?: "+str(isDir)
                    print "isHidden?: "+str(isHidden)
                    if not isDir and not isHidden:
                        extracted_file = zippedfile.extract(extracted_file_name)
                        # save each of the extracted files
                        print extracted_file_name
                        list_of_file_urls += [AWS_UPLOAD_DESTINATION+str(extracted_file_name)]
                        default_storage.save(str(extracted_file_name),File(open(extracted_file,'rwb')))
        return list_of_file_urls
    except Exception as e:
        print e
        return None

def upload_file(request):
    print "I am inside upload_file"
    if request.method == 'POST':
        print "inside upload_file POST request handling: "+str(request.POST)
        print "file: "+str(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            list_of_file_urls = handle_uploaded_file(request.FILES['file'])
            print list_of_file_urls
            response = {
                'success': True,
                'content': render_to_string( 'upload_response.html', RequestContext(request) ),
                'urls': list_of_file_urls,
            }
            # return JsonResponse( statusCode = 200, body = response ).response
            return HttpResponse(json.dumps(response),mimetype='application/json')
            # return render_to_response('upload_response.html',{'success':success,'urls':list_of_file_urls}, context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('test_upload.html', {'submit_success': False, 'form': form}, context_instance = RequestContext(request))