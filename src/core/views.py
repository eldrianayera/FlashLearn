from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .models import Course , User , Document , Flashcard
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
import fitz
from openai import OpenAI
from .forms import SignUpForm
from django.contrib.auth import login

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

class LandingPageView(TemplateView):
    template_name = "core/landing_page_view.html"
    

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("courses")
    
    # If user is already authenticated, keep them out of signup
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    
    # Auto-login after successful signup
    def form_valid(self, form):
        response =  super().form_valid(form)
        login(self.request, self.object)
        return response
    

class CourseCreateView(LoginRequiredMixin,CreateView):
    model = Course
    template_name = "core/course_create.html"
    fields = ["name","course_note"]
    success_url = reverse_lazy('courses')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

    

class CourseUpdateView(UpdateView):
    model = Course
    template_name = "core/course_update.html"
    fields = ["name", "course_note"] 
    
    def get_success_url(self):
        return reverse_lazy('course-detail' , args=[self.object.slug])

class CourseDeleteView(DeleteView):
    model = Course
    template_name = "core/course_delete.html"
    context_object_name = "course"
    
    def get_success_url(self):
        return reverse_lazy('courses')




    
class CourseListView(LoginRequiredMixin , ListView):
    model = Course
    template_name = "core/courses.html"
    context_object_name = "courses"
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    template_name = "core/course_detail_view.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    

class DocumentCreateView(LoginRequiredMixin,CreateView):
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
    

class DocumentDetailView(LoginRequiredMixin,DetailView):
    model = Document
    template_name = "core/document_detail_view.html"
    context_object_name = "document"

    

class DocumentUpdateView(LoginRequiredMixin,UpdateView):
    model = Document
    template_name = "core/document_form.html"
    fields = ['name','file','document_note','summary']
    
    def get_success_url(self):
        return reverse("course-detail", args=[self.object.course.slug])
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['course'] = self.object.course
        return ctx
    

class DocumentDeleteView(LoginRequiredMixin,DeleteView):
    model = Document
    template_name = "core/document_delete.html"
    context_object_name = "document"

    def get_success_url(self):
        return reverse('course-detail',args=[self.object.course.slug])
    

class FlashcardCreateView(LoginRequiredMixin,CreateView):
    model = Flashcard
    template_name = "core/flashcard_form.html"
    fields = ["question","answer"]

    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['document_pk'] = self.document.pk
        return ctx


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.document = self.document
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('document-detail', args=[self.object.document.pk])


class FlashcardUpdateView(LoginRequiredMixin,UpdateView):
    model = Flashcard
    template_name = "core/flashcard_form.html"
    fields = ['question','answer']
    
    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['document_pk'] = self.object.document.pk
        ctx['update'] = True
        return ctx
    
    def get_success_url(self):
        return reverse_lazy('document-detail', args=[self.object.document.pk])


class FlashcardDeleteView(LoginRequiredMixin,DeleteView):
    model = Flashcard
    template_name = "core/flashcard_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('document-detail', args=[self.object.document.pk])
