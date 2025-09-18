from ast import Delete
from cmd import PROMPT
from time import process_time_ns
from urllib import response
from django import dispatch
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Course , User , Document , Flashcard
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
import fitz
import requests
import json
from openai import OpenAI

def extract_pdf_text(file):
    doc = fitz.open(file.path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text 


def summarize_text_with_openrouter(text):
    prompt = f"Please summarize the following text. Only return the summary—do not include any additional text or commentary. The summary should capture the key points, main ideas, and any important details in a concise manner: {text}"


    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    
    completion = client.chat.completions.create(
    extra_headers={},
    extra_body={},
    model="openai/gpt-oss-20b:free",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
    )
    summary = completion.choices[0].message.content 
    return summary




# Create your views here.
    
class CourseListView(LoginRequiredMixin , UserPassesTestMixin, ListView):
    model = Course
    template_name = "core/courses.html"
    context_object_name = "courses"
    
    def test_func(self):
        return True
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    template_name = "core/course_detail_view.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    

class DocumentCreateView(CreateView):
    model = Document
    template_name = "core/document_form.html"
    fields = ['name','file','document_note']
    
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course = self.course
        
        response = super().form_valid(form)
    
        pdf_text = extract_pdf_text(form.instance.file)
        summary = summarize_text_with_openrouter(pdf_text)
        
        form.instance.summary = summary
        form.instance.save(update_fields=['summary'])
        
        return response


    def get_success_url(self):
        return reverse("course-detail", args=[self.course.slug])
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['course'] = self.course
        return context
    

class DocumentUpdateView(UpdateView):
    model = Document
    template_name = "core/document_form.html"
    fields = ['name','file','document_note','summary']
    
    def get_success_url(self):
        return reverse("course-detail", args=[self.object.course.slug])
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['course'] = self.object.course
        return ctx
    

class DocumentDeleteView(DeleteView):
    model = Document
    template_name = "core/document_delete.html"
    context_object_name = "document"

    def get_success_url(self):
        return reverse('course-detail',args=[self.object.course.slug])
    
