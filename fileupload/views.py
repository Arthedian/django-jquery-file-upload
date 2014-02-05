# encoding: utf-8
from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from fileupload.models import *
from django.shortcuts import render
import urllib


class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        for i in range(len(files)):
            name=urllib.parse.unquote(files[i]["thumbnailUrl"][7:])
            hi=Picture.objects.get(file=name)
            files[i]["thumbnail"]=hi.thumbnail.url
            #files[i]["thumbnail"]=files[i]["thumbnailUrl"][7:]
        data = {'files': files}
		#f = self.request.FILES.get('file')
        #data = [{'name': f.name, 'url': self.object.file.url, 'thumbnail_url': self.object.thumbnail.url, 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class BasicVersionCreateView(PictureCreateView):
    template_name_suffix = '_basic_form'


class BasicPlusVersionCreateView(PictureCreateView):
    template_name_suffix = '_basicplus_form'


class AngularVersionCreateView(PictureCreateView):
    template_name_suffix = '_angular_form'


class jQueryVersionCreateView(PictureCreateView):
    template_name_suffix = '_jquery_form'


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        for i in range(len(files)):
            name=urllib.parse.unquote(files[i]["thumbnailUrl"][7:])
            hi=Picture.objects.get(file=name)
            files[i]["thumbnail"]=hi.thumbnail.url
            #files[i]["thumbnail"]=files[i]["thumbnailUrl"][7:]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

def test(request):
	novinky=Picture.objects.all() #vezme vsechny novinky a nejnovejsi vlozi na zacatek
	return render(request, 'test.html', {'test': novinky,})