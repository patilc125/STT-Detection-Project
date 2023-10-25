from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import segmentationApp
import os,shutil, glob
import cv2

from .migrationFromFlask.api import Api
from .SegmentationMethods.threshold import threshold
from .SegmentationMethods.regionGrowin import regionGrowing
import mimetypes

from django.contrib import messages

# Create your views here.

class MainView(TemplateView):
    template_name = 'segmentationApp/main.html'



def file_upload_view(request):

    folder = '.\\media\\images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    folder = '.\\media\\predicted'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    if request.method == 'POST':
        my_file = request.FILES.get('file')
        (prefix, suffix) = str(my_file).split('.')
      

        segmentationApp.objects.all().delete()
        segmentationApp.objects.create(upload=my_file, segmentation="predicted/"+prefix+"_predicted."+suffix)
      
        return HttpResponse("")

    return JsonResponse({'post':'false'})

def file_segment_view(request):

        method=request.POST.get('methods')
        if method == 'U-Net':
            api = Api()
            api.call(folder=".\\media\\images",odp=".\\media\\predicted")
            images = segmentationApp.objects.all()
            return render(request, 'segmentationApp/segment.html',{'images' : images,'method':method})
            
        elif method=='Thresholding':
            t = request.POST.get('slider')
            threshold(input_dir=".\\media\\images", output_dir=".\\media\\predicted", threshold=int(t))
            images = segmentationApp.objects.all()
            return render(request, 'segmentationApp/segment.html',{'images' : images,'method':method})

        elif method=="Region Growing":
            images = segmentationApp.objects.all()
            return render(request, 'segmentationApp/region_growing_parameters.html',{'images' : images,'method':method})

        else:
            

            messages.error(request, 'You must choose segmentaton method.')

            return render(request, 'segmentationApp/main.html')


def start_region_growing(request):
    C=request.META.get('QUERY_STRING')
    (cx,cy)=C.split(',')
    # map was clicked at cx,cy coordinates
    x=int(cx)
    y=int(cy)

    img = cv2.imread(glob.glob(".\\media\\images\\*.png")[0])
    if len(img.shape)==3:
        value = img[y,x,0]
    else:
        value = img[y,x]
    #regionGrowing(input_dir=".\\media\\images", output_dir=".\\media\\predicted", seed=(x,y),lower=5,upper=80,multiplier=2.5)
    
    images = segmentationApp.objects.all()
    method="Region Growing"
    
    return render(request, 'segmentationApp/region_growing_parameters.html',{'images' : images,'method':method,'x':x,'y':y, 'value': value})



def start_region_growing_parameters(request):
    lower=request.GET.get('lower')
    upper=request.GET.get('upper')
    multiplier=request.GET.get('multiplier')
    x=request.GET.get('x')
    y=request.GET.get('y')
    if x=='' or y=='':
        messages.error(request, 'Choose start point.')
    else:
        x=int(x)
        y=int(y)
    images = segmentationApp.objects.all()
    method="Region Growing"
    if lower.isnumeric():
       lower=int(lower)
    else:
        messages.error(request, 'Lower value is incorrect.')
        if not upper.isnumeric():
            messages.error(request, 'Upper value is incorrect.')
        if not multiplier.isnumeric():
            messages.error(request, 'Multiplier value is incorrect.')
        
        

        return render(request, 'segmentationApp/region_growing_parameters.html',{'images' : images,'method':method,'x':x,'y':y})
        

    if upper.isnumeric():
       upper=int(upper)
    else:

        
        messages.error(request, 'Upper value is incorrect.')
        
        if not multiplier.isnumeric():
            messages.error(request, 'Multiplier value is incorrect.')
        
        

        return render(request, 'segmentationApp/region_growing_parameters.html',{'images' : images,'method':method,'x':x,'y':y})
       
    if isfloat(multiplier):
       multiplier=float(multiplier)
    else:

        messages.error(request, 'Multiplier value is incorrect.')

        return render(request, 'segmentationApp/region_growing_parameters.html',{'images' : images,'method':method,'x':x,'y':y})
       

    regionGrowing(input_dir=".\\media\\images", output_dir=".\\media\\predicted", seed=(x,y),lower=lower,upper=upper,multiplier=multiplier)
    
    images = segmentationApp.objects.all()
    method="Region Growing"

    return render(request, 'segmentationApp/segment.html',{'images' : images,'method':method})

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def download_file(request):
    # fill these variables with real values
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

    
# def display_images(request):
  
#     if request.method == 'GET':
  
#         # getting all the objects of hotel.
#         return render((request, 'segmentationApp/segment.html',
#                      {'images' : images}))
    


