import requests
from termcolor import colored

def search_for_stock_videos(query: str, api_key: str, items: int = 10, min_dur: int = 0) -> list:
    """
    Searches for stock videos on Pexels with improved verbosity.

    Args:
        query (str): The search query for the videos.
        api_key (str): The Pexels API key for authentication.
        items (int): The number of items to retrieve per page.
        min_dur (int): The minimum duration of videos in seconds.

    Returns:
        list: A list containing URLs of the videos that match the criteria.
    """
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": items}
    url = "https://api.pexels.com/videos/search"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.

        data = response.json()
        video_urls = []

        for video in data.get("videos", []):
            if video["duration"] >= min_dur:
                highest_resolution_video = max(video["video_files"], key=lambda x: x["width"] * x["height"])
                video_urls.append(highest_resolution_video["link"])

        if video_urls:
            print(colored(f"Found {len(video_urls)} videos for query \"{query}\" with minimum duration of {min_dur} seconds.", "green"))
        else:
            print(colored(f"No videos found for query \"{query}\" with the specified criteria.", "yellow"))

        return video_urls

    except requests.RequestException as e:
        print(colored(f"Error during request: {e}", "red"))
    except ValueError as e:
        print(colored("Error processing JSON response.", "red"))
    except Exception as e:
        print(colored(f"An unexpected error occurred: {e}", "red"))

    return []