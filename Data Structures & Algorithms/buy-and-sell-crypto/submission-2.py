class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = prices[0]  # Initialize the min_price to a very high value
        max_profit = 0  # Initialize max_profit to 0
        
        for price in prices:
            # If the current price is lower than the min_price, update min_price
            if price < min_price:
                min_price = price
            
            # Calculate the potential profit if selling at the current price
            potential_profit = price - min_price
            
            # If the potential profit is greater than the max_profit, update max_profit
            if potential_profit > max_profit:
                max_profit = potential_profit
        
        return max_profit