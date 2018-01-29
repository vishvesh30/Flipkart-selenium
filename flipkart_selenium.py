from math import ceil
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver1 = webdriver.Edge()
driver2 = webdriver.Ie()

options = webdriver.ChromeOptions()
options.binary_location = "C:\\Program Files (x86)\\Opera\\50.0.2762.67\\opera.exe"# path to opera executable
driver3 = webdriver.Opera(options=options)
final_data = []
#final_data['Product'] = []
product_data = {}
review_title_list = []
review_text_list = []
output_file = open('data.json', 'w', encoding='utf-8')


def product_list():
    url = "https://www.flipkart.com/air-conditioners/pr?sid=j9e,abm,c54&otracker=categorytree"
    driver1.get(url)

    total_string = driver1.find_element_by_xpath('//div[@class="_1JKxvj _31rYcN"]/span/span')
    page_data = str(total_string.text).split(" ")
    total_page = int(page_data[3])
    page_no = 1
    while page_no <= total_page:
        print("in while loop product list")
        temp_url = url + "&page=" + str(page_no) + "&viewType=list"
        print(temp_url)
        driver1.get(temp_url)
        for link_tag in driver1.find_elements_by_class_name("_1UoZlX"):
            half_link = link_tag.get_attribute("href")
            product(half_link)
        print("after for loop")
        page_no += 1
    print("exit while loop")


def product(url):
    # url = "https://www.flipkart.com/apple-iphone-x-silver-256-gb/p/itmexrgv4cgmrxxp?pid=MOBEXRGVVTMF9FYV&srno=s_1_2&otracker=search&lid=LSTMOBEXRGVVTMF9FYVKHKOAY&fm=SEARCH&iid=c096c9b3-b065-42fe-86d6-3dad683a2532.MOBEXRGVVTMF9FYV.SEARCH&ppt=Search%20Page&ppn=Search%20Page&ssid=pdpdvo49b40000001516342964696&qH=882a0465d260983a"
    driver2.get(url)
    try:
        link_tag = driver2.find_element_by_xpath('//div[@class="col _39LH-M"]/a')
        link = str(link_tag.get_attribute("href"))
        total_review_line = link_tag.find_element_by_xpath('//div[@class="swINJg _3nrCtb"]/span')
        count = total_review_line.text.split(" ")
        review_count = int(count[2])
        total_pages = ceil(review_count / 10)
        product_name_tag = driver2.find_element_by_xpath('//h1[@class="_3eAQiD"]')
        product_name = product_name_tag.text
        review(link, total_pages, product_name)
    except:
        print("No review on url " + url)


def review(link, total_pages, product_name):
    page = 1
    while page <= total_pages:
        url = link + "&page=" + str(
            page)
        # print(url)
        driver3.get(url)

        for span_more in driver3.find_elements_by_class_name("_1EPkIx"):
            span_more.click()

        for title in driver3.find_elements_by_class_name("_2xg6Ul"):
            review_title_list.append(title.text)
        for div_element in driver3.find_elements_by_xpath('//div[@class="qwjRop"]/div/div'):
            review_text_list.append(div_element.text)
        page += 1

    process(product_name)


def process(product_name):
    product_data['review'] = []
    for i in range(len(review_title_list)):
        #     product_data['review'].append({
        #         'Review_title': review_title_list[i],
        #         'Review_text': review_text_list[i]
        #     })
        final_data.append({
            'Name': product_name,
            'Review_title': review_title_list[i],
            'Review_text': review_text_list[i]
        })

    review_text_list.clear()
    review_title_list.clear()


def write():
    json.dump(final_data, output_file)
    # print(final_data)


product_list()
write()
print("exit")
driver1.close()
driver2.close()
driver3.close()
output_file.close()
