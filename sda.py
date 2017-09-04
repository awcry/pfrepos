import ftplib
import cloudinary.uploader

from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(800, 600)
driver.get('http://pgups-karelia.ru/edu-process/change-ochno-spo/')
driver.save_screenshot('tols.png')
cloudinary.uploader.upload('tols.png')
