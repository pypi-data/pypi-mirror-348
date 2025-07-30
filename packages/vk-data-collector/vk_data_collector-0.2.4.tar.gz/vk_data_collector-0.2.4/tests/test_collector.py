class DummyService:
    """Stub for Service to avoid real requests to VK API."""

    def get_wall_posts_by_domain(self, domain, count=1, offset=0):
        # Return fake data imitating VK API structure
        if count == 1:
            return {"response": {"count": 3}}
        # Three posts with different dates (timestamp)
        return {
            "response": {
                "items": [
                    {
                        "date": 1740769200,  # "2025-03-01"
                        "id": 1,
                        "owner_id": 1,
                        "comments": {"count": 0},
                    },
                    {
                        "date": 1738350000,  # "2025-02-01"
                        "id": 2,
                        "owner_id": 1,
                        "comments": {"count": 0},
                    },
                    {
                        "date": 1735671600,  # "2025-01-01"
                        "id": 3,
                        "owner_id": 1,
                        "comments": {"count": 0},
                    },
                ]
            }
        }


def test_collect_posts_to_date(tmp_path):
    # Create collector with a stubbed service
    from src.collector.collector import Collector

    collector = Collector(service=DummyService())

    # Collect posts up to date "2025-03-01" (timestamp 1740769200)
    # Only the first post (1740769200) should be included
    result_files = collector.collect_posts_to_date(
        ["testgroup"], "2025-02-28", str(tmp_path),
    )
    assert len(result_files) == 1

    # Check file contents
    import json

    with open(result_files[0], encoding="utf-8") as f:
        posts = json.load(f)
    assert len(posts) == 1
    assert posts[0]["date"] == 1740769200


def test_collect_all_posts(tmp_path):
    # Create collector with a stubbed service
    from src.collector.collector import Collector

    collector = Collector(service=DummyService())

    # Collect all posts
    result_files = collector.collect_all_posts(["testgroup"], str(tmp_path))
    assert len(result_files) == 1

    # Check file contents
    import json

    with open(result_files[0], encoding="utf-8") as f:
        posts = json.load(f)
    assert len(posts) == 3
    assert posts[0]["date"] == 1740769200
