from difflib import SequenceMatcher


class SimilarityEngine:

    def compare(
        self,
        fp1,
        fp2
    ):

        seq1 = fp1["sequence"]
        seq2 = fp2["sequence"]

        # sequence ordering similarity
        sequence_score = (
            SequenceMatcher(
                None,
                seq1,
                seq2
            ).ratio()
        )

        # token overlap similarity
        overlap = len(
            set(seq1) & set(seq2)
        )

        overlap_score = (
            overlap /
            max(len(set(seq1)), 1)
        )

        # service continuity
        service_overlap = len(
            set(fp1["services"])
            &
            set(fp2["services"])
        )

        service_score = min(
            service_overlap,
            1.0
        )

        # weighted final similarity
        final_score = (
            sequence_score * 0.70
            +
            overlap_score * 0.25
            +
            service_score * 0.05
        )

        return round(final_score, 4)