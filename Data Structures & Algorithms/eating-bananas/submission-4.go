func calcHours(piles []int, k int) int {
    var totalHours int
    for _, p := range piles {
        totalHours += (p + k - 1)/k  // round up
    }
    return totalHours
}

func minEatingSpeed(piles []int, h int) int {
    maxPile := 0
    for _, p := range piles {
        if p > maxPile {
            maxPile = p
        }
    }
    left, right := 1, maxPile
    res := right

    for left <= right {
        mid := left + (right - left) / 2
        if calcHours(piles, mid) <= h {
            res = mid
            right = mid - 1
        } else {
            left = mid + 1
        }
    }
    return res
}
