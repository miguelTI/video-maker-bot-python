from PIL import Image, ImageFilter, ImageFont, ImageDraw
import textwrap

DEFAULT_FONT_TYPE = "Arial Bold.ttf"
DEFAULT_FONT_SIZE = 48
DEFAULT_TEXT_WIDTH = 75
DEFAULT_SHADOW_OFFSET = 2
ORIGINAL_IMAGE_SUFFIX = "-original.png"
CONVERTED_IMAGE_SUFFIX = "-converted.png"
SENTENCE_IMAGE_TAG = "-sentence"
DEFAULT_IMAGE_WIDTH = 1920
DEFAULT_IMAGE_HEIGHT = 1080
DEFAULT_IMAGE_MODE = "RGBA"
TEXT_POSITION = [(100, 50), (100, DEFAULT_IMAGE_HEIGHT - 350)]
WHITE_RGB = (255, 255, 255)
TRANSPARENT_RGBA = (0, 0, 0, 0)
BLACK_RGB = (0, 0, 0)


def generate_slide_images_for_all_sentences(sentences):
    for key, sentence in enumerate(sentences):
        generate_slide_images_for_sentence(key, sentence)


def generate_slide_images_for_sentence(sentence_key, sentence):
    original_image = Image.open("{}{}".format(sentence_key, ORIGINAL_IMAGE_SUFFIX)).convert(DEFAULT_IMAGE_MODE)
    output_path = "{}{}".format(sentence_key, CONVERTED_IMAGE_SUFFIX)
    resize_image(original_image, sentence_key, output_path)
    merge_images(original_image, output_path)
    create_sentence_image(sentence_key, sentence.text, "{}{}{}".format(sentence_key, SENTENCE_IMAGE_TAG,
                                                                       CONVERTED_IMAGE_SUFFIX))


def resize_image(image, sentence_key, output_path):
    try:
        resized_image = image.resize((DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT))
        resized_image.filter(ImageFilter.GaussianBlur(30)).save(output_path)
    except:
        print("Error resizing image {}".format(sentence_key))


def merge_images(original_image, converted_image):
    try:
        image_width, image_height = original_image.size
        background_image = Image.open(converted_image).convert(DEFAULT_IMAGE_MODE)
        background_image_width, background_image_height = background_image.size

        offset = ((background_image_width - image_width) // 2, (background_image_height - image_height) // 2)

        background_image.paste(original_image, offset, original_image)
        background_image.save(converted_image)
    except:
        print("Error merging image {}".format(converted_image))


def get_text_position_by_sentence_key(sentence_key):
        return TEXT_POSITION[0] if sentence_key % 2 == 0 else TEXT_POSITION[1]


def create_sentence_image(sentence_key, sentence_text, output_image_path):
    try:
        new_image = Image.new(DEFAULT_IMAGE_MODE, (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT), TRANSPARENT_RGBA)
        text_lines = textwrap.wrap(sentence_text, width=DEFAULT_TEXT_WIDTH)
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype(DEFAULT_FONT_TYPE, DEFAULT_FONT_SIZE)
        text_position_x, text_position_y = get_text_position_by_sentence_key(sentence_key)

        for line in text_lines:
            font_width, font_height = font.getsize(line)
            draw.text((text_position_x + DEFAULT_SHADOW_OFFSET, text_position_y + DEFAULT_SHADOW_OFFSET), line,
                      BLACK_RGB,
                      font=font)
            draw.text((text_position_x - DEFAULT_SHADOW_OFFSET, text_position_y - DEFAULT_SHADOW_OFFSET), line,
                      BLACK_RGB,
                      font=font)
            draw.text((text_position_x + DEFAULT_SHADOW_OFFSET, text_position_y - DEFAULT_SHADOW_OFFSET), line,
                      BLACK_RGB,
                      font=font)
            draw.text((text_position_x - DEFAULT_SHADOW_OFFSET, text_position_y + DEFAULT_SHADOW_OFFSET), line,
                      BLACK_RGB,
                      font=font)
            draw.text((text_position_x, text_position_y), line, WHITE_RGB, font=font)
            text_position_y += font_height
        new_image.save(output_image_path)
    except:
        print("Couldn't add text to image {}_converted.png".format(sentence_key))
