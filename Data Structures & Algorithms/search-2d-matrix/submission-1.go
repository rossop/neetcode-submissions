func searchMatrix(matrix [][]int, target int) bool {
	rows, cols := len(matrix), len(matrix[0])
	l, r := 0, rows * cols - 1

	for l <= r {
		mid := (l+r) / 2
		val := matrix[mid / cols][mid % cols]
		if val < target {
			l = mid + 1
		} else if val > target {
			r = mid - 1
		} else {
			return true
		}
	}
	return false
}
