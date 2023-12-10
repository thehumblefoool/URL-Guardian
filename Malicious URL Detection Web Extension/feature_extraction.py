# Import necessary modules and libraries
import pandas as pd
import re
from urllib.parse import urlparse
import math

#Import necessary patterns from patterns.py 
from patterns import *

#Function to determine URL length
def get_url_length(url):
    if len(url) < 54:
        return 1 #Low
    elif 54 <= len(url) <= 75:
        return 0 #Moderate
    return -1 #High

#Function to check if the URL starts with "https://"
def check_https(url):
    return 1 if url.startswith('https://') else 0

#Function to check if the URL is using a shortening service
def check_shortening_service(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return 1 if domain in shorteners else 0

#Function to count special characters
def count_specialchar(url):
    count = sum(url.count(char) for char in special_chars)
    return count

#Function to count sensitive words
def count_sensitive_words(url, sensitive_words):
    url_lower = url.lower()
    count = sum(url_lower.count(word) for word in sensitive_words)
    return count

#Function to check for the presence of '@' 
def has_at_symbol(url):
    return 1 if "@" in url else 0

#Function to count double slashes
def count_double_slash(url):
    return url.count('//')

#Function to count dash
def count_dash_symbol(url):
    return url.count('-')

#Function to count subdomains
def count_multiple_subdomains(url):
    num_dots = [x.start() for x in re.finditer(r'\.', url)]
    if len(num_dots) <= 3:
        return 1  #Low
    elif len(num_dots) == 4:
        return 0  #Moderate
    else:
        return -1  #High

#Function to check the presence of IP address pattern
def contains_ip_address(url):
    ip_address_pattern = ipv4_pattern + "|" + ipv6_pattern
    match = re.search(ip_address_pattern, url)
    return -1 if match else 1

#Function to get the ratio of numerical characters
def numchar_classification(domain_name):
    if not domain_name:
        return -1  #Error or abnormal
    numeric_chars = sum(c.isdigit() for c in domain_name)
    ratio = numeric_chars / len(domain_name)
    high_ratio_threshold = 0.5
    moderate_ratio_threshold = 0.2
    if ratio > high_ratio_threshold:
        return -1  #High
    elif moderate_ratio_threshold < ratio <= high_ratio_threshold:
        return 0  #Moderate
    else:
        return 1  #Low

#Function to extract the domain name
def get_domain_from_url(url):
    return urlparse(url).netloc

#Function to calculate the URL entropy
def calculate_entropy(url):
    #Shannon Entropy Formula
    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])

    if entropy < 3:
        return -1  #Low
    elif 3 <= entropy < 4:
        return 0  #Moderate
    else:
        return 1  #High

#Function to extract features from the URL
def extract_features(url):
    features = {
        'count_specialchar': count_specialchar(url),
        'count_sensitive_words': count_sensitive_words(url, sensitive_words),
        'using_shortener': check_shortening_service(url),
        'has_at_symbol': has_at_symbol(url),
        'count_double_slash': count_double_slash(url),
        'count_dash_symbol': count_dash_symbol(url),
        'count_multiple_subdomains': count_multiple_subdomains(url),
        'url_length': get_url_length(url),
        'https': check_https(url),
        'contains_ip_address': contains_ip_address(url),
        'url_entropy': calculate_entropy(url),
        'numchar_classification': numchar_classification(get_domain_from_url(url))
    }

    return list(features.values())
