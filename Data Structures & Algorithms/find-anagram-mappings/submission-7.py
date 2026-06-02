from collections import defaultdict, deque

class Solution:
    def anagramMappings(self, nums1: list[int], nums2: list[int]) -> list[int]:
        # Build a map: value -> deque of indeces
        pos: defaultdict[int, deque[int]] = defaultdict(deque)
        for i, val in enumerate(nums2):
            pos[val].append(i)

        mapping: list[int] = [0]*len(nums1)

        for i, val in enumerate(nums1):
            mapping[i] = pos[val].popleft()

        return mapping