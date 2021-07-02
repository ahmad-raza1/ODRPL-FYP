from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View
from numpy.core.arrayprint import _leading_trailing

from .scraper import SS_scraper as scrp
from .text_similarity import zero_shot_classifier as zsc

import ast, json
import numpy as np


def index(request):
	return render(request, "index.html")


def abstracts(request):

	if request.method == "POST":
		query_text = str(request.POST["InputSubject"])
		query_text = " ".join(query_text.split())
		
		# clearing extra/duplicate whitespaces
		query_text = " ".join(query_text.split())
		"""
		file = open("sample.json", "r")
		content = file.read()
		papers = ast.literal_eval(content)
		file.close()

		request.session["papers"] = papers

		#print(json.dumps(scores, sort_keys=False, indent=4))

		context = {
			"query_text": query_text,
			"papers": papers
		}

		return render(request, "abstracts.html", context)
		"""
		papers = scrp.scrape_papers_info(query_text)

		if papers:	
			request.session["query_text"] = query_text
			abstracts = [paper["abstract"] for paper in papers]
			
			result = zsc.compute_relevance_scores(query_text, abstracts)
			print("\n\n----------------------------------\n\n")

			scores = np.around(result["scores"], decimals=2)
			print(scores)
			
			for x in range(len(papers)):
				papers[x]["score"] = int(scores[x] * 100)
				
			#with open("sample.json", "w") as outfile: 
			#	json.dump(papers, outfile)

			print(json.dumps(papers, sort_keys=False, indent=4))
			request.session["papers"] = papers

			context = {
				"query_text": query_text,
				"papers": papers
			}

			return render(request, "abstracts.html", context)

		else:
			return HttpResponse("<h1>No results found!</h1>")

	return redirect("index")


def	full_papers(request):

	if request.method == "POST":
		try:
			query_text = request.session["query_text"]
			papers = request.session["papers"]
		except:
			raise Http404("Error!")

		check_boxes = request.POST.getlist("check")

		if check_boxes:
			chkd_checkboxes_indices = []
			length = len(check_boxes)

			for x in range(length):
				chkd_checkboxes_indices.append(int(check_boxes[x]))

			selected_papers = []

			for x in chkd_checkboxes_indices:
				selected_papers.append(papers[x-1])

			print("\n\n--------------------------------------------\n\n")
			print(json.dumps(selected_papers, sort_keys=False, indent=4))
			
			context = {
				"query_text": query_text,
				"selected_papers": selected_papers
			}

			return render(request, "full_papers.html", context)

	return redirect("abstracts")