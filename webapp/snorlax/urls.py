from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'snorlax.views.home', name='home'),
    url(r'^storeData$', 'snorlax.views.storeData', name='storeData'),
    #url(r'^getData$', 'snorlax.views.getData', name='getData'),
)