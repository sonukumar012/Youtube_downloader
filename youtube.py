from flask import Flask, render_template, request, redirect, url_for, session
from pytube import YouTube

app = Flask(__name__)
app.secret_key = b'\x1eb?\x0cO\xaa\x19\xa5\xc3\x1c\xc0\x04\x16V`\x0c\x98\x08\x17\xbc\xec\xec\xe7('  # Set your secret key for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        resolution = request.form.get('resolution', 'highest')  # Default to 'highest' if resolution is not provided
        try:
            yt = YouTube(youtube_link)
            if resolution == 'highest':
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
            stream.download()
            session['message'] = 'Download complete!'
            return redirect(url_for('index'))  # Redirect to index route to render the index template again
        except Exception as e:
            session['message'] = str(e)
            return redirect(url_for('index'))  # Redirect to index route to render the index template again

if __name__ == '__main__':
    app.run(debug=True)