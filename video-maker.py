from Content import Content
from services import UserInput, TextProcessing

print("Starting orchestrator")

content = Content()

# Read user input
content.search_term, content.prefix = UserInput.get_topic_and_prefix_from_input()

# Fetch content from source
content.source_content, content.source_content_sanitized = TextProcessing.\
    fetch_content_and_sanitize(content.prefix, content.search_term)
content.sentences = TextProcessing.fetch_keywords_from_content(content.source_content_sanitized)
print(content.to_json())

# Process content text

# Fetch images for content

# Render video
