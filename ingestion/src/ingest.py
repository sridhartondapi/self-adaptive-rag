import os
import glob
from pathlib import Path
from .config import DOCUMENT_DIR, HASH_FILE, S3_PATH, S3_BUCKET
from .hash_store import get_file_hash, load_previous_hashes, save_hashes
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document
from .chunker import generate_chunks_for_file
from .vectorstore import get_chroma_client
from .loader_to_s3 import upload_chroma_to_s3, upload_hash_file_to_s3

def update_vectorstore():
    print("Starting ingestion pipeline...")
    previous_hashes = load_previous_hashes(HASH_FILE)

    current_files = sorted(glob.glob(os.path.join(DOCUMENT_DIR,"**/*.pdf"), recursive=True))
    current_rel_path = [os.path.relpath(f, DOCUMENT_DIR) for f in current_files]
    current_hashes = {rel:get_file_hash(os.path.join(DOCUMENT_DIR, rel)) for rel in current_rel_path}

    if not current_files:
        print ("No PDF files found.")
        return 
    vectorstore = get_chroma_client()

    deleted_count = 0
    for prev_rel in list(previous_hashes.keys()):
        if prev_rel not in current_hashes:
            print (f"Deleting removed files here: {prev_rel}")

            results = vectorstore.get(where={"source": prev_rel})
            if results['ids']:
                vectorstore.delete(ids=results['ids'])
                deleted_count += len(results['ids'])
            del previous_hashes[prev_rel]

    new_or_changed_count = 0
    new_chunks = []
    for rel_path, curr_hash in current_hashes.items():
        is_changed = rel_path in previous_hashes and previous_hashes[rel_path] != curr_hash
        is_new = rel_path not in previous_hashes

        if is_new or is_changed:
            new_or_changed_count += 1

        if is_changed:
            results = vectorstore.get(where={"source": rel_path})
            if results['ids']:
                vectorstore.delete(ids=results['ids'])

        full_path = os.path.join(DOCUMENT_DIR, rel_path)
        chunks = generate_chunks_for_file(full_path, rel_path)
        new_chunks.extend(chunks)

        previous_hashes[rel_path] = curr_hash

    if new_chunks:
        print(f"\nAdding {len(new_chunks)} new/updated chunks...")


        filtered_chunks = []
        for item in new_chunks:
            # Safety check: ensure it's a Document
            if not isinstance(item, Document):
                print(f"Skipping invalid chunk type: {type(item)}")
                continue

            # Force-remove lists from metadata
            safe_metadata = {}
            for key, value in item.metadata.items():
                if isinstance(value, (str, int, float, bool, type(None))):
                    safe_metadata[key] = value
                elif isinstance(value, list):
                    # Convert list to comma-separated string (or skip)
                    safe_metadata[key] = ",".join(str(v) for v in value if v is not None)
                else:
                    # Skip other complex types
                    print(f"Skipping complex metadata key '{key}': {type(value)}")

            filtered_doc = Document(
                page_content=item.page_content,
                metadata=safe_metadata
            )
            filtered_chunks.append(filtered_doc)

        if not filtered_chunks:
            print("No valid chunks after filtering - skipping add")
        else:
            chunk_ids = []
            for doc in filtered_chunks:
                chunk_id = doc.metadata.get("chunk_id")
                if chunk_id:
                    chunk_ids.append(chunk_id)
                else:
                    print("Warning: Chunk missing chunk_id - generating fallback")
                    chunk_ids.append(f"fallback_{len(chunk_ids)}")

            try:
                vectorstore.add_documents(filtered_chunks)
                print("Successfully added chunks to Chroma!")
                count_after = vectorstore._collection.count()
                print (f"vectorstore now actually contains {count_after} items.")
            except Exception as e:
                print(f"Final add failed: {e}")

        # Always save hashes, even if add failed
        save_hashes(previous_hashes, HASH_FILE)

        if S3_PATH:
            print ("\nUploading the Chroma db to S3.....")
            upload_chroma_to_s3(S3_BUCKET)
            print ("upload to S3 completed.....")
            upload_hash_file_to_s3()
        else:
            print ("VECTORSTORE not set, upload to S3 skipped")

    print (f"\nSummary:")
    print (f" - New/Changed Files: {new_or_changed_count}")
    print (f" - Chunks deleted: {deleted_count}")
    print (f" - Chunks are added/updated: {len(new_chunks)}")
    print (" Update Complete")



