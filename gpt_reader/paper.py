from PyPDF2 import PdfReader

class Paper(object):

    def __init__(self, pdf_obj: PdfReader) -> None:
        self._pdf_obj = pdf_obj
        self._paper_meta = self._pdf_obj.metadata

    def iter_pages(self, iter_text_len: int = 3000):
        page_idx = 0
        for page in self._pdf_obj.pages:
            txt = page.extract_text()
            for i in range((len(txt) // iter_text_len) + 1):
                yield page_idx, i, txt[i * iter_text_len:(i + 1) * iter_text_len]
            page_idx += 1


if __name__ == '__main__':
    reader = PdfReader('../alexnet.pdf')
    paper = Paper(reader)
