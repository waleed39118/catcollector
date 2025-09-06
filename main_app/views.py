from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'image']
  # success_url = '/cats/'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  
class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']
  
class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'
# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def cats_index(request):
  # SELECT * FROM 'main_app_cat';
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # Get the toys, cat dosent have
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', 
                {'cat': cat, 
                'feeding_form': feeding_form,
                'toys': toys_cat_doesnt_have
                })

@login_required  
def add_feeding(request, cat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id)


class ToyList(LoginRequiredMixin, ListView):
  model = Toy
  
class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
  
  
class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'
  
  
class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']
  
  
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required   
def assoc_toy(request, cat_id, toy_id):
  #Add this toy_id with the cat selected
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

#Remove the toy_ from the cat selected
@login_required  
def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

def signup(request):
  error_message=''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid signup - Please try again later'
    
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)