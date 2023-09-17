import time
import undetected_chromedriver
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import json
import requests
import asyncio
from sql_queries import sql_Avito, sql_Cian, sql_Domclick



class Avito:
    def __init__(self, url="https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?context"
                     "=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA"
                     "&p=", headless=False, to_json=True, to_database=False):
        self.url = url
        self.headless = headless
        self.to_json = to_json
        self.to_database = to_database

    def get_data(self):
        result_page = {}
        count_page = 20
        for page in range(1, count_page + 1):
            try:
                print("DRIVER CONNECTING...")
                options = Options()
                if self.headless:
                    options.add_argument('--headless')
                driver = undetected_chromedriver.Chrome(executable_path="chromedriver.exe", options=options)
                print("DRIVER CONNECTED")
                driver.get(url=f"{self.url}{page}")
                print("PAGE LOADED!")
                result = {}

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")
                container = soup.find("div", class_="items-items-kAJAg")
                items = container.find_all("div", class_="iva-item-root-_lk9K")

                count = 0
                for item in items:
                    count += 1
                    print(f"Process #{count}/{len(items)}...")

                    href = title = description = address = metro = img = "Not found"

                    try:
                        href = f'https://www.avito.ru{item.find("div", class_="iva-item-title-py3i_").find("a").get("href")}'
                    except Exception as ex:
                        pass

                    try:
                        title = item.find("div", class_="iva-item-title-py3i_").find("h3").text.strip().replace(" ", "")
                    except Exception as ex:
                        pass

                    try:
                        price = int(item.find("div", class_="iva-item-priceStep-uq2CQ").find("span").find("p",
                                                                                                      class_="styles-module-root-_KFFt").text.strip().replace(" ", "").replace(" ", "").replace("₽", ""))
                    except Exception as ex:
                        price = 0

                    try:
                        address = item.find("div", class_="geo-root-zPwRk").find("p").find("span").text
                        metro = item.find("div", class_="geo-root-zPwRk").find("p",
                                                                               class_="styles-module-margin-top_0-_usAN").find(
                            "span", class_="geo-icons-uMILt").find_next("span").text
                    except Exception as ex:
                        pass

                    try:
                        description = item.find("div", class_="iva-item-descriptionStep-C0ty1").find("p").text.rstrip().replace("\n", "")
                    except Exception as ex:
                        pass

                    try:
                        img = item.find("div", class_="photo-slider-photoSlider-Eyzg_").find("li",
                                                                                             class_="photo-slider-list-item-h3A51").get(
                            "data-marker").replace("slider-image/image-", "")
                    except Exception as ex:
                        pass

                    res = {
                        "website": "avito",
                        "href": href,
                        "title": title,
                        "price": price,
                        "address": address,
                        "metro": metro,
                        "description": description,
                        "img": img
                    }


                    if self.to_database:
                        sql_Avito(
                            href=href,
                            title=title,
                            price=price,
                            address=address,
                            metro=metro,
                            description=description,
                            img=img
                        )

                    result[f"item_{count}"] = res
                    print(f"Appartment: {title} was parsed successfully!")
                    print("Next item...", "\n")
                    time.sleep(0.05)

                result_page[f"Page_{page}"] = result
                print(f"Page #{page}/{count_page} was parsed")
                print("Parsing next page!")


            except Exception as ex:
                print(ex)

            finally:
                driver.close()
                driver.quit()


            if self.to_json:
                with open("result_json_avito.json", "w", encoding="utf-8") as file:
                    json.dump([result_page], file, indent=4, ensure_ascii=False)







class DomClick:
    def __init__(self, url="https://domclick.ru/search?deal_type=sale&category=living&offer_type=flat&offer_type=layout&aids=2299&offset=", headless=False, to_json=True, to_database=False):
        self.url = url
        self.headless = headless
        self.proxies = {
            "https": "https://52.183.8.192:3128"
        }

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        self.to_json = to_json
        self.to_database = to_database


    def get_data(self):
        result_page = {}
        page_items = 20
        count_page = 4 * page_items
        try:
            for page in range(20, count_page, 20):
                try:
                    options = Options()
                    if self.headless:
                        options.add_argument('--headless')
                        options.proxy = self.proxies
                    # driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
                    driver = undetected_chromedriver.Chrome(executable_path="chromedriver.exe", options=options)
                    driver.get(url=f"{self.url}{page}")
                    time.sleep(10)

                    result = {}

                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")
                    main_block_items = soup.find("div", class_="o9A9H")
                    list_items = main_block_items.find_all("div", class_="NrWKB")

                    for count, list_item in enumerate(list_items):
                        href = list_item.find("a", class_='a4tiB2').get("href")
                        title = " ".join([item.text for item in list_item.find_all("span", class_="_6KKuHL")])
                        price = int(list_item.find("p", class_="Z4r7pA").text.replace(" ", "").replace("₽", ""))
                        address = list_item.find(attrs={"data-e2-id": 'product-snippet-address'}).text
                        try:
                            metro = list_item.find("div", class_="_6Ht-Tx").find("span", class_='gzUns0').text
                        except Exception as ex:
                            metro = None

                        try:
                            description = list_item.find("div", class_="_8MNxzN").text.replace("\n", "")
                        except Exception as ex:
                            description = None
                        img = list_item.find("picture", class_="picture-picture-content-0-9-1").find("img").get("src")
                        #

                        res = {
                            "website": "domclick",
                            "href": href,
                            "title": title,
                            "price": price,
                            "address": address,
                            "metro": metro,
                            "description": description,
                            "img": img
                        }

                        if self.to_database:
                            sql_Domclick(
                                href=href,
                                title=title,
                                price=price,
                                address=address,
                                metro=metro,
                                description=description,
                                img=img
                            )
                        result[f"item_{count + 1}"] = res
                        print(f"Appartment: {title} was parsed successfully!")
                        print("Next item...", "\n")
                        time.sleep(0.05)

                    result_page[f"Page_{int(page / 20) + 1}"] = result
                    print(f"Page #{int(page / 20) + 1}/{int(count_page / 20)} was parsed")
                    print("Parsing next page!")



                except Exception as ex:
                    print(ex)

                finally:
                    driver.close()
                    driver.quit()
                    time.sleep(5)

                if page > 20:
                    break
        except Exception as ex:
            print(ex)

        finally:
            with open("result_json_domClick.json", "w", encoding="utf-8") as file:
                json.dump(result_page, file, indent=4, ensure_ascii=False)


class Cian:
    def __init__(self, url="https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=", headless=False, to_json=True, to_database=False):
        self.url = url
        self.headless = headless
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        self.to_json = to_json
        self.to_database = to_database

    def get_data(self):
        result_page = {}

        pages = 20

        try:
            for page in range(1, pages + 1):
                request = requests.get(url=f"{self.url}{page}", headers=self.headers)

                soup = BeautifulSoup(request.text, "lxml")
                items = soup.find_all("div", class_="_93444fe79c--card--ibP42 _93444fe79c--wide--gEKNN")
                count = 0
                result = {}
                for item in items:
                    count += 1

                    item_href = item.find("a", class_="_93444fe79c--media--9P6wN").get("href")
                    item_title = item.find("span", {"data-mark": "OfferTitle"}).text.strip().replace(" ", "")
                    item_price = int(item.find("span", {"data-mark": "MainPrice"}).text.strip().replace(" ", "").replace(" ", "").replace("₽", ""))
                    item_address = item.find("div", class_="_93444fe79c--labels--L8WyJ").text
                    try:
                        item_metro = item.find("div", class_="_93444fe79c--container--w7txv").find("a").text
                    except Exception as ex:
                        item_metro = "Not found"
                    try:
                        item_description = item.find("div", class_="_93444fe79c--description--SqTNp").find("p").text.rstrip().replace("\n", "")
                    except Exception as ex:
                        item_description = "Not found"

                    item_image = item.find("ul", class_="_93444fe79c--container--Pf0cj").find("li", class_="_93444fe79c--container--Havpv").find("img").get("src")

                    res = {
                        "website": "cian",
                        "href": item_href,
                        "title": item_title,
                        "price": item_price,
                        "address": item_address,
                        "metro": item_metro,
                        "description": item_description,
                        "img": item_image
                    }


                    if self.to_database:
                        sql_Cian(
                            href=item_href,
                            title=item_title,
                            price=item_price,
                            address=item_address,
                            metro=item_metro,
                            description=item_description,
                            img=item_image
                        )


                    result[f"item_{count}"] = res
                    print(f"Appartment: {item_title} was parsed successfully!")
                    print("Next item...", "\n")
                    time.sleep(0.05)

                result_page[f"Page_{page}"] = result
                print(f"Page #{page}/{pages} was parsed")
                print("Parsing next page!")




        except Exception as ex:
            print(ex)

        with open("result_json_cian.json", "a", encoding="utf-8") as file:
            json.dump(result_page, file, indent=4, ensure_ascii=False)



def main():
    avito_obj = Avito(to_database=True, headless=True, to_json=False)
    domclick_obj = DomClick(to_database=False, headless=False, to_json=False)
    cian_obj = Cian(to_database=True, headless=True, to_json=False)

    '''   RUN    '''
    avito_obj.get_data()
    cian_obj.get_data()
    # domclick_obj.get_data()


if __name__ == '__main__':
    main()



