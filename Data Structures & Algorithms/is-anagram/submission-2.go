func isAnagram(s string, t string) bool {
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
