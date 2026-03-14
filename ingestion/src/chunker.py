import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from .filters import extract_filter_names
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def generate_chunks_for_file(pdf_file: str, rel_path: str) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks: list[Document] = []  # ← explicit type hint

    try:
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()

        if not pages:
            print(f"  Warning: No pages extracted from {rel_path}")
            return chunks

        for page_num, page in enumerate(pages, 1):
            split_texts = text_splitter.split_text(page.page_content)

            for chunk_idx, chunk_text in enumerate(split_texts):
                filters = extract_filter_names(chunk_text)

                chunk_id = f"{os.path.basename(pdf_file)}_p{page_num}_c{chunk_idx}"

                # MUST create Document object here — this is the fix
                doc = Document(
                    page_content=chunk_text,
                    metadata={
                        "source": rel_path,
                        "filename": os.path.basename(pdf_file),
                        "page": page.metadata.get("page", page_num),
                        "chunk_id": chunk_id,
                        "filter_names": filters,
                        "report_type": os.path.splitext(os.path.basename(pdf_file))[0]
                    }
                )
                chunks.append(doc)  # ← append Document, NOT string

        print(f"  → Generated {len(chunks)} chunks for {rel_path}")

    except Exception as e:
        print(f"    Error processing {rel_path}: {str(e)}")

    return chunks