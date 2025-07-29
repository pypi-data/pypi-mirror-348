# SPDX-FileCopyrightText: 2025-present Shane Rogers <shane@teer.ai>
#
# SPDX-License-Identifier: MIT

from typing import Dict, Any, Optional, TypedDict, NotRequired, Literal


# Provider-specific cache objects

class AnthropicCache(TypedDict):
    """Anthropic-specific cache information"""
    
    cache_creation_input_tokens: NotRequired[int]
    """The number of tokens used to create the cache."""
    
    cache_read_input_tokens: NotRequired[int]
    """The number of tokens read from the cache."""


class OpenAICache(TypedDict):
    """OpenAI-specific cache information"""
    
    input_cached_tokens: NotRequired[int]
    """The number of input tokens retrieved from cache."""


class GoogleCache(TypedDict):
    """Google-specific cache information"""
    
    cached_content_token_count: NotRequired[int]
    """The number of tokens retrieved from cache."""
    
    thoughts_token_count: NotRequired[int]
    """The number of tokens used for thoughts."""


class CacheObject(TypedDict):
    """Cache object containing provider-specific cache information"""
    
    anthropic: NotRequired[AnthropicCache]
    """Anthropic-specific cache information."""
    
    openai: NotRequired[OpenAICache]
    """OpenAI-specific cache information."""
    
    google: NotRequired[GoogleCache]
    """Google-specific cache information."""


class UsageObject(TypedDict):
    """Usage object containing token usage information"""
    
    input: int
    """The number of input tokens."""
    
    output: int
    """The number of output tokens."""
    
    cache: NotRequired[CacheObject]
    """Cache-related token information."""


# Provider type
Provider = Literal["anthropic", "openai", "google"]


class MetadataObject(TypedDict, total=False):
    """Metadata for attribution and analytics"""
    
    user_id: str
    """The ID of the user who made the request."""
    
    organization_id: str
    """The ID of the organization the user belongs to."""
    
    member_id: str
    """The ID of the member within the organization."""
    
    team_id: str
    """The ID of the team the user belongs to."""
    
    session_id: str
    """The ID of the user's session."""
    
    request_id: str
    """A unique identifier for the request."""
    
    project_id: str
    """The project or initiative the request is associated with."""


class PlatformObject(TypedDict):
    """Teer-specific platform information"""
    
    rate_card_id: str
    """The ID of the rate card to use for billing."""


class IngestPayload(TypedDict):
    """Payload for the ingest API"""
    
    provider: Provider
    """The LLM provider."""
    
    model: str
    """The model name."""
    
    function_id: NotRequired[str]
    """A unique identifier for the function or endpoint using the LLM."""
    
    usage: UsageObject
    """Token usage information."""
    
    trace_id: NotRequired[str]
    """A unique identifier for the trace. Used for distributed tracing."""
    
    span_id: NotRequired[str]
    """A unique identifier for the span within the trace."""
    
    parent_span_id: NotRequired[str]
    """The ID of the parent span, if applicable."""
    
    batch: NotRequired[bool]
    """Whether this was part of a batch operation."""
    
    platform: NotRequired[PlatformObject]
    """Teer-specific platform information."""
    
    billing: NotRequired[Dict[str, Any]]
    """Billing information."""
    
    metadata: NotRequired[MetadataObject]
    """Additional metadata for attribution and analytics."""
