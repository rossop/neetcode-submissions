class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        R, C = len(matrix), len(matrix[0])
        l, r = 0, R * C - 1
        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // C][mid % C]
            if val < target:
                l = mid + 1
            elif val > target:
                r = mid - 1
            else:
                return True
        return False