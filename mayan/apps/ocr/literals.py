DEFAULT_OCR_AUTO_OCR = True
DEFAULT_OCR_BACKEND = 'mayan.apps.ocr.backends.tesseract.Tesseract'
DEFAULT_OCR_BACKEND_ARGUMENTS = {
    'environment': {'OMP_THREAD_LIMIT': '1'}
}

ERROR_LOG_DOMAIN_NAME = 'ocr'

TASK_DOCUMENT_VERSION_PAGE_OCR_TIMEOUT = 10 * 60  # 10 Minutes per page
