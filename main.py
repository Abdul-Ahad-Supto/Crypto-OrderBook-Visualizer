import requests
import matplotlib.pyplot as plt

# Replace with the trading pair symbol you want to monitor
symbol = 'RUNEUSDT'

# URL for the Binance API with a larger depth (e.g., 50 levels)
url = f'https://api.binance.com/api/v1/depth?symbol={symbol}&limit=1000'

# Function to fetch order book data and visualize it
def visualize_order_book():
    response = requests.get(url)
    if response.status_code == 200:
        order_book = response.json()
        bids = order_book['bids']
        asks = order_book['asks']

        # Extract prices and quantities for buyers and sellers
        buyer_prices = [float(bid[0]) for bid in bids]
        buyer_quantities = [float(bid[1]) for bid in bids]

        seller_prices = [float(ask[0]) for ask in asks]
        seller_quantities = [float(ask[1]) for ask in asks]

        # Calculate the total sum of buyer and seller prices separately
        total_buyer_sum = sum([price * quantity for price, quantity in zip(buyer_prices, buyer_quantities)])
        total_seller_sum = sum([price * quantity for price, quantity in zip(seller_prices, seller_quantities)])

        # Create subplots for buyers, sellers, and the comparison of sums
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

        # Plot buyer quantities as a histogram
        ax1.hist(buyer_prices, weights=buyer_quantities, bins=50, color='green', alpha=0.6, label='Buyers')
        ax1.set_title('Buyers')
        ax1.invert_xaxis()  # Invert x-axis to display highest prices on top
        ax1.get_xaxis().get_major_formatter().set_useOffset(False)  # Prevent scientific notation

        # Plot seller quantities as a histogram
        ax2.hist(seller_prices, weights=seller_quantities, bins=50, color='red', alpha=0.6, label='Sellers')
        ax2.set_title('Sellers')
        ax2.invert_xaxis()
        ax2.get_xaxis().get_major_formatter().set_useOffset(False)

        # Plot the comparison of total buyer and seller sums
        ax3.bar(['Buyers', 'Sellers'], [total_buyer_sum, total_seller_sum], color=['green', 'red'])
        ax3.set_title('Comparison of Total Buyer and Seller Sums')
        ax3.set_ylabel('Total Sum')

        # Format total sums as strings without scientific notation for legend
        total_buyer_sum_str = f'{total_buyer_sum:.2f}'  # Adjust decimal places as needed
        total_seller_sum_str = f'{total_seller_sum:.2f}'  # Adjust decimal places as needed

        # Create custom icons (design bars) for the legend
        buyer_bar = plt.Line2D([0], [0], color='green', lw=10, label=f'Total Buyers: {total_buyer_sum_str}')
        seller_bar = plt.Line2D([0], [0], color='red', lw=10, label=f'Total Sellers: {total_seller_sum_str}')

        # Show legend with formatted total sums for both buyers and sellers
        ax1.legend()
        ax2.legend()

        # Combine both buyer and seller sums with the custom icons in the legend
        ax3.legend(handles=[buyer_bar, seller_bar], loc='upper left')

        plt.tight_layout()

        # Pause for a few seconds to allow the plot to be displayed
        plt.pause(10)

        # Close the plot to allow for the next update
        plt.close()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# Periodically update and visualize the order book
while True:
    visualize_order_book()