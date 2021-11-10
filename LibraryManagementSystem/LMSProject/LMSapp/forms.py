from django import forms
from .models import Book,BookHistory,MyUser


class BookCreateForm(forms.ModelForm):
   class Meta:
     model = Book
     fields = ['category','book_name', 'quantity']

   def clean_category(self) :
      category = self.cleaned_data.get('category')
      if not category :
         raise forms.ValidationError('This field is required')
      return category


   def clean_book_name(self) :
      book_name = self.cleaned_data.get('book_name')
      if not book_name :
         raise forms.ValidationError('This field is required')
      for instance in Book.objects.all() :
          if instance.book_name == book_name :
              raise forms.ValidationError(str(book_name) + ' is already created')
      return book_name



class BookHistorySearchForm(forms.ModelForm) :
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta :
        model = BookHistory
        fields = ['category','book_name', 'start_date', 'end_date']
class BookSearchForm(forms.ModelForm) :
    export_to_CSV = forms.BooleanField(required=False)
    class Meta :
         model = Book
         fields = ['category', 'book_name']

class BookUpdateForm(forms.ModelForm) :
    class Meta :
         model = Book
         fields = ['category', 'book_name', 'quantity']

class IssueForm(forms.ModelForm) :
     class Meta :
          model = Book
          fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm) :
     class Meta :
          model = Book
          fields = ['receive_quantity']

class ReorderLevelForm(forms.ModelForm) :
     class Meta :
           model = Book
           fields = ['reorder_level']

