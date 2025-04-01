from instagrapi import Client
import random as r
import time
import schedule
from datetime import datetime, timedelta

USERNAME = 'aurora_creation1'
PASSWORD = '******'

tags = ["pixelart", "gamedev", "indiegame", "pythoncoding", "programming", "coding", "python", "javascript", "webdevelopment", "webdesign", "webdeveloper", "webdev", "webdesigner", "webdesigning"]

comments = ["Great post! Keep it up!", "Awesome work! Keep it up!", "Nice post! Keep it up!", "Amazing work! Keep it up!", "Great content! Keep it up!", "Awesome content! Keep it up!", "Nice content! Keep it up!", "Amazing content! Keep it up!", "Great job! Keep it up!", "Awesome job! Keep it up!", "Nice job! Keep it up!", "Amazing job! Keep it up!"]

followed_users = {}  # Dictionary to store followed users and the follow timestamp

def search_tags():
    client = Client()
    client.login(USERNAME, PASSWORD)

    num_interaction_posts = r.randint(1, 5)

    time.sleep(r.randint(2000, 7000) / 1000)

    tag_choice = r.choice(tags)
    hashtag_posts = client.hashtag_medias_recent(tag_choice)

    print(f"... Searched TAG ({tag_choice}) ...")
    print(f"... Proceeding to interact with {len(hashtag_posts)} posts ...")

    chosen_post_ids = []

    for i in range(num_interaction_posts):
        insertion_index = r.randint(0, len(hashtag_posts) - 1)

        while insertion_index in chosen_post_ids:
            insertion_index = r.randint(0, len(hashtag_posts) - 1)

        chosen_post_ids.append(insertion_index)

    for i in chosen_post_ids:
        print(f"... Interacting with POST caption - '{hashtag_posts[i].caption_text}' ...")

        like = True
        if r.randint(0, 100) == 50:
            like = False

        follow = True
        if r.randint(0, 100) == 50:
            follow = False

        comment = True
        if r.randint(0, 100) == 50:
            comment = False

        media_id = hashtag_posts[i].pk
        user_id = hashtag_posts[i].user.pk

        time.sleep(r.randint(4000, 8000) / 1000)

        if follow:
            time.sleep(r.randint(3000, 9000) / 1000)

            try:
                client.user_follow(user_id)
                followed_users[user_id] = datetime.now()  # Track the follow timestamp
                print(f"... Followed user {user_id} ...")
            except Exception as e:
                print("Too many follow requests. Slow down following.")

        if comment:
            try:
                client.media_comment(media_id, r.choice(comments))
            except Exception as e:
                print("Too many comment requests. Slow down commenting.")

        print("... post interacted ...")

def unfollow_non_followers():
    client = Client()
    client.login(USERNAME, PASSWORD)

    current_time = datetime.now()
    for user_id, follow_time in list(followed_users.items()):
        try:
            is_following_back = client.user_info(user_id).following
            if not is_following_back:
                if current_time - follow_time > timedelta(days=4):
                    client.user_unfollow(user_id)
                    del followed_users[user_id]
                    print(f"... Unfollowed user {user_id} (did not follow back within 4 days) ...")
            else:
                del followed_users[user_id]  # Remove from tracking if they follow back
        except Exception as e:
            print(f"Error checking user {user_id}: {e}")

    # Unfollow all users who are not following back
    following = client.user_following(client.user_id)
    followers = client.user_followers(client.user_id)
    for user_id in following.keys():
        if user_id not in followers:
            try:
                client.user_unfollow(user_id)
                print(f"... Unfollowed user {user_id} (not following back) ...")
            except Exception as e:
                print(f"Error unfollowing user {user_id}: {e}")

search_tags()

time_1 = str(r.randint(10, 12)) + ":" + str(r.randint(10, 59))
time_2 = str(r.randint(14, 16)) + ":" + str(r.randint(10, 59))
time_3 = str(r.randint(17, 21)) + ":" + str(r.randint(10, 59))

schedule.every().day.at(time_1).do(search_tags)
schedule.every().day.at(time_2).do(search_tags)
schedule.every().day.at(time_3).do(search_tags)
schedule.every().day.at("23:00").do(unfollow_non_followers)  # Schedule unfollow task daily

print("Scheduled time for\n:" + time_1 + "\n" + time_2 + "\n" + time_3)

while True:
    schedule.run_pending()
    time.sleep(1)
