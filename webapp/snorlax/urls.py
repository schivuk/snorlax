from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'snorlax.views.home', name='home'),
    url(r'^storeData$', 'snorlax.views.storeData', name='storeData'),
    url(r'^trainPosition$', 'snorlax.views.trainPosition', name='trainPosition'),
    url(r'^learnPositions$', 'snorlax.views.learnPositions', name='learnPositions'),
    url(r'^getPosition$', 'snorlax.views.getPosition', name='getPosition'),
   	url(r'^clearAll$', 'snorlax.views.clearAll', name='clearAll'),
   
    #url(r'^getData$', 'snorlax.views.getData', name='getData'),
)
