from django.shortcuts import redirect


def require_login(get_response):

    def middleware(request):
        if request.user.is_authenticated or request.path == '/':
            response = get_response(request)
            return response

        return redirect('/')

    return middleware