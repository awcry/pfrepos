
import config # main config
import urllib
import socket
import time

from selenium import webdriver

try:
    while True:
        code = urllib.request.urlopen(config.updatescript_url).getcode()
        print("{0} - {1}".format(config.updatescript_url, code))
        codePPK = urllib.request.urlopen(config.updatescriptPPK_url).getcode()
        print("{0} - {1}".format(config.updatescriptPPK_url, codePPK))
        if (code not in [200, 301]) or (codePPK not in [200, 301]):
            print('ERROR: {0} - {1}')
        else:
            print('UpdateScript: is in progress..')
            print('UpdateScriptPPK: is in progress..')
            driver = webdriver.PhantomJS()
            driver.set_window_size(800, 600)
            driver.get(config.updatescript_url) # url changes
            driver.save_screenshot(config.chng_file)
            driverPPK = webdriver.PhantomJS()
            driverPPK.set_window_size(800, 600)
            driverPPK.get(config.updatescriptPPK_url) # url changes
            driverPPK.save_screenshot(config.chngPPK_file)
            print('UpdateScript: success!')
            print('UpdateScriptPPK: success!')
            time.sleep(config.updatescript_updatetime)
except socket.error as e:
	print('Ping Error: ', e)
