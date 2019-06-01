from Content import Content
from services import UserInput

print("Starting orchestrator")

content = Content()

# Read user input
content.search_term, content.prefix = UserInput.get_topic_and_prefix_from_input()
print(content.to_json())
# Fetch content from source

# Process content text

# Fetch images for content

# Render video
