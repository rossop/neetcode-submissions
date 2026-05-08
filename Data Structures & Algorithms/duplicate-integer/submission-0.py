from collections import Counter

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        return not Counter(nums) == Counter(set(nums))
         