from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)


@app.route('/summarize', methods=['POST'])
def summarize_video():
    youtube_video = request.json.get('video_url')
    video_id = youtube_video.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += i['text']
    summarizer = pipeline("summarization")
    num_iters = int(len(result) / 1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
    return jsonify({'summary': summarized_text})


if __name__ == '__main__':
    app.run(debug=True)
