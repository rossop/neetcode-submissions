class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        N: int = len(nums)
        ans: list[int] = [1] * N
        for i in range(N):
            for j,n in enumerate(nums):
                if j != i:
                    ans[i] *= n
        return ans


        