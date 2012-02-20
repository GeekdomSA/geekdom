from django.core.management.base import NoArgsCommand
from optparse import make_option
from manager.models import *
from settings import *

class Command(NoArgsCommand):

    help = "Foursquare user scraper"

    def handle_noargs(self, **options):


        from urllib import urlopen
        import json
        
        count = 0
        
        url = "https://api.foursquare.com/v2/venues/" + FOURSQUARE_VENUE_ID + "/herenow?oauth_token=" + FOURSQUARE_OAUTH_TOKEN + "&v=20111212"

        f = urlopen(url)
        f = f.read()    
        j = json.loads(f)
        
        for item in j['response']['hereNow']['items']:
            fname = item['user']['firstName']
            lname = item['user']['lastName']
            print "Found: " + fname + " " + lname + "."

            try:
                user = User.objects.get(first_name__icontains = fname, last_name__icontains = lname)
                print "matched with user #" + str(user.id)
                if user.my_profile.check_in():
                    print user.username + " is now checked in."
                    count = count + 1
                else:
                    print user.username + " was already checked in."
            except:
                print "user not found."

        print str(count) + " new users checked in."