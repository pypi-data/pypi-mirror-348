# VK Data Collector

A Python library for collecting data from VK (VKontakte) social network. Allows you to gather posts, comments, and group information from public VK walls.

## Features

- Collect posts from public walls (groups and users)
- Collect posts up to a specific date
- Collect comments for posts
- Collect group information
- Simple and intuitive API
- Data saved in JSON format

## Installation

```shell
pip install vk-data-collector
```

## Quick Start

```python
from vk_data_collector import create_collector

# Initialize with your VK API token
collector = create_collector("your_vk_service_token_here")

# List of VK walls to collect from
# Can be found in URL: https://vk.com/wall_name
walls = ["group_name", "public_wall_name"]

# Collect all posts
saved_files = collector.collect_all_posts(walls, "output/posts")

# Collect posts up to a specific date (YYYY-MM-DD)
saved_files_to_date = collector.collect_posts_to_date(walls, "2024-01-01", "output/posts_to_date")

# Collect comments for the posts
collector.collect_comments_for_posts(saved_files, "output/comments")

# Collect group information
collector.collect_groups(walls, "output/groups")
```

## Requirements

- Python 3.9+
- VK API Service Token ([How to get token](https://dev.vk.com/en/api/access-token/getting-started))

## License

MIT License
