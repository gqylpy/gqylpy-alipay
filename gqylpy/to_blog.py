from sanic import response
from sanic import Blueprint
from config import BLOG_DOMAIN_NAME

to_blog = Blueprint('redirect_blog', url_prefix='106')


@to_blog.get('/<blog_path:string>')
async def fn_106(request, blog_path):
    # User home
    return response.redirect(
        f'http://{BLOG_DOMAIN_NAME}/{blog_path}/'
    )


@to_blog.get('/<blog_path:string>/<aid:int>')
async def fn_1060(request, blog_path, aid):
    # Article page
    return response.redirect(
        f'http://{BLOG_DOMAIN_NAME}/{blog_path}/{aid}/'
    )
