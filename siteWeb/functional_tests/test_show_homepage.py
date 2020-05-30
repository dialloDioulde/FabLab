from selenium import webdriver
from siteWeb.models import Loaner, Type, Material, LoanMaterial, Loan, UserProfile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse, resolve
import time


#class TestFunctionals(StaticLiveServerTestCase):

    #def setUp(self):
        #self.browser = webdriver.chrome('functional_tests/chromedriver.exe')


    #def tearDown(self):
       # self.browser.close()

    #def test_no_get_home_page(self):
       # self.browser.get(self.live_server_url)
        #time.sleep(20)
