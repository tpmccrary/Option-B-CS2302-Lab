# *************************
# NAME: Timothy P. McCrary
# CLASS: CS 2302
# LAB 1 OPTION B
# INSTRUCTOR: Diego Aguiree
# TA: Manoj Pravaka Saha
# DATE: 09/11/2018
# *************************

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
import time

reddit = praw.Reddit(client_id='CW1S2T7f6TTy-Q',
                     client_secret='m2ujS6NgrfMD12vs95wfhaWfTAY',
                     user_agent='Scoutbravo'
                     )

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Lists that will hold the comments.
negative_comments_list = []
neutral_comments_list = []
positive_comments_list = []


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


# Recursive function that analyzes comments
def process_comments(comment, index):
    # print("_____Start of Function_____\nINDEX IS: ", index)
    # print("Number of comments: ", len(comment))
    # BASE CASE.
    if index >= len(comment):
        # print("REACHED BASE CASE.")
        return
    else:
        # Checks a comment if it is negative, neutral, or positive and puts it in a list accordingly.
        # print("REACHED ELSE STATEMENT.")
        if get_text_negative_proba(comment[index].body) > get_text_neutral_proba(
                comment[index].body) and get_text_negative_proba(comment[index].body) > get_text_positive_proba(
                comment[index].body):
            negative_comments_list.append(comment[index].body)
        elif get_text_neutral_proba(comment[index].body) > get_text_negative_proba(
                comment[index].body) and get_text_neutral_proba(comment[index].body) > get_text_positive_proba(
                comment[index].body):
            neutral_comments_list.append(comment[index].body)
        elif get_text_positive_proba(comment[index].body) > get_text_negative_proba(
                comment[index].body) and get_text_positive_proba(comment[index].body) > get_text_neutral_proba(
                comment[index].body):
            positive_comments_list.append(comment[index].body)
        process_comments(comment, index + 1)
        # print("_____End of Else_____\nINDEX IS: ", index)
    if len(comment[index].replies) != 0:
        # print("REACHED SECOND IF STATEMENT.")
        comment = comment[index].replies
        process_comments(comment, 0)


# Prints the number of comments in each list.
def print_comment_lists():
    print("Number of Negative Comments: ", len(negative_comments_list))
    print("Number of Neutral Comments: ", len(neutral_comments_list))
    print("Number of Positive Comments: ", len(positive_comments_list))


# Prints all the comments out from the list.
def print_all_comments():
    # __________PRINTS OUT ALL COMMENTS IN THEIR RESPECTIVE LISTS________________
    print("__________NEGATIVE COMMENTS__________")
    for i in range(len(negative_comments_list)):
        print((i + 1), ") ", negative_comments_list[i], "\n***************\n")

    print("__________NEUTRAL COMMENTS__________")
    for i in range(len(neutral_comments_list)):
        print((i + 1), ") ", neutral_comments_list[i], "\n***************\n")

    print("__________POSITIVE COMMENTS__________")
    for i in range(len(positive_comments_list)):
        print((i + 1), ") ", positive_comments_list[i], "\n***************\n")


# Clears content of the lists.
def delete_list_contents():
    del negative_comments_list[:]
    del neutral_comments_list[:]
    del positive_comments_list[:]


def main():
    # __________TEST 1 - Given Reddit Link_________________________________________________
    print("_____TEST #1_____")
    comments = get_submission_comments(
        'https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    start_time = time.time()
    process_comments(comments, 0)
    print("Running Time(seconds): ", (time.time() - start_time))
    print_comment_lists()
    delete_list_contents()

    # __________Test 2 - Post with only 4 comments.____________________________________________________
    print("_____TEST #2_____")
    comments = get_submission_comments(
        'https://www.reddit.com/r/halo/comments/8rxz3x/unable_to_join_does_this_happen_to_anyone_else/')

    start_time = time.time()
    process_comments(comments, 0)
    print("Running Time(seconds): ", (time.time() - start_time))
    print_comment_lists()
    delete_list_contents()

    # __________Test 3 - Post with no comments(as of 09/10/18)_____________________________________
    print("_____TEST #3_____")
    comments = get_submission_comments(
        'https://www.reddit.com/r/BikiniBottomTwitter/comments/9f0oea/we_arent_all_good_noodles/')

    start_time = time.time()
    process_comments(comments, 0)
    print("Running Time(seconds): ", (time.time() - start_time))
    print_comment_lists()
    delete_list_contents()

    # __________Test 4 - Post with most comments 350,000(I could find)._______________________________________
    print("_____TEST #4_____")
    comments = get_submission_comments(
        'https://www.reddit.com/r/blog/comments/d14xg/everyone_on_team_reddit_would_like_to_raise_a/')

    start_time = time.time()
    process_comments(comments, 0)
    print("Running Time(seconds): ", (time.time() - start_time))
    print_comment_lists()
    delete_list_contents()

    # __________Test 5 - Post with 49,000 comments(crashes)._______________________________________
    print("_____TEST #5_____")
    comments = get_submission_comments(
        'https://www.reddit.com/r/news/comments/3v6iq7/authorities_respond_to_20_victim_shooting/')

    start_time = time.time()
    process_comments(comments, 0)
    print("Running Time(seconds): ", (time.time() - start_time))
    print_comment_lists()
    delete_list_contents()


main()
