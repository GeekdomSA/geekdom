from django.template import Context
from manager.models import BackgroundImage

def flickr_background(request):
  try:
    background_image = BackgroundImage.objects.order_by('?')[0].url
  except:
    background_image = []
  
  return {'background_image' : background_image }

