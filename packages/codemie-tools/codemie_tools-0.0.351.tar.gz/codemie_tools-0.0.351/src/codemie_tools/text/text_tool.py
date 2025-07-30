from typing import Type, Any, Optional

import chardet
from pydantic import BaseModel, Field

from codemie_tools.base.codemie_tool import CodeMieTool
from codemie_tools.text.tool_vars import TEXT_TOOL


class TextTool(CodeMieTool):
    """ Tool for working with data from Plain Text files. """
    args_schema: Optional[Type[BaseModel]] = None
    name: str = TEXT_TOOL.name
    label: str = TEXT_TOOL.label
    description: str = TEXT_TOOL.description
    file_content: Any = Field(exclude=True)

    def execute(self):
        bytes_data = self.bytes_content()
        encoding = chardet.detect(bytes_data)['encoding']
        data = bytes_data.decode(encoding)

        return str(data)

    def bytes_content(self) -> bytes:
        """
        Returns the content of the file as bytes
        """
        if self.file_content is None:
            raise ValueError("File content is not set")
        if isinstance(self.file_content, bytes):
            return self.file_content

        return self.file_content.encode('utf-8')
