class Solution:
    def validWordSquare(self, words: List[str]) -> bool:
        N: int = len(words)
        for i, row in enumerate(words):
            for j, c in enumerate(row):
                if j >= N or i >= len(words[j]) or words[j][i] != c:
                    return False

        return True