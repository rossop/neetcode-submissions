class Solution:
    def maxArea(self, heights: list[int]) -> int:
        # O(n)
        res: int = 0
        l, r = 0, len(heights) - 1

        while l < r:
            area = (r-l)*min(heights[l],heights[r])
            res = max(res, area)

            if heights[l] > heights[r]:
                r -= 1
            elif heights[l] < heights[r]:
                l += 1
            elif heights[l] == heights[r]:
                if heights[l+1] > heights[r-1]:
                    l += 1
                else:
                    r -= 1
              
        return res

    def maxAreaBruteForce(self, heights: list[int]) -> int:
        # BRUTE FORCE
        res: int = 0

        for l in range(len(heights)):
            for r in range(l+1, len(heights)):
                area = (r-l)*min(heights[l],heights[r])
                res = max(res, area)

        return res

        