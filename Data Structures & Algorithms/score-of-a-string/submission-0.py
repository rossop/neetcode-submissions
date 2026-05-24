class Solution:
    def scoreOfString(self, s: str) -> int:
        S: int = len(s)
        ans: int = 0
        for i in range(S-1):
            ans += abs(ord(s[i+1]) - ord(s[i]))
        return ans

        