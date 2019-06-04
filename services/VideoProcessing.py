from PIL import Image, ImageFilter, ImageFont, ImageDraw
import textwrap
from moviepy.editor import ImageClip, transfx, CompositeVideoClip, concatenate

DEFAULT_FONT_TYPE = "Arial Bold.ttf"
DEFAULT_FONT_SIZE = 48
DEFAULT_TEXT_WIDTH = 75
DEFAULT_SHADOW_OFFSET = 2
ORIGINAL_IMAGE_SUFFIX = "-original.png"
CONVERTED_IMAGE_SUFFIX = "-converted.png"
SENTENCE_IMAGE_TAG = "-sentence"
YOUTUBE_THUMBNAIL_PATH = "youtube_thumbnail.jpg"
DEFAULT_IMAGE_WIDTH = 1920
DEFAULT_IMAGE_HEIGHT = 1080
DEFAULT_IMAGE_MODE = "RGBA"
YOUTUBE_THUMBNAIL_MODE = "RGB"
TEXT_POSITION = [(100, 50), (100, DEFAULT_IMAGE_HEIGHT - 350)]
SLIDE_POSITION = ["top", "bottom"]
WHITE_RGB = (255, 255, 255)
TRANSPARENT_RGBA = (0, 0, 0, 0)
BLACK_RGB = (0, 0, 0)
DEFAULT_VIDEO_FPS = 24


def generate_slide_images_for_all_sentences(sentences):
    for key, sentence in enumerate(sentences):
        print("Generating slide {}...".format(key))
        generate_slide_images_for_sentence(key, sentence)
    create_youtube_thumbnail(0, YOUTUBE_THUMBNAIL_PATH)


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


def merge_images(original_image, output_path):
    image_width, image_height = original_image.size
    resize_width, resize_height = [int(image_width * (DEFAULT_IMAGE_HEIGHT / image_height)), DEFAULT_IMAGE_HEIGHT] if image_height > image_width else [DEFAULT_IMAGE_WIDTH, int(image_height * (DEFAULT_IMAGE_HEIGHT / image_width))]
    original_image = original_image.resize((resize_width, resize_height))
    background_image = Image.open(output_path).convert(DEFAULT_IMAGE_MODE)
    background_image_width, background_image_height = background_image.size

    offset = ((background_image_width - resize_width) // 2, (background_image_height - resize_height) // 2)

    background_image.paste(original_image, offset, original_image)
    background_image.save(output_path)


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


def create_youtube_thumbnail(sentence_key, output_path):
    original_image = Image.open("{}{}".format(sentence_key, CONVERTED_IMAGE_SUFFIX)).convert(YOUTUBE_THUMBNAIL_MODE)
    original_image.save(output_path)


def get_slide_position_by_sentence_key(sentence_key):
    return SLIDE_POSITION[0] if sentence_key % 2 == 0 else SLIDE_POSITION[1]


def render_video(sentences, output_path, audio_path):
    print("Rendering video...")
    image_slides = []
    for key, sentence in enumerate(sentences):
        image_slide = ImageClip("{}{}".format(key, CONVERTED_IMAGE_SUFFIX)).set_duration(10)
        text_slide = ImageClip("{}{}{}".format(key, SENTENCE_IMAGE_TAG, CONVERTED_IMAGE_SUFFIX)).set_duration(10)
        slided_slide = text_slide.fx(transfx.slide_in, 1, get_slide_position_by_sentence_key(key))
        slides_video = CompositeVideoClip([image_slide, slided_slide])
        image_slides.append(slides_video)

    final_video = concatenate(image_slides)
    final_video.write_videofile(output_path, audio=audio_path, fps=DEFAULT_VIDEO_FPS)
