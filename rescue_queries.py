"""MongoDB queries derived from the Dashboard Specifications table."""
import re

PROFILES = {
    "water": (["Labrador Retriever", "Chesapeake Bay Retriever", "Newfoundland"], "Intact Female", 26, 156),
    "mountain": (["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"], "Intact Male", 26, 156),
    "disaster": (["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"], "Intact Male", 20, 300),
}


def rescue_query(rescue_type):
    """Include named breeds and mixes; apply inclusive age bounds in weeks.

    Breed components are slash separated in AAC records. Labrador Retriever Mix
    is required for water rescue; the other preferred breeds include mixes.
    """
    if rescue_type == "reset":
        return {}
    breeds, sex, low, high = PROFILES[rescue_type]
    patterns = []
    for breed in breeds:
        suffix = r" Mix" if rescue_type == "water" and breed == "Labrador Retriever" else r"(?: Mix)?"
        patterns.append(r"(?:^|/)" + re.escape(breed) + suffix + r"(?:/|$)")
    return {"animal_type": "Dog", "breed": {"$regex": "|".join(patterns), "$options": "i"},
            "sex_upon_outcome": sex,
            "age_upon_outcome_in_weeks": {"$gte": low, "$lte": high}}
