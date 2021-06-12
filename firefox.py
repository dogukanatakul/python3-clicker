#!/usr/bin/env python
# -*-coding:utf-8-*-
from selenium import webdriver
import time
import settings as setting
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import sys
import json
import os

searchKey = str(input("Aranacak kelime:"))
clickText = str(input("Tıklanacak kelime:"))
limit = int(input("Kaç kez işlem yapılsın:"))
i = 1
while i <= limit:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("geo.prompt.testing", True)
    profile.set_preference("geo.prompt.testing.allow", True)
    profile.set_preference("geo.wifi.scan", True)
    profile.set_preference("geo.provider.network.url",
                           'data:application/json,{"location":{"lat":' + setting.getLocation()[0] + ',"lng":' +
                           setting.getLocation()[1] + '},"accuracy": 100.0}')
    if setting.getSetting('user-agent') == "on":
        profile.set_preference("general.useragent.override", str(setting.getDevice()))
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile)
    time.sleep(2)
    driver.maximize_window()
    # VPN START
    if setting.getSetting('vpn') == "on":
        # EKLENTİ KURMA
        driver.install_addon(os.path.abspath("vpn.xpi"), temporary=True)
        # EKLENTİ KURMA
        time.sleep(15)
        driver.switch_to.window(driver.window_handles[0])  # İlk sekmeye geri dön (eklentinin reklamından kurtulma)
        time.sleep(setting.getSetting('workSleep'))
        driver.get("about:config")
        time.sleep(setting.getSetting('workSleep'))
        driver.find_element_by_xpath('//*[@id="warningButton"]').click()
        time.sleep(setting.getSetting('workSleep'))
        driver.find_element_by_xpath('//*[@id=\"about-config-search\"]').send_keys("extensions.webextensions.uuids")
        time.sleep(setting.getSetting('workSleep'))
        plugin = json.loads(driver.find_element_by_xpath('/html/body/table/tr/td[1]/span/span').get_attribute('innerHTML'))
        driver.get("moz-extension://" + plugin["touch-vpn@anchorfree.com"] + "/panel/index.html")
        time.sleep(setting.getSetting('workSleep'))
        driver.find_element_by_xpath('//*[@class="button button--red data-consent__accept-button"]').click()
        time.sleep(setting.getSetting('workSleep'))
        driver.find_element_by_xpath('//*[@id="ConnectionButton"]').click()
        time.sleep(setting.getSetting('loadingSleep'))
        driver.get("https://www.google.com.tr/search?q=" + searchKey)
        time.sleep(setting.getSetting('loadingSleep'))

        # Anlaşma Mesajı
        try:
            driver.find_element_by_xpath('//*[@id="' + setting.getSetting('contractID') + '"]').click()
            time.sleep(2)
        except NoSuchElementException:
            print("")
        # Anlaşma Mesajı SON

        driver.execute_script("window.scrollTo(0, window.scrollY + 5000)")
        time.sleep(2)
        # LOKASYON TIKLAMA
        try:
            driver.find_element_by_xpath('//*[@id="' + setting.getSetting('locationID') + '"]').click()
        except NoSuchElementException:
            print("Bir hata oluştu.")
            time.sleep(10)
            driver.close()
            sys.exit()
        # LOKASYON TIKLAMA SON
        time.sleep(setting.getSetting('loadingSleep'))
    driver.get("https://www.google.com.tr/search?q=" + searchKey)
    time.sleep(setting.getSetting('loadingSleep'))

    # HEDEF TIKLAMA
    try:
        driver.find_element_by_partial_link_text(clickText).click()
    except NoSuchElementException:
        print("Bir hata oluştu.")
        time.sleep(10)
        driver.close()
        sys.exit()
    # HEDEF TIKLAMA
    time.sleep(setting.getSetting('loadingSleep'))
    # SİTE İÇİ GEZİNME
    if setting.getSetting("scroll-bot") == "on":
        driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
        time.sleep((setting.getSetting('adSiteSleep') / 3))
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep((setting.getSetting('adSiteSleep') / 3))
        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
        time.sleep((setting.getSetting('adSiteSleep') / 3))
        driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
        driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    # SİTE İÇİ GEZİNME
    i += 1
    driver.close()
sys.exit()
