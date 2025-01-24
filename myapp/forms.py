from django import forms

class AssignmentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    rollnumber = forms.CharField(label='Roll Number', max_length=100)
    assignment = forms.CharField(label='Assignment Number', max_length=100, initial='Assignment-')
    subject_name = forms.CharField(label='Subject Name', max_length=100)
    submission_date = forms.DateField(label='Submission Date', widget=forms.DateInput(attrs={'type': 'date'}))
    submission_to = forms.CharField(label='Submission To', max_length=100)
    image = forms.ImageField(label='Upload Collage Logo', required=False)
