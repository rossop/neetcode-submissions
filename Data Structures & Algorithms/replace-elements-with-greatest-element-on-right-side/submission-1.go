func replaceElements(arr []int) []int {
	n := len(arr)
	if n == 0 {
		return arr
	}

	maxSoFar := -1
	for i := n - 1; i >= 0; i-- {
		currentVal := arr[i]
		arr[i] = maxSoFar

		if currentVal > maxSoFar {
			maxSoFar = currentVal
		}
	}
	return arr
}

func replaceElementsLeftToRight(arr []int) []int {
	n := len(arr)
	if n == 0 {
		return arr
	}

	for i := 0; i < n-1; i++ {
		maxIdx := i + 1
		for j := i + 1; j < n; j++ {
			if arr[j] > arr[maxIdx] {
				maxIdx = j
			}
		}

		arr[i] = arr[maxIdx]
	}
	
	// Set the last element to -1 as per the standard problem rule
	if n > 0 {
		arr[n-1] = -1
	}
	return arr
}
