class PostProcessingService:

    def post_process_ocr(self, ocr_result):
        try:
            pages_text = []
            for page in ocr_result['pages']:
                blocks = self.extract_text_blocks(page['blocks'])
                sorted_blocks = self.sort_blocks(blocks)
                page_text = self.concatenate_blocks(sorted_blocks)
                pages_text.append(page_text)

            return "\n\n".join(pages_text)
        except Exception as e:
            raise ValueError(f"Error during post-processing: {e}")

    def extract_text_blocks(self, blocks):
        text_blocks = []
        for block in blocks:
            for line in block['lines']:
                line_text = " ".join([word['value'] for word in line['words']])
                text_blocks.append({
                    'text': line_text,
                    'top': line['geometry'][0][1],   # y-coordinate of the top edge
                    'left': line['geometry'][0][0]   # x-coordinate of the left edge
                })
        return text_blocks

    def sort_blocks(self, blocks):
        return sorted(blocks, key=lambda x: (x['top'], x['left']))

    def concatenate_blocks(self, blocks):
        return "\n".join([block['text'] for block in blocks])