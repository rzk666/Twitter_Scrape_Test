# SECOND VERSION 19:41 #
# Added an option to filter retweets & save scrape results to a .json file #
# Also, made the script run on if it's ran as main so it can also be used as a module #

# Modules Imports
from bs4 import BeautifulSoup
import requests
import re
import json


# Functions definition
def request_page(page_url):
    try:
        response = requests.get(page_url)
        print("Successfully received page \n --------- \n")
    except requests.exceptions.RequestException as e:
        print('Request failed: \n {}'.format(e))
        response = "Invalid Response"
    return response


def scrape_following(acc_soup, acc_handle):
    following_container = acc_soup.find(attrs={"href": "/{}/following".format(acc_handle)})
    following = int((following_container.find("span", class_="ProfileNav-value")).string)
    print("Successfully scraped following \n --------- \n{}".format(following))
    return following


def scrape_followers(acc_soup, acc_handle):
    followers_container = acc_soup.find(attrs={"href": "/{}/followers".format(acc_handle)})
    followers = int((followers_container.find("span", class_="ProfileNav-value")).string)
    print("Successfully scraped followers \n --------- \n{}".format(followers))
    return followers


def scrape_posts_likes(acc_soup, acc_handle):
    post_likes_container = acc_soup.find(attrs={"href": "/{}/likes".format(acc_handle)})
    post_likes = post_likes_container.find("span", class_="ProfileNav-value").string
    post_likes = re.sub('[,]', '', post_likes)
    print("Successfully scraped followers \n --------- \n{}".format(post_likes))
    return int(post_likes)


def scrape_account_tweets(acc_soup):
    tweets_container = acc_soup.find(attrs={"data-nav": "tweets"})
    tweets = tweets_container.find("span", class_="ProfileNav-value")
    tweets = tweets["data-count"]
    print("Successfully scraped tweets \n --------- \n{}".format(tweets))
    return int(tweets)


def scrape_tweets(acc_soup):
    tweets_limit = int(input("\n Enter number of tweets to scrape: \n"))
    if (input("\n Count retweets as well? (y/n)\n") != 'y'):
        tweets = acc_soup.find_all(lambda tweet: (("data-tweet-id" in tweet.attrs) and not ("js-retweet-text" in str(tweet))), limit=tweets_limit)
    else:
        tweets = acc_soup.find_all(lambda tweet: "data-tweet-id" in tweet.attrs, limit=tweets_limit)

    content_list = [tweet.find("p", class_="TweetTextSize").text for tweet in tweets]
    print("Successfully scraped {} account tweets \n --------- \n".format(tweets_limit))
    content_list = list(map(check_content, content_list))
    for index, cur_tweet in enumerate(content_list):
        print("Tweet {}: \n {} \n \n --------".format(int(index + 1), cur_tweet))
    return content_list


def check_content(content_string):
    if ("pic.twitter.com/" in content_string):
        if (content_string.startswith("pic.twitter.com")):
            return "IMAGE"
        else:
            return (content_string[0:content_string.index("pic.twitter.com")])
    return content_string


def scrape_account(acc_soup, acc_handle):
    return {"followers": scrape_followers(acc_soup, acc_handle),
            "following": scrape_following(acc_soup, acc_handle),
            "posts_likes": scrape_posts_likes(acc_soup, acc_handle),
            "total_tweets": scrape_account_tweets(acc_soup),
            "tweets_list": scrape_tweets(acc_soup)}


def save_to_json(scrape_results):
    if input("Save scrape results as data.JSON? (y/n)\n") == 'y':
        with open('data.json', 'w') as json_file:
            json.dump(scrape_results, json_file)


# Running script as main added, so you can also use this as a module


if __name__ == "__main__":
    account_handle = input("Enter account to scrape: \n")

    account_to_scrape = request_page("https://twitter.com/" + account_handle)

    account_soup = BeautifulSoup(account_to_scrape.content, "html.parser")

    scrape_results = scrape_account(account_soup, account_handle)

    save_to_json(scrape_results)
