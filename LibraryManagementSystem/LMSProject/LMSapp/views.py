from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required



def home(request):
    title = 'Welcome: This is the Home Page'
    form='Welcome: This is the Home Page'
    context = {
      "title": title,
       "test": form,
    }
    #return render(request, "home.html",context)
    return redirect('/list_books')
@login_required
def list_books(request):
    form = BookSearchForm(request.POST or None)
    title = 'List of Books'
    queryset = Book.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form" : form
    }
    if request.method == 'POST' :
        category = form['category'].value()
        queryset = Book.objects.filter(
            book_name__icontains=form['book_name'].value()
        )

        if (category != '') :
            queryset = queryset.filter(category_id=category)
    if request.method == 'POST' :

      if form['export_to_CSV'].value() == True :
          response = HttpResponse(content_type='text/csv')
          response['Content-Disposition'] = 'attachment; filename="List of book.csv"'
          writer = csv.writer(response)
          writer.writerow(['CATEGORY', 'BOOK NAME', 'QUANTITY'])
          instance = queryset
          for stock in instance :
              writer.writerow([stock.category, stock.book_name, stock.quantity])
          return response

      context = {
               "form" : form,
               "title" : title,
               "queryset" : queryset,
            }

    return render(request, "list_books.html", context)
@login_required
def add_books(request):
    form = BookCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_books')
    context = {
        "form": form,
        "title": "Add Book",
    }
    return render(request, "add_books.html", context)



def update_books(request, pk):
    queryset = Book.objects.get(id=pk)
    form = BookUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = BookUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('/list_books')

    context = {
        'form':form
    }
    return render(request, 'add_books.html', context)
def delete_books(request, pk):
    queryset = Book.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_books')
    context = {

    }
    return render(request, 'delete_books.html',context)

def book_detail(request, pk):
    queryset = Book.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "book_detail.html", context)
def issue_books(request, pk):
    queryset = Book.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity=0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.book_name) + "s now left in Store")
        instance.save()

        return redirect('/book_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.book_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_books.html", context)



def receive_books(request, pk):
    queryset = Book.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity=0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.book_name)+"s now in Store")

        return redirect('/book_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "title": 'Reaceive ' + str(queryset.book_name),
            "instance": queryset,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "add_books.html", context)
def reorder_level(request, pk):
    queryset = Book.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.book_name) + " is updated to " + str(instance.reorder_level))

        return redirect("/list_books")
    context = {
            "instance": queryset,
            "form": form,
        }
    return render(request, "add_books.html", context)
@login_required
def book_history(request):
    form = BookHistorySearchForm(request.POST or None)
    title = 'HISTORY DATA'
    queryset = BookHistory.objects.all()

    context = {
        "title": title,
        "queryset": queryset,
        "form" : form,
    }
    return render(request, "book_history.html",context)

