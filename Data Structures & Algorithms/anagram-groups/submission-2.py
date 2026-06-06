class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        n: int = len(strs)
        group: List[str] = []
        G: List[List[str]] = []
        visited: List[int] = []

        p1: int = 0

        while p1 < n:
            if p1 not in visited:
                s: str = strs[p1]
                group.append(s)
                chars = sorted([c for c in s])  # Sort characters instead of using a set
                visited.append(p1)
                
                for i in range(p1+1, n):
                    new_s: str = strs[i]
                    if i not in visited and sorted([c for c in new_s]) == chars:
                        group.append(new_s)
                        visited.append(i)
                
                G.append(group)
                group = []  # Reset the group for the next set of anagrams
            
            p1 += 1

        return G
