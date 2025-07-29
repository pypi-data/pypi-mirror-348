"""
Example script showing how to use the VK data collector library.
"""

from vk_data_collector import create_collector


def main():
    # Your VK API access token
    token = "your_access_token_here"
    
    # Create a collector instance using the factory function
    collector = create_collector(token)

    # Example usage - replace with your group names
    vk_groups = ["group_name"]

    # Collect data - replace output_path with your desired directory
    base_output_path = "output_path"
    collector.collect_groups(vk_groups, f"{base_output_path}/groups")
    saved_post_files = collector.collect_all_posts(
        vk_groups, f"{base_output_path}/posts"
    )
    collector.collect_comments_for_posts(
        saved_post_files, f"{base_output_path}/comments"
    )


if __name__ == "__main__":
    main()
