import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from .models import VideoGroup, VideoStream

def home(request):
    if request.method == 'POST':
        group_name = request.POST['name']
        VideoGroup.objects.create(name=group_name)
    groups = VideoGroup.objects.all()
    return render(request, 'video_app/home.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(VideoGroup, pk=pk)
    if request.method == 'POST':
        rtsp_url = request.POST.get('rtsp_url')
        if rtsp_url:
            VideoStream.objects.create(group=group, rtsp_url=rtsp_url)
            output_dir = os.path.join('video_app', 'static', 'streams', str(group.id))
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, 'index.m3u8')
            command = [
                'ffmpeg',
                '-i', rtsp_url,
                '-codec:v', 'libx264',
                '-codec:a', 'aac',
                '-f', 'hls',
                '-hls_time', '4',
                '-hls_playlist_type', 'event',
                output_file
            ]
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    print(f'FFmpeg error: {stderr.decode()}')
            except Exception as e:
                print(f'Error starting ffmpeg: {e}')
            return redirect('group_detail', pk=group.pk)
    return render(request, 'video_app/group_detail.html', {'group': group})

def delete_stream(request, pk):
    stream = get_object_or_404(VideoStream, pk=pk)
    group_pk = stream.group.pk
    stream.delete()
    return redirect('group_detail', pk=group_pk)
