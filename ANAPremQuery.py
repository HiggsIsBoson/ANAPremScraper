import chromedriver_binary
import os,datetime,calendar
from optparse import OptionParser
from selenium.webdriver.chrome.options import Options

# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Append a 0 for single digit day/month
def zstr(day_or_month):
    return str(day_or_month) if day_or_month>=10 else '0'+str(day_or_month) 

#########################
class ANAPremQuery():

  def setup_method(self, doHeadless=False):
    chrome_options = Options()
    # doHeadless=True ->Operate in the "batch mode" (no browswer window will show up)
    if doHeadless: 
        print("The headless mode is currently not working (the search result won't be displayed). Will run with the normal foreground mode.")
        #chrome_options.add_argument('--headless');
    
    self.driver = webdriver.Chrome(options=chrome_options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()

  ##########
  def doQuery(self, origin, dest, year, month, day=-1):

    #
    # day>0  -> Just query the day
    # day<=0 -> Dump all days of the month
    #

    dumpWholeMonth = bool(day<=0)
    
    # A bunch of sanity checks
    if year > 2030 :
        print('Outragously distant year %i specified. Are you sure? (will return gracefully for now...)' % year)
        os.sys.exit(1)

    today = datetime.date.today()
    if year < today.year or (year==today.year and month < today.month):
        print('Past month specified: %i-%i. This can only handle the future. Exit.' % (year,month))
        os.sys.exit(1)

    weekNum_1stDay, nDaysOfTheMonth = calendar.monthrange(year, month)
    if day > nDaysOfTheMonth :
        print('Spurious day %i specified. You are not supposed to do this! Exit.' % day)
        os.sys.exit(1)

    # Figure the first day to fetch (one can only search for the future)
    day_1stQuery=None
    if dumpWholeMonth : 
        print('Try to query for the month: %i-%i' % (year,month))
        day_1stQuery = max(today+datetime.timedelta(days=1),datetime.date(year,month,1))
        print("Note only start the query from the nearest future date (if applicable): ", day_1stQuery)

    else:
        day_1stQuery = datetime.date(year, month, day) 
        print("Try a query on: ", day_1stQuery)
        if day_1stQuery < today:
            print("Can't query the past. Exit.")
            os.sys.exit(1)

    
    # Start the browsing
    self.driver.get("https://www.ana.co.jp/ja/jp/book-plan/fare/domestic/premiumclass/")
#    self.driver.set_window_size(1792, 1017)
    self.driver.execute_script("window.scrollTo(0,109)")

    # Switch Return -> Oneway
    self.driver.find_element(By.ID, "secondmodule_ticket02").click()

    # Delete the preset origin in the form
    self.driver.find_element(By.CSS_SELECTOR, "#module001 .m_departureAirport .d_clearButton > img").click() 

    # Origin
    self.driver.find_element(By.ID, "m_secondmodule_depApoText_01").click()
    self.driver.find_element(By.ID, "m_secondmodule_depApoText_01").send_keys(origin)
    self.driver.find_element(By.ID, "m_secondmodule_depApoText_01").send_keys(Keys.ENTER)

    # Destination
    self.driver.find_element(By.ID, "m_secondmodule_arrApoText_01").click()
    self.driver.find_element(By.ID, "m_secondmodule_arrApoText_01").send_keys(dest)
    self.driver.find_element(By.ID, "m_secondmodule_arrApoText_01").send_keys(Keys.ENTER)

    # Open the calendar
    self.driver.find_element(By.ID, "calTextId_Second_01").click()

    # Scroll until finding the month 
    calendar_name="#cal_Second_01_month_"+str(year)+zstr(month)
    while len(self.driver.find_elements(By.CSS_SELECTOR, calendar_name))==0 :
        self.driver.find_element(By.LINK_TEXT, "次の3ヶ月").click()

    # Click on the desired date on the calendar grid
    #   Monthly dump mode -> 1st day of the month
    #   Note: 
    weekNum = day_1stQuery.weekday()   #        Mon=0, ...       Sun=6
    columnNum = (weekNum+1) % 7 + 1    # Sun=1, Mon=2, ... Sat=7
    rowNum = int((day_1stQuery.day-1+(weekNum_1stDay+1)%7)/7)+1
    print('Click on (raw,col)=(%i,%i) on the calender %s' % (rowNum,columnNum,calendar_name))    
    self.driver.find_element(By.CSS_SELECTOR, calendar_name+" tr:nth-child("+str(rowNum)+") > td:nth-child("+str(columnNum)+")").click()

    # Start the inital query
    self.driver.find_element(By.NAME, "submitButtonName_Second").click()
    
    # Save & go over the rest of the month in case of a monthly query
    current_month = zstr(month)
    while current_month == zstr(month) :
    
        dateString = self.driver.find_element(By.CSS_SELECTOR, ".flightSummaryDate").text
        current_month = str(dateString.split('年')[1].split('月')[0])
        actualDate = dateString.replace('年','').replace('月','').replace('日','').split('(')[0]
        #print("actualDate: ",actualDate, " current_month: ", current_month)
        
        if current_month != zstr(month): break
        outFile = 'output/rawquery_'+origin+'_'+dest+'_'+actualDate+'.html'
        with open(outFile, 'w') as f:  f.write(self.driver.page_source)
        print('Generated '+outFile)

        # Move on to the next day in case of a monthly query
        if dumpWholeMonth : 
            self.driver.find_element(By.CSS_SELECTOR, "#nextDayButton > .jsRollOver").click()
            element = self.driver.find_element(By.CSS_SELECTOR, "#nextDayButton > .jsRollOver")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

        # Finish here if not
        else : break




######################################
parser = OptionParser(usage="usage : python ANAPremQuery.py -y [year] -m [month] (-d [day]) -O [origin] -D [destination]")
parser.add_option("-y", dest="year", type="int", default=2022, help="Year inquired")
parser.add_option("-m", dest="month", type="int", default=2, help="Month inquired")
parser.add_option("-d", dest="day", type="int", default=-1, help="(optional) Date inquired. Go over the whole month if <=0.")
parser.add_option("-O", dest="origin", type="string", default="haneda", help="Origin (all small capitals)")
parser.add_option("-D", dest="destination", type="string", default="naha", help="Destination (all small captals)")
parser.add_option("-b", dest="doHeadless", action="store_true", default=False, help="Run on batch mode (i.e. no browser window showing up)")

(options, args) = parser.parse_args()

###########
browser = ANAPremQuery()
browser.setup_method(options.doHeadless)
browser.doQuery(options.origin, options.destination, options.year, options.month, options.day) 
browser.teardown_method()

