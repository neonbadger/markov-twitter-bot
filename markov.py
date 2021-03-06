import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as strifilenames:
        text_file = open(filenng; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    upper_case_keys = []
    all_keys = chains.keys()

    for word_set in all_keys:
        if word_set[0][0].isupper():
            upper_case_keys.append(word_set)

    key = choice(upper_case_keys)
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    joined_text = " ".join(words)

    
    # slice text string if it's over 140 characters

    if len(joined_text) > 140:
        joined_text = joined_text[:140]


        # check the last punctuation, and if it is '?', '.', or '--', slice up to
        # these punctuations. Otherwise, slice up to the last space

        if '.' in joined_text and '?' in joined_text: 
            last_question_mark_index = joined_text.rindex('?') 
            last_period_index = joined_text.rindex('.')  
            max_index = max(last_period_index, last_question_mark_index)
            joined_text = joined_text[:max_index + 1]
        elif '.' in joined_text:    
            last_period_index = joined_text.rindex('.') 
            joined_text = joined_text[:last_period_index + 1] 
        elif '?' in joined_text: 
            last_question_mark_index = joined_text.rindex('?')       
            joined_text = joined_text[:last_question_mark_index + 1]
        elif '--' in joined_text:
            last_double_dash_index = joined_text.rindex('--')
            joined_text = joined_text[:last_double_dash_index - 1] + '.'
        else:
            last_space_index = joined_text.rindex(" ")
            joined_text = joined_text[:last_space_index]


    return joined_text

def tweet(text):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    
    api = twitter.Api (
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


    print api.VerifyCredentials()

    status = api.PostUpdate(text)

    print status.text



# # Get the filenames from the user through a command line prompt, ex:
# # python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1]

# # Open the files and turn them into one long string
# text = open_and_read_file(filenames)

# # Get a Markov chain
# chains = make_chains(text)

# # Your task is to write a new function tweet, that will take chains as input
# # tweet(chains)

# text_body = make_text(chains)

# print text_body

# tweet(text_body)


# print tweet_again


def auto_tweet(filename):
    text = open_and_read_file(filename)
    chains = make_chains(text)
    text_body = make_text(chains)
    tweet(text_body)

file_list = sys.argv[1:]

print file_list

auto_tweet(file_list)

tweet_again = raw_input('Enter to tweet again [q to quit] [hit <Return> to continue] > ')

while True:
    if tweet_again == '': 
        print "Success"
        auto_tweet(file_list)
        tweet_again = raw_input('Enter to tweet again [q to quit] [hit <Return> to continue] > ')

    elif tweet_again == 'q':
        print "Thank you for using the Dori-Shijie twitter bot."
        break
    else:
        print "Invalid response."
        tweet_again = raw_input('Enter to tweet again [q to quit] [hit <Return> to continue] > ')
        continue

