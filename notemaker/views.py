from django.shortcuts import render
from django.contrib import messages
from django.core.files import File
from .forms import NoteForm
from .utils import (
    createDocument, downloadVideo, generateNotes,
    splitVideoFrames, imageToText, getAudio, 
    audioToText, convertDocxToPdf
)
from django.http import FileResponse
import os
from .models import NoteMakerModel
import concurrent.futures

def processAudio(title, id):
    audio = getAudio(title, id)
    audioText = audioToText(audio)
    return audioText

def processVideo(title, id):
    splitVideoFrames(title, f'/tmp/{id}_frames')
    text = imageToText(f'/tmp/{id}_frames')
    return text


def home(request):
    if request.method == 'POST':
        noteForm = NoteForm(request.POST)
        if noteForm.is_valid():
            link = noteForm.cleaned_data['youtubeLink']
            processing = noteForm.cleaned_data['processing']
            noteType = noteForm.cleaned_data['noteType']
            noteMakeModel = NoteMakerModel(
                youtubeLink=link, 
                processing=processing, 
                noteType=noteType
            )
            noteMakeModel.save()
            title = downloadVideo(link, noteMakeModel.id)
            if processing == 'video':
                splitVideoFrames(title, f'/tmp/{noteMakeModel.id}_frames')
                text = imageToText(f'/tmp/{noteMakeModel.id}_frames')
                
                result = generateNotes(text)
                if noteType == 'twocolumn':
                    createDocument(result, f'{noteMakeModel.id}_notes.docx', True)
                else:
                    createDocument(result, f'{noteMakeModel.id}_notes.docx')
                
                
                os.removedirs(f'/tmp/{noteMakeModel.id}_frames')
                os.remove(f"/tmp/{title}")

                messages.success(request, "Notes generated successfully")

                return FileResponse(open(f'/tmp/{noteMakeModel.id}_notes.docx', 'rb'))
            elif processing == 'audio':
                text = ''
                try:
                    audio = getAudio(title, noteMakeModel.id)
                    text = audioToText(audio)
                    
                    result = generateNotes(text)
                except Exception as e:
                    messages.error(request, e)
                    return render(request, 'home.html', {'form': noteForm})
                if noteType == 'twocolumn':
                    createDocument(result, f'{noteMakeModel.id}_notes.docx', True)
                else:
                    createDocument(result, f'{noteMakeModel.id}_notes.docx')
                
                
                
                os.remove(f"/tmp/{title}")
                os.remove(f"/tmp/{audio}")

                messages.success(request, "Notes generated successfully")

                return FileResponse(open(f'/tmp/{noteMakeModel.id}_notes.docx', 'rb'))
            elif processing == 'both':
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    videoText = executor.submit(processVideo, title, noteMakeModel.id)
                    audioText = executor.submit(processAudio, title, noteMakeModel.id)

                text = videoText.result()
                audioText = audioText.result()


                text += '\n' + audioText
                result = generateNotes(text)
                if noteType == 'twocolumn':
                    createDocument(result, f'{noteMakeModel.id}_notes.docx', True)
                else:
                    createDocument(result, f'{noteMakeModel.id}_notes.docx')
                

                os.remove(f"/tmp/{title}")
                os.removedirs(f'/tmp/{noteMakeModel.id}_frames')

                messages.success(request, "Notes generated successfully")

                return FileResponse(open(f'/tmp/{noteMakeModel.id}_notes.docx', 'rb'))
        else:
            return render(request, 'home.html', {'form': noteForm})
    noteForm = NoteForm()
    return render(request, 'home.html', {'form': noteForm})

