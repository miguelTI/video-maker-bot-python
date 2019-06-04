from Content import Content
from services import UserInput, TextProcessing, ImageProcessing, VideoProcessing, Youtube

print("Starting orchestrator")

DEFAULT_CONTENT_PATH = "content.pickle"
DEFAULT_VIDEO_PATH = "test.mp4"
DEFAULT_AUDIO_PATH = "audio.mp3"
content = Content()
content = content.load(DEFAULT_CONTENT_PATH)

content.search_term, content.prefix = UserInput.get_topic_and_prefix_from_input()
content.save(DEFAULT_CONTENT_PATH)

content.source_content, content.source_content_sanitized = TextProcessing.\
    fetch_content_and_sanitize(content.prefix, content.search_term)
content.sentences = TextProcessing.fetch_keywords_from_content(content.source_content_sanitized)
content.save(DEFAULT_CONTENT_PATH)

content.sentences, content.downloaded_images = ImageProcessing.\
    fetch_images_and_download_for_sentences(content.sentences, content.search_term, content.downloaded_images)
content.save(DEFAULT_CONTENT_PATH)

VideoProcessing.generate_slide_images_for_all_sentences(content.sentences)
VideoProcessing.render_video(content.sentences, DEFAULT_VIDEO_PATH, DEFAULT_AUDIO_PATH)

Youtube.upload_video(DEFAULT_VIDEO_PATH, content)

print ("Start sharing your video :)")
# print(content.to_json())