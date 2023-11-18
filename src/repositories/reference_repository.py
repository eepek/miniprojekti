from entities.reference import Inproceedings


class ReferenceRepository:
    def __init__(self):
        self._references = []

    def save(self, reference: Inproceedings):
        self._references.append(reference)
        # ja tässä sitten kirjoitetaan ulkoiseen tiedostoon sama
        # eli str(reference) kirjoitetaan tiedoston loppuun

    def load_all(self):
        return self._references
