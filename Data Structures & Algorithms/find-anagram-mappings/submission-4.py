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

    def anagramMappingsMap(self, nums1: list[int], nums2: list[int]) -> list[int]:
        '''
        Does not account for duplication
        Time: O(n)
        Space: O(n)
        '''
        myMap: dict[int, int] = {}

        for i in range(len(nums2)):
            myMap[nums2[i]] = i

        result: list[int] = [0] * len(nums1)

        for i in range(len(nums1)):
            result[i] = myMap[nums1[i]]

        return result

    def anagramMappingsNested(self, nums1: List[int], nums2: List[int]) -> List[int]:
        '''
        Does not account for duplication
        Time: O(n^2)
        Space: O(1)
        '''
        N: int = len(nums1)
        mappings: list[int] = [0]*N

        for i, n1 in enumerate(nums1):
            for j, n2 in enumerate(nums2):
                if n1 == n2:
                    mappings[i] = j
                    break
        
        return mappings