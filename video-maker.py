from Content import Content
from services import UserInput

print("Starting orchestrator")

content = Content()

# Read user input
content = UserInput.read_input_and_update_content(content)
print(content.to_json())
# Fetch content from source

# Process content text

# Fetch images for content

# Render video
