from manager.models import Checkin
import datetime

class CheckinChecker:

	def process_response(self, request, response):

		if response.content != "":
		# after login you get redirected to your profile page, so if you set the cookie on any request, 
		# you won't see it (since it's getting set at the redirect)
		# therefore, only set the cookie if there is content in the response

			try: 
				test = request.COOKIES['asked_for_checkin']
			except:

				try:
					if request.user.is_authenticated():
						now = datetime.datetime.now()

						checkin = Checkin.objects.filter(userprofile = request.user.my_profile).filter(expires_at__gte = now)
						if not checkin.count() > 0:
							response.set_cookie("asked_for_checkin", value = True, expires=7200) # 2 hours
				except:
					pass
		
		return response

