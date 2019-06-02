from googleapiclient.discovery import build
import config
import wget


def fetch_images_links(query):
    service = build("customsearch", "v1", developerKey=config.GOOGLE_CLOUD_CONFIG["api_key"])

    response = service.cse().list(
        q=query,
        cx=config.GOOGLE_CLOUD_CONFIG["cse_id"],
        searchType="image",
        num=2
        ).execute()
    links = []
    for item in response['items']:
        links.append(item['link'])
    return links


def fetch_images_and_download_for_sentences(sentences, search_term, downloaded_images):
    for key, sentence in enumerate(sentences, start=0):
        sentence.images = fetch_images_links(generate_search_term(search_term, sentence, key))
        downloaded_images.append(download_single_image_for_sentence(sentence, key, downloaded_images))
    return sentences, downloaded_images


def generate_search_term(search_term, sentence, key):
    if key == 0:
        return sentence.keywords[0]
    return "{} {}".format(search_term, sentence.keywords[0])


def download_image(image_url, destination):
    try:
        wget.download(image_url, destination)
        return True
    except:
        print("An exception occurred")


def download_single_image_for_sentence(sentence, sentence_key, downloaded_images):
    for image_url in sentence.images:
        if image_url not in downloaded_images and download_image(image_url, "{}-original.png".format(sentence_key)):
            return image_url
