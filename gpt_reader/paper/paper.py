from PyPDF2 import PdfReader
import tiktoken


class Paper(object):

    def __init__(self, paper_path) -> None:
        self.pdf_path = paper_path
        self.pdf_obj = PdfReader(paper_path)
        self.paper_meta = self.pdf_obj.metadata
        self.catelogue = None
        self.text = ''
        for page in self.pdf_obj.pages:
            txt = page.extract_text()
            self.text += txt

        self.paper_parts = None
        self.paper_summaries = [('PaperMeta', str(self.paper_meta))]

    def has_catelogue(self):
        return self.catelogue is not None

    def set_catelogue(self, catelogue_list):
        self.catelogue = catelogue_list

    def iter_pages(self, iter_text_len: int = 3000):
        page_idx = 0
        for page in self.pdf_obj.pages:
            txt = page.extract_text()
            for i in range((len(txt) // iter_text_len) + 1):
                yield page_idx, i, txt[i * iter_text_len:(i + 1) * iter_text_len]
            page_idx += 1

    def split_paper_by_titles(self):

        if self.catelogue is None:
            raise RuntimeError('catelogue is None, not initialized')

        text_str = self.text
        titles = self.catelogue
        title_positions = []
        for title in titles:
            position = text_str.find(title)
            if position != -1:
                title_positions.append((position, title))

        title_positions.sort()

        paper_parts = []
        for i, (position, title) in enumerate(title_positions):
            start_pos = position
            end_pos = title_positions[i+1][0] if i < len(title_positions) - 1 else len(text_str)
            paper_part = text_str[start_pos:end_pos].strip()
            paper_parts.append((title, paper_part))

        self.paper_parts = paper_parts

    def compute_part_tokens(self, model='gpt-3.5-turbo'):

        enc = tiktoken.encoding_for_model(model)
        rs = []
        if self.paper_parts is not None:
            for i in self.paper_parts:
                rs.append((i[0], len(enc.encode(i[1]))))

        return rs
    