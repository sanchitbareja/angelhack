from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
import json, os, hashlib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from angelhack.settings import AWS_UPLOAD_DESTINATION
from parse import parse
from parseHtml import parseHtml
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from toast.models import Toast

# Login/Logout and signup pages

def login(request):
    t = get_template('login.html')
    html = t.render(RequestContext(request))
    return HttpResponse(html)

def login_authenticate(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/")
    else:
        # Show an error page
        return HttpResponseRedirect("/accounts/invalid/")

def logout(request):
    auth.logout(request)
    # Redirect to a success page. - to redo and redirect to /account/loggedout/ instead
    return HttpResponseRedirect("/accounts/loggedout/")

def loggedout(request):
    t = get_template('loggedout.html')
    html = t.render(RequestContext(request))
    return HttpResponse(html)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/login/")
    else:
        form = UserCreationForm()
        print form
    return render_to_response("signup.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def invalid(request):
    return HttpResponseRedirect("/accounts/login/")


# General pages
def index_home(request):
    iframe_url = "http://text2impress.s3.amazonaws.com/28712277BOTCDRhKaUPGXJK.html"
    if request.method=="POST":
        parsed_html = parseHtml(parse(request.POST['impressify_text_final']))
        total_html = ""
        for elem in parsed_html:
            total_html += elem
        rendered_html_page = render_to_response('default_impressjs.html',{"generated_html":total_html}, RequestContext(request))
        # print "Rendered page starts here -----------------"
        # print rendered_html_page.content
        # print "Rendered page ends here -----------------"
        import random, string
        digits = "".join( [random.choice(string.digits) for i in xrange(8)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(15)] )
        random_string = digits+chars+".html"
        link_to_page = default_storage.save(random_string, ContentFile(rendered_html_page.content))
        iframe_url = "http://text2impress.s3.amazonaws.com/"+random_string
        if request.user.is_authenticated():
            new_toast = Toast(user=request.user,url=iframe_url)
            new_toast.save()
    return render_to_response('index_home.html',{"iframe_url":iframe_url}, context_instance=RequestContext(request))

def generate_impressjs(request):
    return render_to_response('default_impressjs.html', context_instance=RequestContext(request))

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

def past_toasts(request):
    user=request.user
    history_of_toasts = Toast.objects.filter(user=user)
    return render_to_response('past_toasts.html',{'history_of_toasts':history_of_toasts}, context_instance=RequestContext(request))
