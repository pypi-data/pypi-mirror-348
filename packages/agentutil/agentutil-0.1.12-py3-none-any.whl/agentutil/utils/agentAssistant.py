from abc import ABC, abstractmethod
from agentutil.utils.models import News


class AgentAssistant(ABC):
    SUCCESS_FINAL_STATE = "موفق✅"
    FAILURE_FINAL_STATE = "ناموفق❌"
    @abstractmethod
    def publish_article(self, news_id: str, news: News):
        pass

    @abstractmethod
    def update_news_status(
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
            ):
        pass


class TestAgentAssistant(AgentAssistant):
    def __init__(self):
        super().__init__()

    def publish_article(self, news_id: str, news: News):
        print(f"Publishing article: {news.title} for user: {news_id}")
        return True, 1111

    def update_news_status(
        self,
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
            ):
        print(f"Updating news status: {news_id} to {new_status}")
        if title:
            print(f"Title: {title}")
        if cms_news_id: 
            print(f"CMS News ID: {cms_news_id}")
        if cost:
            print(f"Cost: {cost}")
        if duration:
            print(f"Duration: {duration}")
        # Simulate a database update
        # In a real implementation, this would update the database
        # For this test, we'll just print the values
        print("News status updated successfully.")
        # Simulate a successful update by returning True
        return True
