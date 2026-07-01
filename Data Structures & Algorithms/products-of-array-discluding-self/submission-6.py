class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        prefix: int = 1
        N: int = len(nums)
        ans: list[int] = [1] * N
        for i in range(N):
            ans[i] = prefix
            prefix *= nums[i]
        
        postfix: int = 1
        for i in range(N-1, -1, -1):
            ans[i] *= postfix
            postfix *= nums[i]

        return ans

    def productExceptSelfNested(self, nums: list[int]) -> list[int]:
        N: int = len(nums)
        ans: list[int] = [1] * N
        for i in range(N):
            for j,n in enumerate(nums):
                if j != i:
                    ans[i] *= n
        return ans


        