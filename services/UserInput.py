prefixes = [
    "Who is",
    "What is",
    "History of"
]

topic_question = "Define a topic "
prefix_question = "Define a prefix"


def generate_prefixes_option_string(prefixes):
    prefixes_string = ""
    for key, prefix_string in enumerate(prefixes, start=1):
        prefixes_string = "{} {} {} \n".format(prefixes_string, str(key), prefix_string)
    return prefixes_string


def read_input_and_update_content(content):
    topic_input = input("{}\n".format(topic_question))
    content.searchTerm = str(topic_input)
    prefix_key_input = input("{}\n{}".format(prefix_question, generate_prefixes_option_string(prefixes)))
    content.prefix = prefixes[int(prefix_key_input) - 1]

    return content
