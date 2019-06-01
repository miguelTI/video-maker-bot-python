PREFIXES = [
    "Who is",
    "What is",
    "History of"
]

TOPIC_QUESTION = "Define a topic "
PREFIX_QUESTION = "Define a prefix"


def _generate_prefixes_option_string(prefixes):
    prefixes_string = ""
    for key, prefix_string in enumerate(prefixes, start=1):
        prefixes_string = "{} {} {} \n".format(prefixes_string, str(key), prefix_string)
    return prefixes_string


def get_topic_and_prefix_from_input():
    topic_input = input("{}\n".format(TOPIC_QUESTION))
    prefix_key_input = input("{}\n{}".format(PREFIX_QUESTION, _generate_prefixes_option_string(PREFIXES)))

    return [str(topic_input), PREFIXES[int(prefix_key_input) - 1]]
