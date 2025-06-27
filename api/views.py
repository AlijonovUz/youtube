import os
import uuid
import json

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from threading import Timer

DOWNLOADS_DIR = "./media/"

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)


def delete_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"Fayl o'chirildi: {file_path}")
    except Exception as e:
        print(f"Faylni o'chirishda xato: {e}")


def error_response(error_id: int, error_msg: str):
    return Response({
        "error": {
            "errorId": error_id,
            "errorMsg": error_msg
        },
        "success": False
    }, status=error_id)


class AudioDownloadView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return error_response(400, "URL parametri yo'q")

        file_id = str(uuid.uuid4())
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "outtmpl": os.path.join(DOWNLOADS_DIR, f"{file_id}.%(ext)s"),
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            return error_response(500, f"yt-dlp xatosi: {str(e)}")

        file_link = f"http://4532381-xa58658.twc1.net/YouTube/media/{file_id}.mp3"

        timer = Timer(60.0, delete_file, [os.path.join(DOWNLOADS_DIR, f"{file_id}.mp3")])
        timer.start()

        return Response({"url": file_link, "success": True}, status=status.HTTP_200_OK)


class VideoFormatsView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return error_response(400, "URL parametri yo'q")

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        formats = []

        def extract_formats(d):
            for f in d.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    formats.append({
                        "format_id": f["format_id"],
                        "ext": f["ext"],
                        "resolution": f.get("format_note") or f.get("height"),
                        "filesize": f.get("filesize"),
                    })

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                extract_formats(info)
        except Exception as e:
            return error_response(500, f"yt-dlp xatosi: {str(e)}")

        return Response({"formats": formats}, status=status.HTTP_200_OK)


class VideoDownloadView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        format_id = request.query_params.get('format_id')
        if not url or not format_id:
            return error_response(400, "URL yoki format_id parametrlari yo'q")

        file_id = str(uuid.uuid4())

        ydl_opts = {
            "format": format_id,
            "outtmpl": os.path.join(DOWNLOADS_DIR, f"{file_id}.%(ext)s"),
            "quiet": True,
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            return error_response(500, f"yt-dlp xatosi: {str(e)}")

        file_link = f"http://4532381-xa58658.twc1.net/YouTube/media/{file_id}.mp4"

        timer = Timer(60.0, delete_file, [os.path.join(DOWNLOADS_DIR, f"{file_id}.mp4")])
        timer.start()

        return Response({"url": file_link, "success": True}, status=status.HTTP_200_OK)


class SearchView(APIView):
    def get(self, request: Request):
        title = request.query_params.get('title')
        page = request.query_params.get('page', 1)
        per_page = 10

        if not title:
            return Response({
                'error': {
                    'errorId': status.HTTP_400_BAD_REQUEST,
                    'errorMsg': "title query parameter is required.",
                },
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            page = int(page)
            if page < 1:
                raise ValueError
        except ValueError:
            return Response({
                'error': {
                    'errorId': status.HTTP_400_BAD_REQUEST,
                    'errorMsg': "page must be a positive integer.",
                },
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)

        offset = (page - 1) * per_page

        raw_results = YoutubeSearch(title, max_results=offset + per_page).to_json()
        all_results = json.loads(raw_results).get('videos', [])

        paginated_results = all_results[offset:offset + per_page]

        if paginated_results:
            status_code = status.HTTP_200_OK
            response = {
                'videos': paginated_results,
                'results_on_page': len(paginated_results),
                'success': True,
            }
        else:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                'error': {
                    'errorId': status.HTTP_404_NOT_FOUND,
                    'errorMsg': "Not found.",
                },
                'success': False
            }

        return Response(response, status=status_code)
