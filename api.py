# Import the necessary libraries.
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# Create a Flask app.
app = Flask(__name__)

# Allow cross-origin requests.
CORS(app)

# Define the `summarize_video()` function.


@app.route('/summarize', methods=['POST'])
def summarize_video():

    # Get the video URL from the request body.
    youtube_video = request.json.get('video_url')

    # Get the video ID from the video URL.
    video_id = youtube_video.split("=")[1]

    # Get the transcript for the video.
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Combine all of the transcript sentences into a single string.
    result = ""
    for i in transcript:
        result += i['text']

    # Create a summarization pipeline.
    summarizer = pipeline("summarization")

    # Summarize the transcript and limit the output to 300 tokens.
    num_iters = int(len(result) / 1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)

    # Return the summary as a JSON object.
    return jsonify({'summary': summarized_text})


# Run the app.
if __name__ == '__main__':
    app.run(debug=True)
