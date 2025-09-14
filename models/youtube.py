import feedparser
import datetime

def get_latest_video(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return None

    entry = feed.entries[0]

    # 動画 or ライブの区別
    is_live = "yt:live" in entry.get("title", "").lower()

    video_data = {
        "title": entry.title,
        "url": entry.link,
        "published": entry.published,
        "is_live": is_live,
        "id": entry.yt_videoid,
    }

    return video_data
