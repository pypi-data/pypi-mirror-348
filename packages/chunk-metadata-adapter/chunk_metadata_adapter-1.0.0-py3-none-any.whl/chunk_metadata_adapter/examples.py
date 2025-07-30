"""
Examples of how to use the Chunk Metadata Adapter.

This module contains practical examples for various use cases.
"""
import uuid

from chunk_metadata_adapter import (
    ChunkMetadataBuilder,
    SemanticChunk,
    FlatSemanticChunk,
    ChunkType,
    ChunkRole,
    ChunkStatus
)


def example_basic_flat_metadata():
    """Example of creating basic flat metadata for a chunk."""
    # Create a builder instance for a specific project
    builder = ChunkMetadataBuilder(project="MyProject", unit_id="chunker-service-1")
    
    # Generate UUID for the source document
    source_id = str(uuid.uuid4())
    
    # Create metadata for a piece of code
    metadata = builder.build_flat_metadata(
        text="def hello_world():\n    print('Hello, World!')",
        source_id=source_id,
        ordinal=1,  # First chunk in the document
        type=ChunkType.CODE_BLOCK,  # Using enum
        language="python",
        source_path="src/hello.py",
        source_lines_start=10,
        source_lines_end=12,
        tags="example,hello",
        role=ChunkRole.DEVELOPER
    )
    
    # Access the metadata
    print(f"Generated UUID: {metadata['uuid']}")
    print(f"SHA256: {metadata['sha256']}")
    print(f"Created at: {metadata['created_at']}")
    
    return metadata


def example_structured_chunk():
    """Example of creating a structured SemanticChunk instance."""
    # Create a builder for a project with task
    builder = ChunkMetadataBuilder(
        project="DocumentationProject",
        unit_id="docs-generator"
    )
    
    # Generate a source document ID
    source_id = str(uuid.uuid4())
    
    # Create a structured chunk 
    chunk = builder.build_semantic_chunk(
        text="# Introduction\n\nThis is the documentation for the system.",
        language="markdown",
        type=ChunkType.DOC_BLOCK,
        source_id=source_id,
        summary="Project introduction section",
        role=ChunkRole.DEVELOPER,
        source_path="docs/intro.md",
        source_lines=[1, 3],
        ordinal=0,
        task_id="DOC-123",
        subtask_id="DOC-123-A",
        tags=["introduction", "documentation", "overview"],
        links=[f"parent:{str(uuid.uuid4())}"]
    )
    
    # Access the data
    print(f"Chunk UUID: {chunk.uuid}")
    print(f"Content summary: {chunk.summary}")
    print(f"Links: {chunk.links}")
    
    return chunk


def example_conversion_between_formats():
    """Example of converting between structured and flat formats."""
    # Create a builder instance
    builder = ChunkMetadataBuilder(project="ConversionExample")
    
    # Start with a structured chunk
    structured_chunk = builder.build_semantic_chunk(
        text="This is a sample chunk for conversion demonstration.",
        language="text",
        type=ChunkType.COMMENT,
        source_id=str(uuid.uuid4()),
        role=ChunkRole.REVIEWER
    )
    
    # Convert to flat dictionary
    flat_dict = builder.semantic_to_flat(structured_chunk)
    print(f"Flat representation has {len(flat_dict)} fields")
    
    # Convert back to structured format
    restored_chunk = builder.flat_to_semantic(flat_dict)
    print(f"Restored structured chunk: {restored_chunk.uuid}")
    
    # Verify they're equivalent
    assert restored_chunk.uuid == structured_chunk.uuid
    assert restored_chunk.text == structured_chunk.text
    assert restored_chunk.type == structured_chunk.type
    
    return {
        "original": structured_chunk,
        "flat": flat_dict,
        "restored": restored_chunk
    }


def example_chain_processing():
    """Example of a chain of processing for document chunks."""
    # Create a document with multiple chunks
    builder = ChunkMetadataBuilder(project="ChainExample", unit_id="processor")
    source_id = str(uuid.uuid4())
    
    # Create a sequence of chunks from a document
    chunks = []
    for i, text in enumerate([
        "# Document Title",
        "## Section 1\n\nThis is the content of section 1.",
        "## Section 2\n\nThis is the content of section 2.",
        "## Conclusion\n\nFinal thoughts on the topic."
    ]):
        chunk = builder.build_semantic_chunk(
            text=text,
            language="markdown",
            type=ChunkType.DOC_BLOCK,
            source_id=source_id,
            ordinal=i,
            summary=f"Section {i}" if i > 0 else "Title"
        )
        chunks.append(chunk)
    
    # Create explicit links between chunks (parent-child relationships)
    for i in range(1, len(chunks)):
        # Add parent link to the title chunk
        chunks[i].links.append(f"parent:{chunks[0].uuid}")
        # Update status to show progress
        chunks[i].status = ChunkStatus.INDEXED
    
    # Simulate processing and updating metrics
    for chunk in chunks:
        # Update metrics based on some processing
        chunk.metrics.quality_score = 0.95
        chunk.metrics.used_in_generation = True
        chunk.metrics.matches = 3
        
        # Add feedback
        chunk.metrics.feedback.accepted = 2
        
    # Print the processed chain
    print(f"Processed {len(chunks)} chunks from source {source_id}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk.summary} - Status: {chunk.status.value}")
    
    return chunks


if __name__ == "__main__":
    print("Running examples...")
    example_basic_flat_metadata()
    example_structured_chunk()
    example_conversion_between_formats()
    example_chain_processing()
    print("All examples completed.") 