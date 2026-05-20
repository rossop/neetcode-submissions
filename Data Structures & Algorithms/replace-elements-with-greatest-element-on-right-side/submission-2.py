class Solution:
    def replaceElements(self, arr: list[int]) -> list[int]:
        rightMax: int = -1
        
        for i in range(len(arr) - 1, -1, -1):
            newMax: int = max(rightMax, arr[i])
            arr[i] = rightMax
            rightMax = newMax
        return arr