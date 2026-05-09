class Solution:

    def encode(self, strs: List[str]) -> str:
        sep: str = '#'
        res: str = ''

        for s in strs:
            res += str(len(s))
            res += sep
            res += s
        
        return res 

    def decode(self, s: str) -> List[str]:
        sep: str = '#'
        res, i = [], 0

        while i < len(s):
            j = i
            while s[j] != sep:
                j += 1
            length = int(s[i:j])
            res.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return res