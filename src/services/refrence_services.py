from repositories.reference_repository import ReferenceRepository


class ReferenceServices:
    def __init__(self, reference_repository: ReferenceRepository) -> None:
        self._reference_repository = reference_repository

    def create_reference(self, reference):
        # Tehdään tarvittavat validoinnit user inputeille
        # Tallennetaan lähde käyttäen reference repositorya
        self._reference_repository.save(reference)
