from django.conf import settings
import pusher

def pusher_call(channel=False, event=False, payload=""):
	p = pusher.Pusher(app_id=settings.PUSHER_APP_ID, key=settings.PUSHER_APP_KEY, secret=settings.PUSHER_APP_SECRET)
	p[channel].trigger(event, payload)
