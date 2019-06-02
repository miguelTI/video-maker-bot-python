import Algorithmia
import re
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
import nltk
from Sentence import Sentence
import config

DEFAULT_LANG = "en"
MAXIMUM_SENTENCES_TO_EXTRACT = 7
MINIMUM_KEYWORD_RELEVANCE = 0.60
ALGORITHMIA_ALGO_VERSION = "web/WikipediaParser/0.1.2"


def fetch_content_and_sanitize(prefix, search_term):
    original_content = fetch_content_from_source("{} {}".format(prefix, search_term), DEFAULT_LANG)
    sanitized_content = clean_dates_in_parenthesis(clean_empty_and_markup_lines(original_content))
    return [original_content, sanitized_content]


def clean_empty_and_markup_lines(string):
    return " ".join([line for line in string.split("\n") if len(line.strip()) > 0 and line[0] != "="])


def clean_dates_in_parenthesis(string):
    return re.sub("\((?:\([^()]*\)|[^()])*\)", "", string).replace("  ", " ")


def fetch_content_from_source(article_name, lang):
    client = Algorithmia.client(config.ALGORITHMIA_CONFIG["client"])
    algo = client.algo(ALGORITHMIA_ALGO_VERSION)
    return algo.pipe({
      "articleName": article_name,
      "lang": lang
    }).result["content"]


def extract_sentences_from_content(content, number_of_sentences):
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    return tokenizer.tokenize(content)[:number_of_sentences]


def fetch_keywords_from_sentence(sentence):
    nlu = NaturalLanguageUnderstandingV1(version=config.WATSON_CONFIG["version"],
                                         url=config.WATSON_CONFIG["url"],
                                         iam_apikey=config.WATSON_CONFIG["iam_apikey"])
    response = nlu.analyze(text=sentence, features=Features(keywords=KeywordsOptions()))
    return extract_text_from_keywords_list(response.result["keywords"])


def extract_text_from_keywords_list(keywords):
    return [keyword["text"] for keyword in keywords if keyword["relevance"] > MINIMUM_KEYWORD_RELEVANCE]


def fetch_keywords_from_content(content):
    sentence_list = []
    for sentence in extract_sentences_from_content(content, MAXIMUM_SENTENCES_TO_EXTRACT):
        new_sentence = Sentence()
        new_sentence.text = sentence
        new_sentence.keywords = fetch_keywords_from_sentence(sentence)
        sentence_list.append(new_sentence)
    return sentence_list
