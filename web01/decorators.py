from django.shortcuts import *
import functools
def sys_required(fun):
    @functools.wraps(fun)
    def run(req):
        if req.user.has_perm("info.modMachine"):
            return fun(req)
        else:
            return render_to_response("403.html",locals(),RequestContext(req))
    return run
