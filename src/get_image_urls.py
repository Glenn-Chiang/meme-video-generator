import sys

def get_image_urls(reddit_service, target_subreddit, num_images_required):
    image_urls = []
    # How many posts to fetch from the subreddit each time
    batch_size = num_images_required
    # How many posts (including skipped non-image posts) scraped from the subreddit so far
    total_posts_scraped = 0
    # Keep track of the id of the latest post that was scraped
    last_post_id = None

    while (len(image_urls) < num_images_required):
        posts = []
        try:
            posts, last_post_id = reddit_service.get_subreddit_posts(
                subreddit_name=target_subreddit, limit=batch_size, after=last_post_id)
            # Every time we fetch a batch of posts, update the total number of posts fetched so far
            total_posts_scraped += batch_size
        except Exception as error:
            print(f'Error getting posts for r/{target_subreddit}: {error}')
            sys.exit()

        # If we fetch 0 posts from a batch, we assume there are no more posts in the subreddit and stop trying to fetch more
        if not posts:
            break

        # Image urls obtained only from this batch
        image_urls_in_batch = 0
        for post_meta in posts:
            post = post_meta['data']
            image_url: str = post['url']

            # Skip non-image posts
            if post['domain'] != 'i.redd.it' or image_url.endswith('gif'):
                continue

            image_urls_in_batch += 1
            image_urls.append(image_url)
            print(image_url)
            if len(image_urls) >= num_images_required:
                break

        # If none of the posts in the batch are images, stop fetching posts
        if image_urls_in_batch == 0:
            break

    # If we are unable to fetch a single post from the given subreddit name, we assume that this subreddit does not exist and exit the program
    if total_posts_scraped == 0:
        print(f'Error getting posts from r/{target_subreddit}')
        return
    
    return image_urls