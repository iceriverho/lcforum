from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lcforum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('forum.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

REST_FRAMEWORK = {
    'PAGINATE_BY': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100
}