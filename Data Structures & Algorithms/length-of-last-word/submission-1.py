class Solution:
    def lengthOfLastWord(self, s: str) -> int:        
        return len(s.strip().split(" ")[-1])

    def lengthOfLastWordLoop(self, s: str) -> int:
        ans: int = 0

        for i in range(len(s)-1, -1, -1):
            if s[i] != " ":
                ans += 1
            else:
                if ans > 0: return ans
        
        return ans