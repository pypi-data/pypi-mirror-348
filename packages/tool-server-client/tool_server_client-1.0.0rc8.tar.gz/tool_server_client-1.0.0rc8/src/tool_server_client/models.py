import base64
from typing import Literal, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field


class MBaseModel(BaseModel):
    class Config:
        populate_by_name = True

class MoveMouseRequest(MBaseModel):
    """Request model for moving mouse"""
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")


class ClickMouseRequest(MBaseModel):
    """Request model for clicking mouse"""
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")
    button: Literal["left", "right", "middle", "double_click", "double_left"] = Field(
        "left", description="mouse button", alias="Button"
    )
    press: bool = Field(False, description="press mouse", alias="Press")
    release: bool = Field(False, description="release mouse", alias="Release")


class PressMouseRequest(MBaseModel):
    """Request model for pressing mouse"""
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")
    button: Literal["left", "right", "middle"] = Field(
        "left", description="mouse button", alias="Button"
    )


class ReleaseMouseRequest(MBaseModel):
    """Request model for releasing mouse"""
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")
    button: Literal["left", "right", "middle"] = Field(
        "left", description="mouse button", alias="Button"
    )


class DragMouseRequest(MBaseModel):
    """Request model for dragging mouse"""
    source_x: int = Field(0, description="source x position", alias="SourceX")
    source_y: int = Field(0, description="source y position", alias="SourceY")
    target_x: int = Field(0, description="target x position", alias="TargetX")
    target_y: int = Field(0, description="target y position", alias="TargetY")


class ScrollRequest(MBaseModel):
    """Request model for scrolling"""
    scroll_direction: str = Field(Literal["up", "down", "left", "right"], alias="Direction")
    scroll_amount: int = Field(0, description="scroll amount", alias="Amount")
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")


class PressKeyRequest(MBaseModel):
    """Request model for pressing key"""
    key: str = Field("", description="key", alias="Key")


class TypeTextRequest(MBaseModel):
    """Request model for typing text"""
    text: str = Field("", description="text", alias="Text")


class WaitRequest(MBaseModel):
    """Request model for waiting"""
    duration: int = Field(0, description="duration in milliseconds", alias="Duration")


class TakeScreenshotRequest(MBaseModel):
    """Request model for taking screenshot"""
    pass


class GetCursorPositionRequest(MBaseModel):
    """Request model for getting cursor position"""
    pass


class GetScreenSizeRequest(MBaseModel):
    """Request model for getting screen size"""
    pass


class ChangePasswordRequest(MBaseModel):
    """Request model for changing password"""
    username: str = Field("", description="username", alias="Username")
    new_password: str = Field("", description="new password", alias="NewPassword")


class ResponseMetadataModel(BaseModel):
    """Response metadata model"""
    RequestId: str = ""
    Action: str
    Version: str
    Service: str = "ecs"
    Region: str = ""


class BaseResponse(BaseModel):
    """Base response model for all API calls"""
    ResponseMetadata: ResponseMetadataModel = None
    Result: Dict[str, Any] = None


class CursorPositionResource(MBaseModel):
    """Resource model for cursor position"""
    x: int = Field(0, description="x position", alias="PositionX")
    y: int = Field(0, description="y position", alias="PositionY")


class CursorPositionResponse(BaseResponse):
    """Response model for getting cursor position"""
    Result: CursorPositionResource = None


class ScreenSizeResource(MBaseModel):
    """Resource model for screen size"""
    width: int = Field(0, description="width", alias="Width")
    height: int = Field(0, description="height", alias="Height")


class ScreenSizeResponse(BaseResponse):
    """Response model for getting screen size"""
    Result: ScreenSizeResource = None


class ScreenshotResource(MBaseModel):
    """Resource model for screenshot"""
    screenshot: str = Field(alias="Screenshot")


class ScreenshotResponse(BaseResponse):
    """Response model for taking screenshot"""
    Result: ScreenshotResource = None

class ReadFileRequest(MBaseModel):
    file_path: str = Field("", description="file path", alias="FilePath")

class ReadFileResource(MBaseModel):
    content: bytes = Field("", description="content", alias="Content")
    error: str = Field("", description="error", alias="Error")
class ReadFileResponse(BaseResponse):
    """Response model for reading file"""
    Result: ReadFileResource = None

    def _decode_content(self):
        if self.Result is None:
            return self
        if self.Result.content is None:
            return self
        self.Result.content = base64.b64decode(self.Result.content)
        return self

class ReadMultiFilesRequest(MBaseModel):
    file_paths: list[str] = Field([], description="file paths", alias="FilePaths")

class ReadMultiFilesResponse(BaseResponse):
    """Response model for reading multi files"""
    def _decode_content(self):
        if self.Result is None:
            return self
        print(f"result : {self.Result}")
        for _, v in self.Result.items():
            if isinstance(v, dict):
                if v.get("Content") is not None:
                    v["Content"] = base64.b64decode(v["Content"])
        return self

class ListDirectoryRequest(MBaseModel):
    dir_path: str = Field("", description="dir path", alias="DirPath")

class ListDirectoryResource(MBaseModel):
    files: list[str] = Field([], description="files", alias="Files")
    error: str = Field("", description="error", alias="Error")

class ListDirectoryResponse(BaseResponse):
    """Response model for listing directory"""
    Result: ListDirectoryResource = None

class SearchFileRequest(MBaseModel):
    dir_path: str = Field("", description="dir path", alias="DirPath")
    pattern: str = Field("", description="pattern", alias="Pattern")

class SearchFileResource(MBaseModel):
    files: list[str] = Field([], description="files", alias="Files")
    error: str = Field("", description="error", alias="Error")

class SearchFileResponse(BaseResponse):
    """Response model for searching file"""
    Result: SearchFileResource = None

class SearchCodeRequest(MBaseModel):
    file_path: str = Field("", description="file path", alias="FilePath")
    pattern: str = Field("", description="pattern", alias="Pattern")

class SearchCodeResource(MBaseModel):
    content: str = Field("", description="content", alias="Content")
    error: str = Field("", description="error", alias="Error")

class SearchCodeResponse(BaseResponse):
    """Response model for searching code"""
    Result: SearchCodeResource = None

class GetFileInfoRequest(MBaseModel):
    file_path: str = Field("", description="file path", alias="FilePath")

class GetFileInfoResource(MBaseModel):
    info: dict = Field({}, description="info", alias="Info")
    error: str = Field("", description="error", alias="Error")

class GetFileInfoResponse(BaseResponse):
    """Response model for getting file info"""
    Result: GetFileInfoResource = None

class CreateFileRequest(MBaseModel):
    file_path: str = Field("", description="file path", alias="FilePath")
    content: bytes = Field("", description="content", alias="Content")

class CreateFileResource(MBaseModel):
    error: str = Field("", description="error", alias="Error")

class CreateFileResponse(BaseResponse):
    """Response model for creating file"""
    Result: CreateFileResource = None

class ListSessionsRequest(MBaseModel):
    pass

class ListSessionsResource(MBaseModel):
    ouptut: str = Field("", description="output", alias="Output")
    error: str = Field("", description="error", alias="Error")

class ListSessionsResponse(BaseResponse):
    """Response model for listing sessions"""
    Result: ListSessionsResource = None

class ListProcessesRequest(MBaseModel):
    pass

class ListProcessesResource(MBaseModel):
    processes: list[dict] = Field([], description="processes", alias="Processes")

class ListProcessesResponse(BaseResponse):
    """Response model for listing processes"""
    Result: ListProcessesResource = None

class ExecuteCommandRequest(MBaseModel):
    command: str = Field("", description="command", alias="Command")
    timeout: int = Field(10, description="timeout", alias="Timeout")

class ExecuteCommandResource(MBaseModel):
    output: str = Field("", description="output", alias="Output")
    error: str = Field("", description="error", alias="Error")

class ExecuteCommandResponse(BaseResponse):
    """Response model for executing command"""
    Result: ExecuteCommandResource = None