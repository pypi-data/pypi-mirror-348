from typing import List

from .utils import Utils


class Split:
    def __init__(self, api_key: str = None):
        """
        Initializes the Split object with default or user-defined thresholds.
        """
        self.utils = Utils(api_key=api_key)

    def _split_large_chunk(self, paragraphs: List[str], embeddings: List[List[float]]) -> (List[str], List[str]):
        """
        Splits 'paragraphs' by finding the least similar boundary using 'embeddings'
        (which are precomputed for these paragraphs only). Returns (left_part, right_part).
        """
        # If there are 0 or 1 paragraphs, no need to split
        if len(paragraphs) < 2:
            return paragraphs, []

        # We'll assume 'embeddings' is already the same length as 'paragraphs'.
        if len(embeddings) < 2:
            # Can't compute consecutive similarities with fewer than 2 embeddings
            return paragraphs, []

        # Find the least similar consecutive boundary
        split_index = self.utils.get_consecutive_least_similar(embeddings)

        left_part = paragraphs[:split_index + 1]
        right_part = paragraphs[split_index + 1:]
        return left_part, right_part

    def split(
        self,
        extracted_text: str,
        min_chunk_size: int = 4000,
        max_chunk_size: int = 7000
    ) -> List[str]:
        """
        Splits the input text into chunks of token-size between [min_chunk_size, max_chunk_size].
        Once a chunk is in that range, we find the "least similar" boundary, store the left side,
        and re-insert the right side for further splitting.
        """
        paragraphs = [p.strip() for p in extracted_text.split("\n\n") if p.strip()]
        if not paragraphs:
            return []

        # Precompute once
        paragraphs_tokens = [self.utils.count_tokens(p) for p in paragraphs]
        paragraphs_embeddings = self.utils.list_embeddings(paragraphs)

        final_chunks = []
        idx = 0
        n = len(paragraphs)

        while idx < n:
            chunk_paragraphs = []
            chunk_embeddings = []
            chunk_tokens = []  # Keep track of tokens in this chunk
            current_tokens = 0

            # 1) Accumulate until we at least exceed min_chunk_size or run out
            while idx < n and current_tokens < min_chunk_size:
                if current_tokens + paragraphs_tokens[idx] <= max_chunk_size:
                    chunk_paragraphs.append(paragraphs[idx])
                    chunk_embeddings.append(paragraphs_embeddings[idx])
                    chunk_tokens.append(paragraphs_tokens[idx])
                    current_tokens += paragraphs_tokens[idx]
                    idx += 1
                else:
                    # This paragraph alone might exceed max_chunk_size -> handle as you see fit
                    break

            # If we haven't hit min_chunk_size but are out of paragraphs, store remainder and quit
            if current_tokens < min_chunk_size and idx >= n:
                if chunk_paragraphs:
                    final_chunks.append(" ".join(chunk_paragraphs))
                break

            # 2) Keep adding while we're under max_chunk_size
            while idx < n:
                if current_tokens + paragraphs_tokens[idx] <= max_chunk_size:
                    chunk_paragraphs.append(paragraphs[idx])
                    chunk_embeddings.append(paragraphs_embeddings[idx])
                    chunk_tokens.append(paragraphs_tokens[idx])
                    current_tokens += paragraphs_tokens[idx]
                    idx += 1
                else:
                    break

            # Now we have between min_chunk_size and max_chunk_size tokens in 'chunk_paragraphs'
            if chunk_paragraphs:
                # 3) Split at the "least similar" boundary
                left_part, right_part = self._split_large_chunk(
                    chunk_paragraphs, chunk_embeddings
                )

                # We'll figure out how many paragraphs ended up in the left part
                used_count = len(left_part)
                leftover_count = len(right_part)

                # Store left side
                final_chunks.append(" ".join(left_part))

                # If there's leftover, reinsert it into the main lists
                if leftover_count > 0:
                    # Slices for leftover
                    leftover_embeddings = chunk_embeddings[used_count:]
                    leftover_tokens = chunk_tokens[used_count:]

                    # Re-insert them at index=idx
                    paragraphs[idx:idx] = right_part
                    paragraphs_embeddings[idx:idx] = leftover_embeddings
                    paragraphs_tokens[idx:idx] = leftover_tokens

                    # Recompute n, in case the paragraphs list has grown
                    n = len(paragraphs)

        return final_chunks