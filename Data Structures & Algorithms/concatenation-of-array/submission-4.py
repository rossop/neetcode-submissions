class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans: list[int] = [0] * 2 * n
        for i, v in enumerate(nums):
            ans[i] = v
            ans[i+n] = v

        return ans