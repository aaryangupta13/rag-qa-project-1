"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Any, Annotated

from pydantic import BaseModel, Field

# ============== Health Schemas ==============


class HealthResponse(BaseModel):
    """Health check response."""

    status: Annotated[str, Field(..., description="Service status")]
    timestamp: Annotated[datetime, Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )]
    version: Annotated[str, Field(..., description="Application version")]


class ReadinessResponse(BaseModel):
    """Readiness check response."""

    status: Annotated[str, Field(..., description="Service status")]
    qdrant_connected: Annotated[bool, Field(..., description="Qdrant connection status")]
    collection_info: Annotated[dict, Field(..., description="Collection information")]


# ============== Document Schemas ==============


class DocumentUploadResponse(BaseModel):
    """Response after document upload."""

    message: Annotated[str, Field(..., description="Status message")]
    filename: Annotated[str, Field(..., description="Uploaded filename")]
    chunks_created: Annotated[int, Field(..., description="Number of chunks created")]
    document_ids: Annotated[list[str], Field(..., description="List of document IDs")]


class DocumentInfo(BaseModel):
    """Document information."""

    source: Annotated[str, Field(..., description="Document source/filename")]
    metadata: Annotated[dict[str, Any], Field(
        default_factory=dict,
        description="Document metadata",
    )]


class DocumentListResponse(BaseModel):
    """Response for listing documents."""

    collection_name: Annotated[str, Field(..., description="Collection name")]
    total_documents: Annotated[int, Field(..., description="Total document count")]
    status: Annotated[str, Field(..., description="Collection status")]


# ============== Query Schemas ==============


class QueryRequest(BaseModel):
    """Request for RAG query."""

    question: Annotated[str, Field(
        ...,
        description="Question to ask",
        min_length=1,
        max_length=1000,
    )]
    include_sources: Annotated[bool, Field(
        default=True,
        description="Include source documents in response",
    )]
    enable_evaluation: Annotated[bool, Field(
        default=False,
        description="Enable RAGAS evaluation (faithfulness, answer relevancy)",
    )]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is RAG?",
                    "include_sources": True,
                    "enable_evaluation": False,
                }
            ]
        }
    }


class SourceDocument(BaseModel):
    """Source document information."""

    content: Annotated[str, Field(..., description="Document content excerpt")]
    metadata: Annotated[dict[str, Any], Field(..., description="Document metadata")]


class EvaluationScores(BaseModel):
    """RAGAS evaluation scores."""

    faithfulness: Annotated[float | None, Field(
        None,
        description="Faithfulness score (0-1): measures factual consistency with sources",
        ge=0.0,
        le=1.0,
    )]
    answer_relevancy: Annotated[float | None, Field(
        None,
        description="Answer relevancy score (0-1): measures relevance to question",
        ge=0.0,
        le=1.0,
    )]
    evaluation_time_ms: Annotated[float | None, Field(
        None,
        description="Time taken for evaluation in milliseconds",
    )]
    error: Annotated[str | None, Field(
        None,
        description="Error message if evaluation failed",
    )]


class QueryResponse(BaseModel):
    """Response for RAG query."""

    question: Annotated[str, Field(..., description="Original question")]
    answer: Annotated[str, Field(..., description="Generated answer")]
    sources: Annotated[list[SourceDocument] | None, Field(
        None,
        description="Source documents used",
    )]
    processing_time_ms: Annotated[float, Field(
        ...,
        description="Query processing time in milliseconds",
    )]
    evaluation: Annotated[EvaluationScores | None, Field(
        None,
        description="RAGAS evaluation scores (if requested)",
    )]


# ============== Error Schemas ==============


class ErrorResponse(BaseModel):
    """Error response."""

    error: Annotated[str, Field(..., description="Error type")]
    message: Annotated[str, Field(..., description="Error message")]
    detail: Annotated[str | None, Field(None, description="Detailed error information")]


class ValidationErrorResponse(BaseModel):
    """Validation error response."""

    error: Annotated[str, Field(default="Validation Error", description="Error type")]
    message: Annotated[str, Field(..., description="Error message")]
    errors: Annotated[list[dict], Field(..., description="Validation errors")]