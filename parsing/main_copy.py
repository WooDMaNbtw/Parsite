# import time
# import undetected_chromedriver
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
# import json
# import requests
#
#
# class Avito:
#     def __init__(self, url="https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?context"
#                            "=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA"
#                            "&p=", headless=True):
#         self.url = url
#         self.headless = headless
#
#     def get_data(self):
#         result_page = {}
#         count_page = 4
#
#         for page in range(1, count_page + 1):
#             driver = undetected_chromedriver.Chrome(headless=self.headless)
#             try:
#                 driver.get(url=f"{self.url}{page}")
#                 time.sleep(5)
#                 result = {}
#
#                 src = driver.page_source
#                 soup = BeautifulSoup(src, "lxml")
#                 container = soup.find("div", class_="items-items-kAJAg")
#                 items = container.find_all("div", class_="iva-item-root-_lk9K")
#
#                 count = 0
#                 for item in items:
#                     count += 1
#                     print(f"Process #{count}/{len(items)}...")
#
#                     href = title = price = description = address = metro = img = "Not found"
#
#                     try:
#                         href = f'https://www.avito.ru{item.find("div", class_="iva-item-title-py3i_").find("a").get("href")}'
#                     except Exception as ex:
#                         pass
#
#                     try:
#                         title = item.find("div", class_="iva-item-title-py3i_").find("h3").text
#                     except Exception as ex:
#                         pass
#
#                     try:
#                         price = item.find("div", class_="iva-item-priceStep-uq2CQ").find("span").find("p",
#                                                                                                       class_="styles-module-root-_KFFt").text
#                     except Exception as ex:
#                         pass
#
#                     try:
#                         address = item.find("div", class_="geo-root-zPwRk").find("p").find("span").text
#                         metro = item.find("div", class_="geo-root-zPwRk").find("p",
#                                                                                class_="styles-module-margin-top_0-_usAN").find(
#                             "span", class_="geo-icons-uMILt").find_next("span").text
#                     except Exception as ex:
#                         pass
#
#                     try:
#                         description = item.find("div", class_="iva-item-descriptionStep-C0ty1").find("p").text
#                     except Exception as ex:
#                         pass
#
#                     try:
#                         img = item.find("div", class_="photo-slider-photoSlider-Eyzg_").find("li",
#                                                                                              class_="photo-slider-list-item-h3A51").get(
#                             "data-marker").replace("slider-image/image-", "")
#                     except Exception as ex:
#                         pass
#
#                     res = {
#                         "href": href,
#                         "title": title.strip().replace(" ", ""),
#                         "price": price.strip().replace(" ", ""),
#                         "address": address,
#                         "metro": metro,
#                         "description": description.rstrip().replace("\n", ""),
#                         "img": img
#                     }
#
#                     result[f"item_{count}"] = res
#                     print(f"Appartment: {title} was parsed successfully!")
#                     print("Next item...", "\n")
#                     time.sleep(0.05)
#
#                 result_page[f"Page_{page}"] = result
#                 print(f"Page #{page}/{count_page} was parsed")
#                 print("Parsing next page!")
#
#
#             except Exception as ex:
#                 print(ex)
#
#             finally:
#                 driver.close()
#                 driver.quit()
#
#             with open("result_json_avito.json", "a", encoding="utf-8") as file:
#                 json.dump([result_page], file, indent=4, ensure_ascii=False)
#         # time.sleep(10)
#
#
# obj = Avito()
# obj.get_data()
#
#
# class DomClick:
#     def __init__(self, url="https://domclick.ru/search?deal_type="
#                            "sale&category=living&offer_type=flat&offer_type=layout&offset=", headless=False):
#         self.url = url
#         self.headless = headless
#
#     '''
#
#     NEED TO BE CHANGED! TAGS!
#
#     '''
#
#     def get_data(self):
#         result_page = {}
#         page_items = 20
#         count_page = 40 * page_items
#         try:
#             for page in range(1, count_page, 20):
#                 print(f"{self.url}{page}")
#                 driver = undetected_chromedriver.Chrome(headless=self.headless)
#                 try:
#                     driver.get(url=f"{self.url}{page}")
#                     time.sleep(10)
#
#                     result = {}
#
#                     src = driver.page_source
#                     soup = BeautifulSoup(src, "lxml")
#                     main_block_items = soup.find("div", class_="o9A9H")
#                     list_items = main_block_items.find_all("div", class_="NrWKB")
#
#                     for count, list_item in enumerate(list_items):
#                         href = list_item.find("a", class_='a4tiB2').get("href")
#                         title = " ".join([item.text for item in list_item.find_all("span", class_="_6KKuHL")])
#                         price = list_item.find("p", class_="Z4r7pA").text
#                         address = list_item.find(attrs={"data-e2-id": 'product-snippet-address'}).text
#                         try:
#                             metro = list_item.find("div", class_="_6Ht-Tx").find("span", class_='gzUns0').text
#                         except Exception as ex:
#                             metro = None
#
#                         try:
#                             description = list_item.find("div", class_="_8MNxzN").text.replace("\n", "")
#                         except Exception as ex:
#                             description = None
#                         img = list_item.find("picture", class_="picture-picture-content-0-9-1").find("img").get("src")
#                         #
#
#                         res = {
#                             "href": href,
#                             "title": title,
#                             "price": price,
#                             "address": address,
#                             "metro": metro,
#                             "description": description,
#                             "img": img
#                         }
#
#                         result[f"item_{count + 1}"] = res
#                         print(f"Appartment: {title} was parsed successfully!")
#                         print("Next item...", "\n")
#                         time.sleep(0.05)
#
#                     result_page[f"Page_{int(page / 20) + 1}"] = result
#                     print(f"Page #{int(page / 20) + 1}/{int(count_page / 20)} was parsed")
#                     print("Parsing next page!")
#
#
#
#                 except Exception as ex:
#                     print(ex)
#
#                 finally:
#                     driver.close()
#                     driver.quit()
#                     time.sleep(5)
#
#                 if page > 60:
#                     break
#         except Exception as ex:
#             print(ex)
#
#         finally:
#             with open("result_json_domClick.json", "w", encoding="utf-8") as file:
#                 json.dump(result_page, file, indent=4, ensure_ascii=False)
#
#
# # obj = DomClick()
# # obj.get_data()
#
#
# class Cian:
#     def __init__(self, url="https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=",
#                  headless=False):
#         self.url = url
#         self.headless = headless
#         self.headers = {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#         }
#
#     def get_data(self):
#         request = requests.get(url=self.url, headers=self.headers)
#
#         soup = BeautifulSoup(request.text, "lxml")
#         items = soup.find_all("div", class_="_93444fe79c--card--ibP42 _93444fe79c--wide--gEKNN")
#         count = 0
#         for item in items:
#             try:
#                 count += 1
#                 item_href = item.find("a", class_="_93444fe79c--media--9P6wN").get("href")
#                 item_info = item.find("div", class_="_93444fe79c--subtitle--vHiOV").text
#                 print(item_href)
#                 print(item_info)
#             except Exception as ex:
#                 pass
#
#         print(count)
#
# # obj = Cian()
# # obj.get_data()
#
#
#
