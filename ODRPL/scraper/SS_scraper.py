from typing import no_type_check_decorator
from . import constants
import sys, os, time, json, re
from .download import download_file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
from collections import OrderedDict

"""
method to remove unwanted words, duplicate 
sentences, and white-spaces from a string """
def clean_text(test_str, word_list, repl_wrd):
	res = re.sub("|".join(sorted(word_list, key = len, reverse = True)), repl_wrd, test_str)
	res = ". ".join(list(OrderedDict.fromkeys(res.split(". ")))) # removes duplicate sentences
	res = " ".join(res.split()) # removes extra white-spaces
	return res

"""
method to scrape the following information of only open-access
papers, which have PDF available from Semantic Scholar site:

1. URL
2. PDF_URL
3. Title
4. Abstract """
def scrape_papers_info(query_str):
	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')

	if 'HEROKU_ENV' in os.environ:
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")

	driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
	driver.maximize_window()

	driver.get('https://www.semanticscholar.org/')
	search_bar = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
	search_bar.send_keys(query_str)
	search_bar.submit()

	while True:
		try:
			main_div = driver.find_element(By.CLASS_NAME, 'result-page')
			break
		except Exception as e:
			print("DOM loading...\n")

	time.sleep(2)

	# try if there are any pages
	try:
		pagination_div = driver.find_element(By.CLASS_NAME, 'cl-pager')
	except Exception as e:
		return False

	pages = pagination_div.find_elements_by_css_selector('div.cl-pager__button.cl-pager__number')
	no_of_pages = len(pages)

	flag = []; # array for keeping track of results that have open-access PDFs
	urls = []; pdf_urls = []; titles = []; abstracts = []

	for x in range(no_of_pages):
		while True:
			try:
				main_div = driver.find_element(By.CLASS_NAME, 'result-page')
				splits = main_div.find_elements_by_css_selector('.cl-paper-row.serp-papers__paper-row.paper-row-normal')
				break
			except Exception as e:
				pass
		
		temp = []
		url_hrefs = []; pdf_url_hrefs = []; title_spans = []
		abstract_spans = []; abstract_expand_btns = []

		empty_flag = True # if pdf is not available
		no_of_results = len(splits)

		for y in range(no_of_results):

			while True:
				try:
					pdf_btn = splits[y].find_element_by_css_selector('span.cl-button__label')
					break
				except Exception as e:
					pass

			if pdf_btn.text == "View PDF on arXiv":
				empty_flag = False

				# PDFs
				pdf_url = splits[y].find_element_by_css_selector('a.flex-row.cl-paper-view-paper')
				pdf_url_hrefs.append(pdf_url)

				# Let's now pick abstracts!!!
				try:
					abstract_div = splits[y].find_element_by_css_selector('div.tldr-abstract-replacement')
				except:	# try second option
					abstract_div = splits[y].find_element_by_css_selector('div.cl-paper-abstract')

				# abstracts
				abstract_spans.append(abstract_div)
				abstract_expand_btns.append(abstract_div.find_element_by_css_selector('span.more.mod-clickable'))
				
				# urls and titles
				url_hrefs.append(splits[y].find_element_by_css_selector('div.cl-paper-row.serp-papers__paper-row > a'))
				title_spans.append(splits[y].find_element_by_css_selector('div.cl-paper-title'))

				print("Result {}:".format(y + 1), pdf_url.get_attribute('href'), "\n")
				temp.append(True)

			else:
				temp.append(False)

		# if there are PDFs on the page
		if not empty_flag:
			# click abstract expand-links
			for btn in abstract_expand_btns:
				WebDriverWait(driver, constants.TIMEOUT).until(EC.visibility_of(btn))
				
				# wait until button is not clickable
				while True:
					try:
						time.sleep(0.5)
						driver.execute_script("arguments[0].click();", btn)
						break
					except Exception as e:
						pass

			# save text in separate lists
			for url, pdf_url, title, abstract in zip(
				url_hrefs, pdf_url_hrefs, title_spans, abstract_spans):

				urls.append(url.get_attribute('href'))
				pdf_urls.append(pdf_url.get_attribute('href'))
				titles.append(title.text)
				abstracts.append(abstract.text)

		flag.append(temp)
		print("\nPage {}:".format(x + 1), flag[x], "\n")
		print("-------------------------------------\n")

		# does not click the next page if it's the last one
		if x == no_of_pages - 1:
			continue

		WebDriverWait(driver, constants.TIMEOUT).until(EC.visibility_of(pages[x + 1]))

		while True:
			try:
				driver.execute_script("arguments[0].click();", pages[x + 1])
				break
			except Exception as e:
				pass
		
		# halt a little bit to let the next page load properly
		time.sleep(3)

	# save the final result
	list_ = []

	for url, pdf_url, title, abstract in zip(
		urls, pdf_urls, titles, abstracts):
		"""
		# download PDF
		filename = 1
		download_file(pdf_url, str(filename))
		filename += 1
		"""
		word_list = ["TLDR\n", "\nAbstract", "Expand", "Collapse"]

		list_.append(
			{
				"url": url,
				"pdf_url": pdf_url,
				"title": title,
				"abstract": clean_text(abstract, word_list, "")
			}
		)

	print("\n\n----------------------------------\n\n")
	print(json.dumps(list_, sort_keys=False, indent=4))
	""""
	with open("sample.json", "w") as outfile: 
		json.dump(list_, outfile)
	"""
	driver.close()
	return list_

if __name__ == "__main__":

	query = "machine learning"
	info_elements = scrape_papers_info(query)