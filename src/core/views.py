from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .models import Course , User , Document , Flashcard
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
import fitz
from openai import OpenAI
from .forms import SignUpForm
from django.contrib.auth import login
from django.conf import settings
from django.views import View
from django.contrib.auth.views import LoginView
import logging
import re
import json


logger = logging.getLogger(__name__)

def extract_pdf_text(file):
    doc = fitz.open(file.path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text 

def openrouter_caller(prompt):
    try:
        client = OpenAI(
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENAI_API_KEY_2,
        )

        completion = client.chat.completions.create(
            model=settings.OPENAI_MODEL_2,
            messages=[{"role": "user", "content": prompt}],
        )
        
        print('!!!!!!!!!!!!!!!!!!!!!!!!!',completion.choices[0].message.content.strip())        
        return completion.choices[0].message.content.strip()

    except Exception as e:
        # Print the error for debugging
        print(f"Error in openrouter_caller: {e}")
        # Or you can return the error as a string
        return f"Error: {str(e)}"





# Create your views here.

class LandingPageView(TemplateView):
    template_name = "core/landing_page_view.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect(reverse_lazy('courses'))
        return super().dispatch(request, *args, **kwargs)
    
class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("courses")
    
    # If user is already authenticated, keep them out of signup
    def dispatch(self, request, *args, **kwargs):
        print('signup pageee')
        if request.user.is_authenticated :
            return redirect('courses')
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
        
        prompt = (
            "Please summarize the following text. Only return the summary—do not include any additional "
            "text or commentary. The summary should capture the key points, main ideas, and any important "
            f"details in a concise manner:\n\n{pdf_text}"
        )
    
        summary = openrouter_caller(prompt)
        
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
        ctx['document'] = self.document
        return ctx
    
    def get_initial(self):
        initial = super().get_initial()
        key = f"flashcard_prefill_{self.document.pk}"
        prefill = self.request.session.pop(key, None)
        if prefill :
            print('tahap 3' , prefill)
            initial.update(prefill)
        return initial



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
        ctx['document'] = self.object.document
        ctx['update'] = True
        return ctx
    
    def get_success_url(self):
        return reverse_lazy('document-detail', args=[self.object.document.pk])


class FlashcardDeleteView(LoginRequiredMixin,DeleteView):
    model = Flashcard
    template_name = "core/flashcard_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('document-detail', args=[self.object.document.pk])
    
    

class FlashcardGenerate(View):

    def post(self, request, *args, **kwargs) :
        document = get_object_or_404(Document, pk=kwargs['pk'])
        topic = request.POST.get('topic')
        is_limited = True if request.POST.get('isDocumentLimited') else False
        
        text = extract_pdf_text(document.file)
            
        prompt = f"""
            WARNING: Please respond with a dictionary format. The dictionary should contain exactly two keys: 'question' and 'answer'. Only a dictionary should be returned, nothing else.

            Context: {text}

            Topic: {topic}

            {'Please limit the question only to the provided context.' if is_limited else 'Please generate a broader question not limited to the provided context.'}
            
            Generate a question related to the topic and the provided context. The question should be relevant to the context and topic.
            """
        
        response = openrouter_caller(prompt)
        print('tahap 2' , response)
        
        match = re.search(r'(\{.*\})', response.strip(), re.DOTALL)
        print(match)
        
        flashcard = json.loads(match.group(1)) if match else {'question':'What is the name of the document ?' , f'answer':'The name of the document is {document.name}'}  
        
        key = f"flashcard_prefill_{document.pk}"
        request.session[key] = flashcard
        request.session.modified = True
        
        return redirect(reverse('flashcard-create', args=[document.pk]))
    
    def get(self,request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs['pk'])
        context = {
            "document": document
        }
        return render(request, "core/flashcard_generate.html",context)
    
    

