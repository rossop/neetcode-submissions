class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        return sorted(s) == sorted(t)

    def isAnagramCounter(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)