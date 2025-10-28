from pypdf import PdfReader
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_pdf(file_path: str) -> str:
 
    try:
        reader = PdfReader(file_path)
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        logger.info(f"✅ Loaded PDF: {file_path}")
        logger.info(f"   Pages: {len(reader.pages)}")
        logger.info(f"   Characters: {len(text):,}")
        
        return text
    
    except Exception as e:
        logger.error(f"❌ Error loading PDF: {e}")
        raise


def load_multiple_pdfs(file_paths: List[str]) -> List[Dict[str, str]]:

    documents = []
    
    for path in file_paths:
        try:
            text = load_pdf(path)
            documents.append({
                'filename': path.split('/')[-1].split('\\')[-1],  # Handle both / and \
                'content': text
            })
        except Exception as e:
            logger.warning(f"⚠️  Skipped {path}: {e}")
    
    logger.info(f"✅ Loaded {len(documents)} documents")
    return documents