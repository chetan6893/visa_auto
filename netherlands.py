import time
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.support.ui import Select
import datetime
import dateparser
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

url = 'https://www.netherlandsandyou.nl/your-country-and-the-netherlands/ireland/about-us/embassy-in-dublin'
#driver = webdriver.Chrome(chrome_options=chrome_options, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver = webdriver.Chrome(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.get(url)
print "sleeping for 5 sec"
time.sleep(5)
driver.find_element_by_xpath("//a[@aria-label='appointment (opens external website)']").click()
driver.find_element_by_xpath("//*[text()='Schedule Appointment ']").click()
select = Select(driver.find_element_by_xpath("//select[contains(@id,'VisaCategory')]"))
select.select_by_visible_text('Visa – Schengen area, tourism')
driver.find_element_by_xpath("//input[@value='Continue']").click()
#Enter details
Select(driver.find_element_by_xpath("//select[contains(@id,'Title')]")).select_by_visible_text('MR.')
driver.find_element_by_xpath("//input[contains(@name,'FName')]").send_keys("Chetan")
driver.find_element_by_xpath("//input[contains(@name,'LName')]").send_keys("Ramachandra")
driver.find_element_by_xpath("//input[contains(@name,'ContactNumber')]").send_keys("0892160549")
driver.find_element_by_xpath("//input[contains(@name,'EmailAddress')]").send_keys("chetan.ireland@gmail.com")
Select(driver.find_element_by_xpath("//select[contains(@name,'Confirmation')]")).select_by_visible_text('I confirm the above statement')
driver.find_element_by_xpath("//input[@value='Continue']").click()
#Get page from calender
soup = BeautifulSoup(driver.page_source)
opendates = soup.findAll('td',attrs={'class': 'OpenDateAllocated'})
best_date = dateparser.parse('Dec 30')
java_href = ''
for date in opendates:
    child = date.findChild()
    if dateparser.parse(child['title']) < best_date:
        best_date = dateparser.parse(child['title'])
        java_href = child['href']
        best_xpath = "//a[@title='{}']".format(child['title'])
        print "date available - {}".format(best_date)
        #click on date
        driver.find_element_by_xpath(best_xpath).click()
        #click on popup
        driver.find_element_by_xpath("//a[contains(@id, 'TimeSlot')]").click()
        # handle popup
        driver.switch_to_alert().accept()
        break
