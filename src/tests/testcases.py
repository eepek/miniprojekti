from entities.reference import Reference
from repositories.reference_repository import ReferenceType


INPRO_VALID1 = Reference(ReferenceType.INPROCEEDINGS, "Garcia23", {
    "title": "Machine Learning Approaches for Medical Image Analysis}",
    "author": "Garcia, Maria and Kim, Chang",
    "booktitle": "Proceedings of the International Conference on Machine Learning",
    "year": 2023,
    "editor": "Emily White and Michael Davis",
    "volume": 3,
    "pages": "87-94",
    "address": "San Francisco, CA",
    "month": "September",
    "note": "New approach"
})

INPRO_VALID2 = Reference(ReferenceType.INPROCEEDINGS, "Jonessen23", {
    "title": "Exploring Patterns in Data Analysis",
    "author": "Jonessen, Michael and Williams, Emily",
    "booktitle": "Proceedings of the International Conference on Data Science",
    "year": 2023,
    "editor": "Alex Johnson and Laura White",
    "volume": 2,
    "series": "Conference Proceedings",
    "pages": "45--52",
    "address": "San Francisco, CA",
    "month": "September",
    "note": "Best Paper Award",
})

INPRO_SOME_FIELDS = Reference(ReferenceType.INPROCEEDINGS, "Boser92", {
    "title": "A training algorithm for optimal margin classifiers",
    "author": "Boser, Bernhard E and Guyon, Isabelle M and Vapnik, Vladimir N",
    "booktitle": "Proceedings of the fifth annual workshop on Computational learning theory",
    "year": 1992,
    "note": "important paper"
})

TECHREPORT_VALID = Reference(ReferenceType.TECHREPORT, "Jones11", {
    "title": "Advancements in Network Security Protocols",
    "author": "Jones, David",
    "institution": "Institute for Secure Networks",
    "year": 2011,
    "type": "Technical Report",
    "number": 2,
    "month": "November",
    "note": "Exploring the evolving landscape of network security",
    "annote": "Internal Use Only",
})

ARTICLE_VALID = Reference(ReferenceType.ARTICLE, "Johnson24", {
    "title": "Predictive Power of Financial Indicators in Assessing Corporate Performance",
    "author": "Emily R. Johnson",
    "journal": "Journal of Financial Analysis",
    "year": 2024,
    "volume": 25,
    "number": 2,
    "pages": "78--102",
    "month": "March",
    "note": "DOI: 10.1234/jfa.2024.5678}",
})

PHD_VALID = Reference(ReferenceType.PHD, "Miller20", {
    "author": "Emma R. Miller",
    "title": "Innovations in Natural Language Processing",
    "school": "Department of Computer Science, University of Technovate",
    "year": 2020,
    "type": "Doctoral Dissertation",
    "address": "Cityville, Techland",
    "month": "September",
    "note": "Supervised by Prof. Alex J. Robertson",
})
