from Content import Content
from services import UserInput, TextProcessing, ImageProcessing, VideoProcessing

print("Starting orchestrator")

DEFAULT_CONTENT_PATH = "content.pickle"
content = Content()
content = content.load(DEFAULT_CONTENT_PATH)

# Read user input
# content.search_term, content.prefix = UserInput.get_topic_and_prefix_from_input()
# content.save(DEFAULT_CONTENT_PATH)

# Fetch content from source
# content.source_content, content.source_content_sanitized = TextProcessing.\
#     fetch_content_and_sanitize(content.prefix, content.search_term)
# content.sentences = TextProcessing.fetch_keywords_from_content(content.source_content_sanitized)
# content.save(DEFAULT_CONTENT_PATH)

# Fetch images for content
# content.sentences, content.downloaded_images = ImageProcessing.\
#     fetch_images_and_download_for_sentences(content.sentences, content.search_term, content.downloaded_images)
# content.save(DEFAULT_CONTENT_PATH)

# Render video
VideoProcessing.generate_slide_images_for_all_sentences(content.sentences)
print(content.to_json())
