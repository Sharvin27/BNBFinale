from django.shortcuts import render,HttpResponse,redirect
from .models import Category
from .forms import ProductForm

def index(request):
    # send_expiration_via_sms()
    return render(request, 'base.html')


def add_inventory(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(display_inventory)
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'inventory/add_inventory.html', {'form': form, 'categories': categories})


def display_inventory(request):
    # Retrieve all categories along with their associated products
    categories = Category.objects.prefetch_related('product_set')

    # Render the template with the categories and associated products
    return render(request, 'inventory/inventory.html', {'categories': categories})

from twilio.rest import Client



    
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Product

def generate_pdf(request):
    # Get all products from the database
    products = Product.objects.all()

    # Create a response object with PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_report.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Product details as a list of lists
    product_data = [
        ["Product Name", "Price", "Quantity Total", "Date Bought", "Date Expiration", "Category", "Quantity Remaining"]
    ]

    for product in products:
        product_data.append([
            product.name,
            f"${product.price}",
            str(product.quantity_total),
            str(product.date_bought),
            str(product.date_expiration),
            product.category.name,
            str(product.quantity_remaining),
        ])

    # Create a table and add styles
    table = Table(product_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the document
    elements.append(table)
    doc.build(elements)

    return response

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import urllib.parse

load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    print(text)
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    index_path = os.path.join(settings.BASE_DIR, "faiss_index")
    vector_store.save_local(index_path)
    return index_path

def get_conversational_chain():
    prompt_template = """
    You are analyzing the data in the inventory given and answering all user questions. The context contains a table with the following
    product names, image, price, quantity_total, date_bought,date_expiration,category,quantity_remaining, Answer on the basis of this.

{context} (Provide the PDF containing the data for analysis)

Question:
{question}

Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local(os.path.join(settings.BASE_DIR, "faiss_index"), embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    response_text = response["output_text"]
    if response_text == "":
        response_text = "It seems that the answer is out of context. Here is a general response: ..."
    return response_text

def gemini(request):
    if request.method == 'POST':
        # Handle PDF upload
        pdf_docs = request.FILES.getlist('pdf_files')
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        pdf_path = get_vector_store(text_chunks)  # Save the PDF path

        # Store the PDF path in the user's session
        request.session['pdf_path'] = pdf_path

        # Handle user question
        user_question = request.POST.get('user_question')
        response_text = user_input(user_question)


        # Return response
        return render(request, 'pages/gemini.html', {'response_text': response_text})
    else:
        return render(request, 'pages/gemini.html')