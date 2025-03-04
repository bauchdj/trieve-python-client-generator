# generated by borea

# if you want to edit this file, add it to ignores in borea.config.json, glob syntax

# TODO: not implemented

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from ....models.models import *

if TYPE_CHECKING:
    from ...trieve_api import TrieveApi


class SplitHtmlContent:
    def __init__(self, parent: "TrieveApi"):
        self.parent = parent

    def split_html_content(
        self,
        chunk_html: str,
        body_remove_strings: Optional[List[str]] = None,
        heading_remove_strings: Optional[List[str]] = None,
    ) -> Any:
        """
                This endpoint receives a single html string and splits it into chunks based on the headings and
        body content. The headings are split based on heading html tags. chunk_html has a maximum size
        of 256Kb.

                Args:
                    chunk_html: The HTML content to be split into chunks
                    body_remove_strings: Text strings to remove from body when creating chunks for each page
                    heading_remove_strings: Text strings to remove from headings when creating chunks for each page

                Returns:
                    Response data
        """
        path = f"/api/chunk/split"
        params = None
        headers = None
        json_data = {
            "body_remove_strings": (
                body_remove_strings if body_remove_strings is not None else None
            ),
            "chunk_html": chunk_html if chunk_html is not None else None,
            "heading_remove_strings": (
                heading_remove_strings if heading_remove_strings is not None else None
            ),
        }
        json_data = {k: v for k, v in json_data.items() if v is not None}

        response = self.parent._make_request(
            method="POST",
            path=path,
            params=params,
            headers=headers,
            json_data=json_data,
        )
        return response.json()
