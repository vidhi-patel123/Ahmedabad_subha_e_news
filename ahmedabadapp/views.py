from django.shortcuts import render,redirect
from .models import*
# ----------------REST-------------------
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import*
# -----------------------------------------
from django.contrib import messages
from datetime import datetime
# -------YOUTUBE VIDEO--------------------
from googleapiclient.discovery import build
from django.http import HttpResponse
import requests
from collections import defaultdict


# Create your views here.

def home(request):
    return render(request, 'home.html')

def ahmedabad_subah(request):
    return render(request,'ahmedabad-subah.html')

def birch_academia(request):
    return render(request,'birch-academia.html')

def ignite_digital(request):
    return render(request,'ignite-digital.html')

def trending_around(request):
    return render(request,'trending-around.html')

class ContactView(APIView):

    def get(self,request,id=None):
        if id:
            try:
                uid = Contact.objects.get(id=id)
                serializer = ContactSerializer(uid)

                return Response({'status':'success','data':'serializer.data'})
            except:
                return Response({'status':'Invalid..'})
        else:
            uid = Contact.objects.all()
            serializer = ContactSerializer(uid,many=True)

            return Response({'status':'success','data': serializer.data})

    def post(self,request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','data': serializer.data})
        else:
            return Response({'status':'Invalid data..'})

    def patch(self, request,id=None):
        try:
            uid = Contact.objects.get(id=id)
        except:
            return Response({'status':'success','data': serializer.data})

        serializer = ContactSerializer(uid,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({'status':'success','data': serializer.data})
        else:
            return Response({'status':'Invalid data..'})
        
    def delete(self,request,id=None):
        if id:
            try:
                uid = Contact.objects.get(id=id).delete()

                return Response({'status':'success'})
            except:
                return Response({'status':'Invalid..'})
        else:
            return Response({'status':'Invalid..'})

def home(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        uid = Contact.objects.create(name=name,
                                      email=email,
                                      subject=subject,
                                      message=message)
        con={
            'quid': "Data addeded Successfully..We will get back to you shortly..!!"
        }
        return render(request,'home.html',con)
    else:
        return render(request,'home.html')
    
# def magazine(request):
#     if request.POST:
#         email = request.POST['email']

#         uid = magazine.objects.create(email=email)

#         return render(request,'index.html')
#     else:
#         return render(request,'index.html')

def privacy_policy(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    return render(request, 'privacy_policy.html')

def terms_and_condition(request):
    return render(request, 'terms_and_condition.html')    

# ---------------------------E-NEWS CODE------------------------------
def newspaper(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        pdf_file = request.FILES.get('pdf_file')
        video_file = request.FILES.get('video_file')

        if date and (pdf_file or video_file):  # at least one file required
            Newspaper.objects.create(
                date=date,
                pdf_file=pdf_file if pdf_file else None,
                video_file=video_file if video_file else None
            )
            messages.success(request,"PDF uploaded successfully..!!")
            return redirect('newspaper')

        else:
            return render(request, 'newspaper.html', {'error': 'Please select at least one file.'})

    return render(request, 'newspaper.html')

# ------------ FOR NEW VIDEOS IN YOUTUBE OR ANY UPDATE THEN WRITE IT --------------
    # python manage.py shell
    # from ahmedabadapp.views import fetch_youtube_videos
    # fetch_youtube_videos()
    # exit()
            #  --------for check videos are store in DB or not-------
            # from ahmedabadapp.models import YoutubeVideo
            # print(YoutubeVideo.objects.all())

import calendar

def uploaded(request):
    selected_date_str = request.GET.get('date')
    pdf_grouped = []

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            pdfs = Newspaper.objects.filter(date=selected_date).order_by('-date')
            videos = YoutubeVideo.objects.filter(published_at=selected_date).order_by('-published_at')

            label = selected_date.strftime("%B %Y")
            pdf_grouped.append({
                'label': label,
                'items': pdfs,
                'videos': videos
            })

        except ValueError:
            # If date is not in correct format, fallback to show all
            pdfs = Newspaper.objects.all().order_by('-date')
            videos = YoutubeVideo.objects.all().order_by('-published_at')
    else:
        pdfs = Newspaper.objects.all().order_by('-date')
        videos = YoutubeVideo.objects.all().order_by('-published_at')

        # Group PDFs
        pdf_dict = defaultdict(list)
        for pdf in pdfs:
            label = pdf.date.strftime("%B %Y")
            pdf_dict[label].append(pdf)

        # Group videos
        video_dict = defaultdict(list)
        for video in videos:
            label = video.published_at.strftime("%B %Y")
            video_dict[label].append(video)

        # Combine
        for label in pdf_dict:
            pdf_grouped.append({
                'label': label,
                'items': pdf_dict[label],
                'videos': video_dict.get(label, [])
            })

    context = {
        'pdf_grouped': pdf_grouped,
        'selected_date': selected_date_str,
    }
    return render(request, 'uploaded.html', context)

def latest_youtube_videos(request):
    videos = YoutubeVideo.objects.order_by('-published_at')[:15]
    youtube_videos = YoutubeVideo.objects.order_by('-published_at')[:15]

    return render(request, 'videos.html', {'videos': videos, 'youtube_videos': youtube_videos})

API_KEY = 'AIzaSyAaCfEr7XP4JtTj1o8F2t0i01CndhElPCo'
CHANNEL_ID = 'UCDXESO6B2iddz4w0gxGWkIQ'

def fetch_youtube_videos():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': API_KEY,
        'channelId': CHANNEL_ID,
        'part': 'snippet',
        'order': 'date',
        'maxResults': 15,
        'type': 'video',
    }

    response = requests.get(url, params=params)
    data = response.json()

    fetched_video_ids = []

    for item in data.get("items", []):
        video_id = item['id']['videoId']
        snippet = item['snippet']
        title = snippet['title']
        published_at_str = snippet['publishedAt']  # e.g. "2025-05-23T07:30:00Z"

        try:
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue  # skip bad date

        # Save new or update existing
        YoutubeVideo.objects.update_or_create(
            video_id=video_id,
            defaults={
                'video_title': title,
                'published_at': published_at,
            }
        )
        fetched_video_ids.append(video_id)  #if delete video in youtube
        YoutubeVideo.objects.exclude(video_id__in=fetched_video_ids).delete()
