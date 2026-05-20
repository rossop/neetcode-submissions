import "slices"

func isAnagram(s string, t string) bool {
    if len(s) != len(t) {
        return false
    }
    sRunes := []rune(s)
    tRunes := []rune(t)

    slices.Sort(sRunes)
    slices.Sort(tRunes)
    
    return slices.Equal(sRunes, tRunes)
}

func isAnagram2(s string, t string) bool {
    if len(s) != len(t) {
        return false
    }

    counts := make(map[rune]int)

    for _, char := range s {
        counts[char]++
    }

    for _, char := range t {
        counts[char]--
        if counts[char] < 0 {
            return false
        }
    }
    return true
}
