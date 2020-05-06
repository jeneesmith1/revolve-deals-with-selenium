import selenium, time, argparse
from selenium import webdriver
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from csv import writer
from twilio.rest import Client

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

def rt(d):
    times = np.random.rand(1000)+np.random.rand(1000)+d
    return np.random.choice(times, 1).tolist()[0]

def deploy_revolve(s, c, o, n):
    url = 'https://www.revolve.com/'
    driver.get(url)

    time.sleep(rt(5))

    try:
        #Sales
        sales_tab = driver.find_element_by_id("tr-main-nav-sale")
        sales_tab.send_keys(Keys.RETURN)
        time.sleep(rt(2))
        print("Gone to sales page")

        try:
            # see if I can filter
            category_selector = "a[title='" + c +  "']"
            filter_by_type = driver.find_element_by_css_selector(category_selector)
            filter_by_type.send_keys(Keys.RETURN)
            time.sleep(rt(5))

            # select size page
            filter_by_size(s)
            time.sleep(rt(5))

            # sort by price low to high
            selection = driver.find_elements_by_xpath("//div[contains(@class, 'js-dropdown dropdown dropdown--center u-inline-block')]")[0]
            selection.click()
            time.sleep(rt(5))

            order_page(o)
            product_info = get_product_descriptions(get_product_links(n))
            add_descriptions_to_csv(product_info)
            twilio_alert(product_info)
  
        except Exception as e:
            print (e)
            print("Something went wrong while filtering")
            pass

    except:
        print("ERROR -- something has happened while deploying")
        import pdb
        pdb.set_trace()
        pass

def filter_by_size(s):
    #select the size of clothing or shoes you want
    sizes = {
        "xs": "extra-small",
        "sm": "apparel-small",
        "m": "medium",
        "l": "apparel-large",
        "23": "23",
        "24": "24",
        "25": "25",
        "26": "26",
        "27": "27",
        "28": "28",
        "29": "29",
        "30": "30",
        "5": "56",
        "5.5": "56",
        "6": "67",
        "6.5": "67",
        "7": "78",
        "7.5": "78",
        "8": "89",
        "8.5": "89",
        "9": "910",
        "9.5": "910",
        "10": "1011",
        "10.5": "1011",
        "11": "1011"
    }
    if s in sizes:
        size_selector = "a[href*='" + sizes[s] + "'"
        size_page = driver.find_element_by_css_selector(size_selector)
        size_page.send_keys(Keys.RETURN)

def order_page(o):
    #order the page
    ordering = {
        'low-to-high': "js-sort-by-price", 
        'high-to-low': "js-sort-by-priced", 
        'newest': "js-sort-by-newestMarkdown", 
        'most-popular': "js-sort-by-popularity", 
        'featured': "js-sort-by-featured",
        'designer': "js-sort-by-designer"
    }

    if o in ordering:
        sort = driver.find_element_by_id("js-sort-by-price")
        sort.click()
        time.sleep(rt(5))

def get_product_links(n=4):
    print("[*] GETTING PRODUCT LINKS")
    items = driver.find_elements_by_class_name("product-link")
    urls = []
    for x in range(0, n):
        urls.append(items[x].get_attribute('href'))
    return urls

def get_product_descriptions(urls):
    print("[*] GETTING PRODUCT INFORMATION")
    product_information = []
    for url in urls:
        driver.get(url)
        time.sleep(rt(5))

        try:
            #get product info
            image = driver.find_element_by_id("img_2").get_attribute('src')
            product_name = driver.find_element_by_class_name("product-name--lg").text
            product_brand = driver.find_element_by_class_name("product-brand--lg").text
            price = driver.find_element_by_id("markdownPrice").text
            product_information.append([price, image, url, product_name, product_brand])

        except:
            print("Product info failed")

    return product_information

def add_descriptions_to_csv(product_information):
    with open("revolve.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        for product in product_information:
            csv_writer.writerow(product)
        print("[*] ADDING TO CSV")


def twilio_alert(product_information):
    account_sid = '[YOUR ACCOUNT SID]'
    auth_token = '[YOUR AUTH TOKEN]'
    client = Client(account_sid, auth_token)
    for product in product_information:
        message_body = product[3] + " from " + product[4] + " only " + product[0]
        message = client.messages \
            .create(
                body=message_body,
                messaging_service_sid='[YOUR MESSAGING SERVICE SID]',
                media_url=[product[1]],
                to='[YOUR PHONE NUMBER]'
            )
        print(message.sid)



if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", default=7200, type=float, help="time in seconds")
    parser.add_argument("-n", "--number", default=4, type=int, help="number of items")
    parser.add_argument("-s", "--size", default="xs", help="indicate size to search for",\
        choices=['xs', 'sm', 'm', 'l', 'xl', '23', '24', '25', '26', '27', '7', '7.5'])
    parser.add_argument("-c", "--category", default="Apparel",\
        help="indicate category to search for", choices=['Apparel', 'Denim', 'Shoes'])
    parser.add_argument("-o", "--order", default="low-to-high",\
        help="indicate how you want to sort ", \
        choices=['low-to-high', 'high-to-low', 'newest', 'popular', 'featured', 'designer'])
    args = parser.parse_args()

    #Start Share War Loop
    starttime=time.time()

    while True:
        #Start Driver, Get URLS, Close
        driver = webdriver.Chrome()
        driver.implicitly_wait(0)

        #Time Delay: While Loop
        random_loop_time = rt(args.time)

        #Run Main App
        deploy_revolve(args.size, args.category, args.order, args.number)
        
        
        print("Closing driver")
        time.sleep(rt(10))
        driver.close()

        #Time Delay: While Loop
        time.sleep(random_loop_time - ((time.time() - starttime) % random_loop_time))
