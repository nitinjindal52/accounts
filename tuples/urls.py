from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'account.views.home', name='home'),
    # url(r'^account/', include('account.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^account/','tuples.views.account' ),
     url(r'^sub_account/','tuples.views.sub_account' ),
     
     url(r'^edit_account/','tuples.views.edit_account' ),
     url(r'^manage/','tuples.views.manage_account' ),
     url(r'^budget/','tuples.views.budget' ),
     url(r'^budget1/','tuples.views.budget1' ),
     url(r'^budget1_go/(?P<account_number>\d+)/(?P<account_period>\d+)/(?P<p_d_o>\d+)/$','tuples.views.budget1_go' ),
     url(r'^budget1_actual_low_acc/(?P<acc_no>\d+)/(?P<year>\d+)/$','tuples.views.budget1_actual_low_acc'),
     url(r'^budget1_budget_low_acc/(?P<acc_no>\d+)/(?P<year>\d+)/$','tuples.views.budget1_budget_low_acc')

)
