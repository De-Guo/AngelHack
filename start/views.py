
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

from django.conf import settings

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
#from .models import ModelWithFileField

from django.core.files.storage import FileSystemStorage


""" Tranform pdf format to txt.
Created on Sun Oct 14 10:11:07 2018
"""
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

import os
import nltk
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def start(request):
	template = 'start.html'
	context   = { }
	return render(request,template,context)


def success(request):
	template = 'success.html'
	context   = { }
	return render(request,template,context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
        	Myfile = request.FILES['file']
        	fs = FileSystemStorage()
        	filename = fs.save(Myfile.name, Myfile)
        	uploaded_file_url = fs.url(filename)
        	#print uploaded_file_url 

        	fp = open(filename, "r")
        	fto = open(filename, "a+")

        	parser = PDFParser(fp)
        	doc = PDFDocument(parser)
        	parser.set_document(doc)
        	resource = PDFResourceManager()
        	laparam = LAParams()

        	device = PDFPageAggregator(resource, laparams=laparam)
        	interpreter = PDFPageInterpreter(resource, device)

        	for page in PDFPage.create_pages(doc):
        		interpreter.process_page(page)
        		layout = device.get_result()

        		for out in layout:
        			if hasattr(out, "get_text"):
        				print (out.get_text())
        				fto.write(out.get_text().encode('utf8'))

        	fp.close()
        	fto.close()



        	item_num = 50
        	f = open(filename)
        	text= f.read()
        	tokens = [t for t in text.split()]
        	clean_tokens = tokens[:]

        	for token in tokens:
        		if token in stopwords.words('english'):
        			clean_tokens.remove(token)
        	freq = nltk.FreqDist(clean_tokens)
        	# List the item_num most common elements and their counts
        	top = freq.most_common(item_num)
        	keys = [top[i][0] for i in range(len(top))]
        	count = [top[i][1] for i in range(len(top))]
        	print freq
        	f.close()


        	return HttpResponseRedirect('/success')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})












