from gliner import GLiNER
from .utils import detect_pii, redact_document

class Scanner():
    def __init__(self, 
                 model=gliner_model, 
                 pii_types=['Person', 'Location', 'Date', 'Email', 'Phone number']):
        self.pii_types = pii_types
        self.model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

    def redact_pii(self, 
                   document):
        labels = detect_pii(self.model, document, self.pii_types)
        redacted_document, labels = redact_document(document, labels)
        return redacted_document, labels