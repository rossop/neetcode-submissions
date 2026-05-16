class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def calcRate(piles: list[int], k: int) -> int:
            return sum([(x+k-1)//k for x in piles])
        
        left, right = 1, max(piles)
        res = right

        while left <= right:
            k: int = left + (right - left) // 2
            if calcRate(piles, k) <= h:
                res = k
                right = k - 1
            else:
                left = k + 1
        return res
    
    def minEatingSpeedBruteForce(self, piles: list[int], h: int) -> int:
        def calcRate(piles: list[int], k: int) -> int:
            return sum([(x+k-1)//k for x in piles])
        
        k_min, k_max = 1, max(piles)
        for k in range(k_min, k_max+1):
            if calcRate(piles, k) <= h:
                return k
        
        return -1
        