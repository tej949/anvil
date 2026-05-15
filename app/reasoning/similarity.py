from difflib import SequenceMatcher


class SimilarityEngine:

    def compare(
        self,
        fp1,
        fp2
    ):

        seq1 = fp1["sequence"]
        seq2 = fp2["sequence"]

        # exact sequence ordering
        sequence_score = (
            SequenceMatcher(
                None,
                seq1,
                seq2
            ).ratio()
        )

        # shared token overlap
        overlap = len(
            set(seq1) & set(seq2)
        )

        overlap_score = (
            overlap /
            max(len(set(seq1)), 1)
        )

        # service overlap
        service_overlap = len(
            set(fp1["services"])
            &
            set(fp2["services"])
        )

        service_score = min(
            service_overlap,
            1.0
        )

        # weighted final score
        final_score = (
            sequence_score * 0.6
            +
            overlap_score * 0.3
            +
            service_score * 0.1
        )

        return round(final_score, 4)