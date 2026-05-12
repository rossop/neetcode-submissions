class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            m: int = (l + r) // 2 
            # m: int = l + ((r - l) // 2) 
            # will work on very large nums avoding overflow 
            # when l + r would lead to it
            if nums[m] > target:
                r = m - 1
            elif nums[m] < target:
                l = m + 1
            else:
                return m


        return -1