import scrapy
import requests
import os
from bs4 import BeautifulSoup as soup
import json

class productSpider(scrapy.Spider):
	name = "pepperfry_spider"
	# Directory were all the scraped data will be saved
	parent_Dir = "C:/Users/ASUS/Desktop/Challenge - Scrape a Shopping Website/Scraped Products/"
	Max_cnt = 20
	
	def start_requests(self):
		# all the products to be scraped
		product_list = [
						"arm-chairs","bean-bags","bench","book-cases","chest-drawers","coffee-table",
						"dinning-set","garden-seating","king-beds","queen-beds","two-seater-sofa"
					   ]
		base_url = "https://www.pepperfry.com/site_product/search?q="

		urls = []
		dir_names = []

		for product in product_list:
			query_string = '+'.join(product.split('-'))
			urls.append(base_url+query_string)
			dir_name = self.parent_Dir+product
			dir_names.append(dir_name)
			if not os.path.exists(dir_name):
				os.makedirs(dir_name)

		for i in range(len(urls)):
			resp = scrapy.Request(url = urls[i],callback = self.parse,dont_filter = True)
			resp.meta['dir_name'] = dir_names[i]
			yield resp


	def parse(self,response,**meta):
		counter=0
		product_url = response.xpath("//div[@class = 'clipCard__hd ']/a/@href").extract()
		for url in product_url:
			resp = scrapy.Request(url = url,callback = self.parse_item,dont_filter=True)
			resp.meta['dir_name'] = response.meta['dir_name']

			if counter==self.Max_cnt:
				break
			else:
				counter+=1
			yield resp
		
	def parse_item(self,response,**meta):
		# print(response)
		item_name = '-'.join(response.xpath("//h1[@class='vip-pro-hd']/text()").extract())
		item_dir = response.meta['dir_name']+"/"+item_name
		# print(item_dir)
		item_metaData = {
			"title" : '-'.join(response.xpath("//h1[@class='vip-pro-hd']/text()").extract()),
			"price" : response.xpath("//span[@class='vip-eff-price-amt']/text()").extract()[0],
			"savings" : response.xpath("//span[@class='vip-saved-price-amt']/text()").extract()[0],
			"description" : ' '.join(response.xpath("//div[@id='additional_info_tab']/div/ul/li/text()").extract()),
		}

		item_detail_keys = response.xpath("//span[@class='vip-prod-dtl-ttl col-secondary pf-block']/text()").extract()
		itemp_detail_values = response.xpath("//span[@class='vip-prod-dtl-subttl pf-block']/text()").extract()

		for i in range(len(item_detail_keys)):
			item_metaData[item_detail_keys[i]] = itemp_detail_values[i] 


		if not os.path.exists(item_dir):
			os.makedirs(item_dir)

		item_str_metaData = json.dumps(item_metaData)

		with open(item_dir+"/"+"meta_data.txt",'w') as f:
			f.write(item_str_metaData)

		all_images = response.xpath("//img[@class='vipImage__thumb-each-pic']/@data-src").extract()			
		
		for idx,images in enumerate(all_images):
			r1 = requests.get(images)
			print(r1)
			filename = "images-"+str(idx)+".jpg"
			with open(os.path.join(item_dir,filename),'wb') as f:
				f.write(r1.content)
				
