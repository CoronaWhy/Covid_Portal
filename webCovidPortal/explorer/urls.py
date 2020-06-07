from django.urls import path;
from explorer import views;

urlpatterns = [
    path('', views.index, name="index"),
    path('taxa', views.taxa, name="taxa"),
    path('sequencerecords', views.sequencerecords, name="sequencerecords"),
    path('sequences', views.sequences, name='sequences'),
    path('nomenclature', views.nomenclature, name='nomenclature'),
    path('epitopeexperimentclasses', views.epitopeexperimentclasses, name='epitopeexperimentclasses'),
    path('epitopeexperimentsfilter', views.epitopeexperimentsfilter, name='epitopeexperimentsfilter'),
    path('epitopesequence', views.epitopesequence, name='epitopesequence'),
    path('structurechains', views.structurechains, name='structurechains'),
    path('structuresequence', views.structuresequence, name='structuresequence'),
    path('structureresidueatoms', views.structureresidueatoms, name='structureresidueatoms'),
];
