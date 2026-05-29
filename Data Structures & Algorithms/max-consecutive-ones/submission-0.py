class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        L: int = 0
        ans: int = 0

        for i in nums:
            if i == 1:
                L += 1
            elif i == 0:
                ans = max(ans, L)
                L = 0
        return max(ans, L)