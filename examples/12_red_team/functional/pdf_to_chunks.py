from dataclasses import dataclass
from pathlib import Path

import yaml

try:
    import pymupdf4llm
except ImportError:
    print(
        "pymupdf4llm is not installed. Please install it with 'uv pip install pymupdf4llm'"
    )
    exit(1)

try:
    from langchain_text_splitters import (
        MarkdownHeaderTextSplitter,
        RecursiveCharacterTextSplitter,
    )
except ImportError:
    print(
        "langchain_text_splitters is not installed. Please install it with 'uv pip install langchain-text-splitters'"
    )
    exit(1)


@dataclass
class Chunk:
    content: str
    metadata: dict
    source_file: str
    chunk_index: int


def pdf_to_markdown(pdf_path: str | Path) -> str:
    return pymupdf4llm.to_markdown(str(pdf_path))


def chunk_markdown(
    markdown_text: str,
    source_file: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[Chunk]:
    headers_to_split_on = [
        ("#", "header_1"),
        ("##", "header_2"),
        ("###", "header_3"),
        ("####", "header_4"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )
    header_splits = markdown_splitter.split_text(markdown_text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    final_splits = text_splitter.split_documents(header_splits)

    chunks = []
    for i, split in enumerate(final_splits):
        chunks.append(
            Chunk(
                content=split.page_content,
                metadata=split.metadata,
                source_file=source_file,
                chunk_index=i,
            )
        )

    return chunks


def process_pdf_folder(
    folder_path: str | Path,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    output_markdown: bool = False,
) -> dict[str, list[Chunk]]:
    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))

    results: dict[str, list[Chunk]] = {}

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        markdown_content = pdf_to_markdown(pdf_file)

        if output_markdown:
            md_output_path = folder / f"{pdf_file.stem}.md"
            md_output_path.write_text(markdown_content, encoding="utf-8")
            print(f"  Saved markdown: {md_output_path.name}")

        chunks = chunk_markdown(
            markdown_content,
            source_file=pdf_file.name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        results[pdf_file.name] = chunks
        print(f"  Created {len(chunks)} chunks")

    return results


def save_chunks_to_yaml(chunks: list[Chunk], output_path: str | Path) -> None:
    data = [{"chunk": chunk.content} for chunk in chunks]
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def main():
    pdf_folder = Path(__file__).parent / "pdfs"
    output_yaml = Path(__file__).parent / "document_chunks.yaml"

    results = process_pdf_folder(
        folder_path=pdf_folder,
        chunk_size=1000,
        chunk_overlap=200,
        output_markdown=True,
    )

    all_chunks = []
    for chunks in results.values():
        all_chunks.extend(chunks)

    save_chunks_to_yaml(all_chunks, output_yaml)
    print(f"Saved {len(all_chunks)} chunks to {output_yaml}")

    return results


if __name__ == "__main__":
    main()
