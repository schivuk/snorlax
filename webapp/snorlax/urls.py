from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'snorlax.views.home', name='home'),
    url(r'^storeData$', 'snorlax.views.storeData', name='storeData'),
    url(r'^storeOnOffData$', 'snorlax.views.storeOnOffData', name='storeOnOffData'),
    url(r'^trainPosition$', 'snorlax.views.trainPosition', name='trainPosition'),
    url(r'^learnPositions$', 'snorlax.views.learnPositions', name='learnPositions'),
    url(r'^getPosition$', 'snorlax.views.getPosition', name='getPosition'),
   	url(r'^clearAll$', 'snorlax.views.clearAll', name='clearAll'),
   	url(r'^showRawData$', 'snorlax.views.showRawData', name='showRawData'),
   	url(r'^getLatestReading$', 'snorlax.views.getLatestReading', name='getLatestReading'),
   	url(r'^base$', 'snorlax.views.base', name='base'),
   	url(r'^alarm$', 'snorlax.views.alarm', name='alarm'),
   	url(r'^feedback$', 'snorlax.views.feedback', name='feedback'),
   	url(r'^profile$', 'snorlax.views.profile', name='profile'),
    url(r'^editAlarm$', 'snorlax.views.editAlarm', name='editAlarm'),
    url(r'^analyzeSleepCycle$', 'snorlax.views.analyzeSleepCycle', name='analyzeSleepCycle'),
    url(r'^logSleepForm$', 'snorlax.views.logSleepForm', name='logSleepForm'),
    url(r'^isAlarmReady$', 'snorlax.views.isAlarmReady', name='isAlarmReady'),
    url(r'^trainCurrentPosition/(?P<label>\w+$)', \
                      'snorlax.views.trainCurrentPosition', name='trainCurrentPosition'),
    #url(r'^getData$', 'snorlax.views.getData', name='getData'),
    url(r'^trainOptions$', 'snorlax.views.trainOptions', name='trainOptions'),
    url(r'^numReadingGroups$', 'snorlax.views.getNumReadingGroups', name='numReadingGroups'),
    url(r'^showCurrentPosition$', 'snorlax.views.showCurrentPosition', name='showCurrentPosition'),
    
  
)
