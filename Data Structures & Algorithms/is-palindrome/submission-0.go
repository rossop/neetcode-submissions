func isPalindrome(s string) bool {
	l, r := 0, len(s) - 1
	for l < r {
		// skip non-alphanumeric from left
		for l < r && !isAlphaNum(s[l]) {
			l++
		}

		// skip non-alphanumeric from right
		for r > l && !isAlphaNum(s[r]) {
			r--
		}

		if strings.ToLower(string(s[l])) != strings.ToLower(string(s[r])){
			return false
		}
		l++
		r --
	}
	return true
}

func isAlphaNum(c byte) bool {
    return ('A' <= c && c <= 'Z') ||
        ('a' <= c && c <= 'z') ||
        ('0' <= c && c <= '9')
}
