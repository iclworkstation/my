from flask import Flask, render_template, request, redirect, send_file
import yt_dlp
import os
import io

app = Flask(__name__)

# ගොනු ඩවුන්ලෝඩ් කිරීමට තාවකාලික ෆෝල්ඩරයක්
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if not video_url:
            return render_template('index.html', error="කරුණාකර URL එකක් ඇතුළත් කරන්න.")

        try:
            # yt-dlp Options
            ydl_opts = {
                'format': 'best',  # හොඳම ගුණාත්මක භාවය තෝරන්න
                'noplaylist': True,
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False) # තොරතුරු පමණක් ලබා ගන්න
                
                # වීඩියෝව ඩවුන්ලෝඩ් කරන්න
                ydl.download([video_url]) 
                
                # ඩවුන්ලෝඩ් වූ ගොනුවේ නම සොයා ගන්න
                file_path = ydl.prepare_filename(info)
                
                # පරිශීලකයාට ගොනුව යවන්න
                return send_file(file_path, as_attachment=True)

        except Exception as e:
            # දෝෂයක් ඇති වුවහොත් පෙන්වන්න
            return render_template('index.html', error=f"ඩවුන්ලෝඩ් කිරීමේ දෝෂයක්: {e}")
            
    return render_template('index.html', error=None)

# ඩවුන්ලෝඩ් කිරීම අවසන් වූ පසු තාවකාලික ගොනුව මකා දැමීම (Clean up)
@app.teardown_request
def cleanup(exception=None):
    # මෙය නිදර්ශනයක් පමණි. Production එකකදී වඩා හොඳ cleanup logic එකක් අවශ්‍ය වේ.
    # උදාහරණයක් ලෙස, සර්වර් එක නැවත පණගැන්වීමේදී downloads ෆෝල්ඩරය හිස් කිරීම.
    pass

if __name__ == '__main__':
    app.run(debug=True)