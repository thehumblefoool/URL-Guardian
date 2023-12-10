import pandas as pd
import re
from urllib.parse import urlparse
import math

sensitive_words = [
    'confirm', 'account', 'secure', 'webscr', 'banking', 'login', 'signin',
    'password', 'credit', 'payment', 'phishing', 'fraud', 'identity', 'verify',
    'transaction', 'personal', 'information', 'update', 'authentication', 'hack',
    'verify', 'validate', 'unauthorized', 'suspicious', 'alert', 'verify', 'suspend',
    'validate', 'block', 'limit', 'warning', 'expire', 'verify', 'verifyaccount',
    'access', 'urgent', 'login', 'verifyemail', 'reset', 'verifylogin', 'unusualactivity'
]

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
    shorteners = [
        'bit.ly', 'tinyurl.com', 'goo.gl', 'rebrand.ly', 't.co', 'ow.ly', 
        'is.gd', 'buff.ly', 'adf.ly', 'bit.do', 'mcaf.ee', 'youtu.be', 
        'shorte.st', 'tiny.cc', 'cutt.ly', 'bl.ink', 'qr.net', 'shorturl.at', 
        'zpr.io', 'v.gd', 'tr.im', 's.id', 'qps.ru', 'bitly.com', 'clk.im', 
        'db.tt', 'linklyhq.com', 'shorl.com', 'clicky.me', 'budurl.com'
    ]
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return 1 if domain in shorteners else 0

#Function to count special characters
def count_specialchar(url):
    special_chars = ['!', '*', '$', '%', '#', ',', '&', '?', ';', '_']
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
        return 1 #Low
    elif len(num_dots) == 4: 
        return 0 #Moderate
    else:
        return -1 #High

def contains_ip_address(url):
    # Define regular expression patterns for IPv4 and IPv6 addresses
    ipv4_pattern = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ipv6_pattern = r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,6}(:[0-9a-fA-F]{1,4}){1,2}"

    # Check if either IPv4 or IPv6 pattern is found in the URL
    match_ipv4 = re.search(ipv4_pattern, url)
    match_ipv6 = re.search(ipv6_pattern, url)

    if match_ipv4 or match_ipv6:
        return 1  # IP address found
    else:
        return 0  # IP address not found

def numchar_classification(domain_name):
    if not domain_name:
        return -1  # Indicates an error or abnormal condition
    numeric_chars = sum(c.isdigit() for c in domain_name)
    ratio = numeric_chars / len(domain_name)
    high_ratio_threshold = 0.5
    moderate_ratio_threshold = 0.2
    if ratio > high_ratio_threshold:
        return -1  # Suspicious
    elif moderate_ratio_threshold < ratio <= high_ratio_threshold:
        return 0  # Gray area
    else:
        return 1  # Normal

#Function to extract the domain name
def get_domain_from_url(url):
    return urlparse(url).netloc

#Function to calculate the URL entropy
def calculate_entropy(url):
    # Shannon Entropy Formula
    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    
    if entropy < 3:
        return -1  # Low entropy
    elif 3 <= entropy < 4:
        return 0  # Moderate entropy
    else:
        return 1  # High entropy


df = pd.read_csv('Dataset\Raw Dataset.csv')

#Feature extraction
df['label'] = df['label'].replace({'malicious': 1, 'benign': 0})
df['count_specialchar'] = df['url'].apply(count_specialchar)
df['count_sensitive_words'] = df['url'].apply(lambda x: count_sensitive_words(x, sensitive_words))
df['using_shortener'] = df['url'].apply(check_shortening_service)
df['has_at_symbol'] = df['url'].apply(has_at_symbol)
df['count_double_slash'] = df['url'].apply(count_double_slash)
df['count_dash_symbol'] = df['url'].apply(count_dash_symbol)
df['count_multiple_subdomains'] = df['url'].apply(count_multiple_subdomains)
df['url_length'] = df['url'].apply(get_url_length)
df['https'] = df['url'].apply(check_https)
df['contains_ip_address'] = df['url'].apply(contains_ip_address)
df['url_entropy'] = df['url'].apply(calculate_entropy)
df['numchar_classification'] = df['url'].apply(lambda x: numchar_classification(get_domain_from_url(x)))

#Save to a new csv file
df.to_csv('Dataset_Features.csv', index=False)
