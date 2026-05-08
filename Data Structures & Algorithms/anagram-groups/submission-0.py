class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_dict: Dict[str, List[str]] = defaultdict(list)

        for s in strs:
            # Sort the string and use it as a key
            key = ''.join(sorted(s))
            anagram_dict[key].append(s)

        # Return the grouped anagrams
        return list(anagram_dict.values())
