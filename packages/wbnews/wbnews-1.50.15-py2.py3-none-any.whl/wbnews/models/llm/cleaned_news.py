from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from wbcore.contrib.ai.llm.config import LLMConfig

if TYPE_CHECKING:
    from wbnews.models import News  # noqa


class CleanNewsModel(BaseModel):
    title: str = Field(
        ...,
        description="The news title cleaned from the email subject without any formatting only meaningful information",
    )
    description: str = Field(
        ...,
        description="The news description cleaned from the email body without any formatting and retaining only meaningful information",
    )


class SummarizedNewsModel(BaseModel):
    summary: str = Field(
        ...,
        description="A summary of the news description in English.",
    )


clean_news_config = LLMConfig["News"](
    key="clean",
    output_model=CleanNewsModel,
    prompt=[
        SystemMessage(
            content="I have an HTML email title and body, and I want to extract only the meaningful content in plain text format, removing all metadata, subscription links, and non-essential parts. The output should be HTML- and Markdown-free and should exclude any text related to links, subscription information, or common phrases like 'Unsubscribe' or 'View online'. Only retain the main email content but do not remove any information related to news."
        ),
        HumanMessage(
            content="Title: {title}\n\nDescription: {description}",
        ),
    ],
    on_save=True,
    on_condition=lambda n: n.source.clean_content,
    query=lambda instance: {"description": instance.description, "title": instance.title},
)

summarized_news_config = LLMConfig["News"](
    key="summarize",
    output_model=SummarizedNewsModel,
    prompt=[
        SystemMessage(content="Given this news description, please extract a short summary"),
        HumanMessage(
            content="Description: {description}",
        ),
    ],
    on_save=True,
    on_condition=lambda n: not n.summary,
    query=lambda instance: {"description": instance.description},
)
