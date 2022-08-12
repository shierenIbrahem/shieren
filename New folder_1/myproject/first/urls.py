from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('bookPassport',views.bookPassport ,name='bookPassport'),
	path('second_page',views.second_page ,name='second_page'),
	path('third_page',views.third_page ,name='third_page'),
	path('four_page',views.four_page ,name='four_page'),
	path('services',views.services ,name='services'),
	#path('profile',views.profile ,name='profile'),
	path('forgettenPassword',views.forgetten_password ,name='forgettenPassword'),
	path('pass_port_count',views.pass_port_count ,name='pass_port_count'),
	path('moving_count',views.moving_count ,name='moving_count'),
	path('staying_count',views.staying_count ,name='staying_count'),
	path('pass_port_cancel',views.pass_port_cancel ,name='pass_port_cancel'),
	path('moving_cancel',views.moving_cancel ,name='moving_cancel'),
	path('notification',views.notification ,name='notification'),
	path('staying_cancel',views.staying_cancel ,name='staying_cancel'),
]

