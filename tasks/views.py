from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse

from reportlab.pdfgen import canvas
from reportlab.lib import colors
# Create your views here.

from .models import *
from .forms import *

# homepage AKA. task list


def index(request):
    # store all tasks in variable
    tasks = Task.objects.all()
    # store form in variable
    form = TaskForm()

    # Handling form submission
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

# edit task page


def editTask(request, pk):
    # store selected task in variable
    task = Task.objects.get(id=pk)
    # create form with existing data
    form = TaskForm(instance=task)

    # handling form submission
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form': form}
    return render(request, 'tasks/edit.html', context)


def deleteTask(request, pk):
    # store selected task in variable
    task = Task.objects.get(id=pk)

    # Delete task
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    context = {'task': task}
    return render(request, 'tasks/delete.html', context)


def downloadPDF(request):
    # set files names
    filename = 'ToDo.pdf'
    doctitle = 'My To Do List'
    title = 'To Do List'
    subtitle = "Today's Date"

    maintext = []
    tasks = Task.objects.all()
    for task in tasks:
        maintext.append(str(task.title))

    # create file
    pdf = canvas.Canvas(filename)
    pdf.setTitle(doctitle)

    # add Title to PDF
    pdf.setFont('Times-Bold', 36)
    pdf.drawCentredString(280, 750, title)

    # add subtitle to PDF
    pdf.setFillColorRGB(0, 0, 200)
    pdf.setFont('Times-Roman', 28)
    pdf.drawCentredString(280, 675, subtitle)

    # draw line
    pdf.line(50, 625, 550, 625)

    # add main text
    text = pdf.beginText(50, 600)
    text.setFont('Times-Roman', 22)
    text.setFillColor(colors.red)
    for line in maintext:
        text.textLine(line)
    pdf.drawText(text)

    pdf.showPage()
    pdf.save()

    return redirect('/')
