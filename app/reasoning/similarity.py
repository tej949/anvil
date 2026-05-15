from difflib import SequenceMatcher


class SimilarityEngine:

    def compare(
        self,
        fp1,
        fp2
    ):

        seq1 = fp1["sequence"]
        seq2 = fp2["sequence"]

        return SequenceMatcher(
            None,
            seq1,
            seq2
        ).ratio()