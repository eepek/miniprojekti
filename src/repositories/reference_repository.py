from entities.reference import Inproceedings


class ReferenceRepository:
    def __init__(self):
        self._references = []
        self.init_references()

    def init_references(self):
        with open(
                "./data/references.bib", "r", encoding="utf-8") as references_data:
            print(references_data)
            # for line in references_data:
            #     # if line[0] == "@":
            #     #     new_reference = dict()
            #     #     key = line[(line.find("{") + 1): (len(line) - 2)]
            #     #     new_reference
            #     #     continue

    def save(self, reference: Inproceedings):
        self._references.append(reference)
        # ja tässä sitten kirjoitetaan ulkoiseen tiedostoon sama
        # eli str(reference) kirjoitetaan tiedoston loppuun
        with open("./data/references.bib", "a", encoding="utf-8") as references_data:
            references_data.write("\n\n" + str(reference))

    def load_all(self):
        return self._references
