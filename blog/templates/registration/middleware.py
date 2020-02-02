from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class ValidLogin(object):

    def process_request(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        return None
