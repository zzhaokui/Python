import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Define the path to the CSV file
csv_path = './rav4_cars.csv'
# csv_path = './crv_cars.csv'

# Check if the file exists at the specified path
if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}")
else:
    # Read the CSV file without headers
    df = pd.read_csv(csv_path, header=None, names=['title', 'location', 'yearnotused', 'odometer', 'price', 'link'])

    # Extract year from title column
    df['year'] = df['title'].str.extract(r'(\b\d{4}\b)', expand=False)

    # Convert the 'year' column to integer (if not already NaN)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')

    # Drop rows where year couldn't be converted to integer
    df = df.dropna(subset=['year'])

    # 删除原始的year_data列
    df.drop(columns=['yearnotused'], inplace=True)

    # Extract numeric part of the odometer reading
    df['odometer'] = df['odometer'].astype(str).apply(lambda x: re.search(r'\d+(?:,\d+)*', x).group() if re.search(r'\d+(?:,\d+)*', x) else '')

    # Clean the 'odometer' column
    df['odometer'] = df['odometer'].str.replace(',', '')

    # Drop rows where odometer cannot be converted to integer
    df = df[df['odometer'].str.isnumeric()]

    # Convert the 'odometer' column to integer
    df['odometer'] = df['odometer'].astype(int)

    # Clean the 'price' column
    df['price'] = df['price'].str.replace('$', '').str.replace(',', '')

    # Fill NaN values with empty string in 'price' column
    df['price'] = df['price'].fillna('')

    # Drop rows where price cannot be converted to integer
    df = df[df['price'].str.isnumeric()]

    # Convert the 'price' column to integer
    df['price'] = df['price'].astype(int)

    # Fill missing locations with empty strings
    df['location'] = df['location'].fillna('')

    # Print the DataFrame to check
    print(df)

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Plot 1: Distribution of car years
    # df['year'].value_counts().sort_index().plot(kind='bar', ax=axs[0, 0], color='skyblue')

    # avoid value overlapping for small pie slice
    def my_autopct(pct):
        return f'{pct:.1f}%' if pct >= 2 else ''

    df['year'].value_counts().sort_index().plot(kind='pie', ax=axs[0, 0], autopct=my_autopct, startangle=90,
                                                colors = ['#99d6ea', '#66c3e5', '#33afe0', '#008bcc',
                                                          '#006e99', '#005566', '#003933', '#002200'], fontsize=12)
    axs[0, 0].set_title('Distribution of Car Years')
    axs[0, 0].set_xlabel('Year')
    axs[0, 0].set_ylabel('Number of Cars')

    # Plot 2: Distribution of odometer readings
    axs[0, 1].hist(df['odometer'], bins=20, edgecolor='k', alpha=0.7, color='orange')
    axs[0, 1].set_title('Distribution of Odometer Readings')
    axs[0, 1].set_xlabel('Odometer (km)')
    axs[0, 1].set_ylabel('Number of Cars')

    # Plot 3: Distribution of car prices
    axs[1, 0].hist(df['price'], bins=20, edgecolor='k', alpha=0.7, color='green')
    axs[1, 0].set_title('Distribution of Car Prices')
    axs[1, 0].set_xlabel('Price ($)')
    axs[1, 0].set_ylabel('Number of Cars')

    # Plot 4: Price vs Odometer
    axs[1, 1].scatter(df['odometer'], df['price'], alpha=0.7, color='red')
    axs[1, 1].set_title('Price vs Odometer')
    axs[1, 1].set_xlabel('Odometer (km)')
    axs[1, 1].set_ylabel('Price ($)')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    plt.show()
