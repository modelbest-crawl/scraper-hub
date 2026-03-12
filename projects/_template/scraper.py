"""
{{PROJECT}} 爬虫
负责人: {{OWNER}}
"""

from packages.core.base_scraper import BaseScraper


class Scraper(BaseScraper):

    def __init__(self):
        super().__init__("{{OWNER}}/{{PROJECT}}")

    def fetch(self, url: str) -> dict:
        response = self.client.get(url)
        return response.json() if hasattr(response, "json") else {"html": response.text}

    def parse(self, raw_data: dict) -> list:
        # TODO: 实现解析逻辑
        raise NotImplementedError("请实现 parse 方法")

    def save(self, items: list):
        from packages.storage import FileStore

        store = FileStore(f"data/{{OWNER}}/{{PROJECT}}")
        store.save_jsonl(items, "result.jsonl")
        self.logger.info(f"保存 {len(items)} 条数据")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
