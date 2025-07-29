import json
import os
import sys
from pathlib import Path

from lib.types.objects.comment import Comment
from service.service import Service


class Collector:
    def __init__(self, service: Service):
        self.service = service
        self.encoding = sys.getdefaultencoding()

    def _process_path(self, path: str) -> Path:
        """Ensure that the given path exists by creating directories if needed."""

        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _write_chunk(
        self, base_filename: str, chunk_index: int, data: list | dict, path: Path
    ) -> None:
        """Save a single chunk of data to a file with the name '{base_filename}_
        chunk_{chunk_index}.json'.
        """
        chunk_file_path = path.joinpath(f"{base_filename}_chunk_{chunk_index}.json")
        with open(chunk_file_path, "w", encoding=self.encoding) as f:
            json.dump(data, f, ensure_ascii=False)

    def _merge_chunks(
        self,
        base_filename: str,
        total_chunks: int,
        path: Path,
        merge_mode: str = "list",
    ) -> str:
        """Merge all saved chunks into a single JSON file named '{base_filename}.json'.

        The merge_mode parameter defines the merging strategy:
        - 'list': concatenates lists using extend,
        - 'dict': merges dictionaries using update.

        The temporary chunk files are removed only after the final JSON file
        has been saved.
        """
        if merge_mode == "list":
            merged_data = []
        elif merge_mode == "dict":
            merged_data = {}
        else:
            raise ValueError("merge_mode must be either 'list' or 'dict'")

        chunk_files = []
        # Read and merge all chunk files
        for i in range(total_chunks):
            chunk_file_path = path.joinpath(f"{base_filename}_chunk_{i}.json")
            chunk_files.append(chunk_file_path)
            with open(chunk_file_path, "r", encoding=self.encoding) as f:
                chunk_data = json.load(f)
            if merge_mode == "list":
                merged_data.extend(chunk_data)
            elif merge_mode == "dict":
                merged_data.update(chunk_data)

        # Save final JSON file
        final_file_path = path.joinpath(f"{base_filename}.json")
        with open(final_file_path, "w", encoding=self.encoding) as f:
            json.dump(merged_data, f, ensure_ascii=False)

        # Remove all temporary chunk files
        for chunk_file_path in chunk_files:
            os.remove(chunk_file_path)

        return str(final_file_path)

    def collect_all_posts(self, domains: list[str], path: str) -> list[str]:
        """Collect all posts for the specified VK domains and save them in chunks,
        then merge the chunks into a single output file.
        """
        final_saved_files = []

        for domain in domains:
            posts_path = self._process_path(path)

            response = self.service.get_wall_posts_by_domain(domain, count=1)

            # Get the total count of posts and determine the number of chunks
            count = response["response"]["count"]
            chunk_size = 100
            runs = (count + chunk_size - 1) // chunk_size

            base_filename = f"{domain}_posts"
            for i in range(runs):
                response = self.service.get_wall_posts_by_domain(
                    domain, count=chunk_size, offset=chunk_size * i
                )
                print(
                    f"COLLECTED POSTS FROM {domain}: {min(chunk_size * (i + 1), count)}/{count}"
                )
                items = response["response"]["items"]

                # Save each chunk to a separate file
                self._write_chunk(base_filename, i, items, posts_path)

            # Merge all chunks into a single file and remove temporary chunk files
            final_saved_files.append(
                self._merge_chunks(base_filename, runs, posts_path, merge_mode="list")
            )
        return final_saved_files

    def collect_groups(self, domains: list[str], path: str) -> list[str]:
        """Collect group information for the specified domains and save to groups.json."""

        groups_path = self._process_path(path)

        fields = (
            "activity,wall,city,description,cover,members_count,place,site,"
            "status,public_date_label,age_limits,has_photo,wiki_page,verified"
        )

        saved_files = []

        for i, domain in enumerate(domains):
            response = self.service.get_group_by_domain(domain, fields=fields)
            print(f"COLLECTED GROUPS: {i + 1}/{len(domains)}")

            groups = response["response"]["groups"]

            file_path = groups_path.joinpath(f"{domain}_group.json")
            with open(file_path, "w", encoding=self.encoding) as f:
                json.dump(groups, f, ensure_ascii=False)

            saved_files.append(file_path)
        return saved_files

    def get_comments(self, owner_id: int, post_id: int) -> list[Comment]:
        """Collect all comments for a post (including nested replies)."""

        chunk_size = 100

        first_res = self.service.get_comments_by_wall_post(
            owner_id=owner_id,
            post_id=post_id,
            count=chunk_size,
            thread_items_count=10,
        )
        response = first_res["response"]

        top_level_count = response["current_level_count"]
        top_level_comments = response["items"]
        top_level_received = len(top_level_comments)

        while top_level_received < top_level_count:
            next_res = self.service.get_comments_by_wall_post(
                owner_id=owner_id,
                post_id=post_id,
                count=chunk_size,
                offset=top_level_received,
                thread_items_count=10,
            )
            items = next_res["response"]["items"]
            top_level_comments.extend(items)
            top_level_received += len(items)

            if len(items) < chunk_size:
                break

        for comment in top_level_comments:
            thread = comment["thread"]
            thread_level_count = thread["count"]

            if thread_level_count <= 10:
                continue

            thread_level_comments = thread["items"]
            thread_level_received = len(thread_level_comments)

            while thread_level_received < thread_level_count:
                thread_res = self.service.get_thread_by_comment(
                    owner_id=owner_id,
                    post_id=post_id,
                    comment_id=comment["id"],
                    count=chunk_size,
                    offset=thread_level_received,
                )
                thread_items = thread_res["response"]["items"]
                thread_level_comments.extend(thread_items)
                thread_level_received += len(thread_items)

                if len(thread_items) < chunk_size:
                    break

        return top_level_comments

    def collect_comments_for_posts(
        self, post_files: list[str], path: str, posts_chunk_size: int = 100
    ) -> list[str]:
        """Collect comments for the previously collected posts by processing posts
        in chunks (default: 100 posts per chunk). Each chunk is saved as
        a temporary JSON file, then all chunks are merged into a single output file.
        """
        comments_path = self._process_path(path)

        final_saved_files = []

        for post_file in post_files:
            with open(post_file, "r", encoding=self.encoding) as f:
                posts = json.load(f)

            num_posts = len(posts)
            total_chunks = (num_posts + posts_chunk_size - 1) // posts_chunk_size
            base_filename = Path(post_file).stem + "_comments"

            for chunk_index in range(total_chunks):
                start = chunk_index * posts_chunk_size
                end = min(start + posts_chunk_size, num_posts)
                chunk_posts = posts[start:end]

                comments_dict_chunk = {}

                for i, post in enumerate(chunk_posts, start=start):
                    if post["comments"]["count"] == 0:
                        continue
                    post_comments = self.get_comments(post["owner_id"], post["id"])
                    print(f"COLLECTED COMMENTS TO POSTS: {i + 1}/{num_posts}")
                    key = f"{post['owner_id']}_{post['id']}"
                    comments_dict_chunk[key] = post_comments

                self._write_chunk(
                    base_filename, chunk_index, comments_dict_chunk, comments_path
                )

            final_saved_files.append(
                self._merge_chunks(
                    base_filename, total_chunks, comments_path, merge_mode="dict"
                )
            )
        return final_saved_files
