import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError


def load_data(file_path):
    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        print("File Not Found, Check your file!")
        return None

    except EmptyDataError:
        print("The file is empty!")
        return None

    except PermissionError:
        print("This is a folder, not a CSV file!")
        return None


def analyze_sales(data):

    data["Revenue"] = data["Quantity"] * data["Price"]

    quantity = data["Quantity"].sum()
    total_revenue = data["Revenue"].sum()
    average_price = data["Price"].mean()

    best_product = data[
        data["Revenue"] == data["Revenue"].max()
    ]["Product"].iloc[0]

    cat_revenue = data.groupby("Category")["Revenue"].sum()

    product_revenue = (
        data.groupby("Product")["Revenue"]
        .sum()
    )

    top_products = (
        product_revenue
        .sort_values(ascending=False)
        .head(5)
    )

    product_quantity = (
        data.groupby("Product")["Quantity"]
        .sum()
    )

    best_category = (
        cat_revenue[
            cat_revenue == cat_revenue.max()
        ].index[0]
    )

    most_sold = data[
        data["Quantity"] == data["Quantity"].max()
    ]["Product"].iloc[0]

    lowest_revenue = data[
        data["Revenue"] == data["Revenue"].min()
    ]["Product"].str.cat(sep=", ")

    average_revenue = data["Revenue"].mean()

    category_percentage = (
        cat_revenue / total_revenue * 100
    )

    most_sold_revenue = data[
        data["Product"] == most_sold
    ]["Revenue"].iloc[0]

    most_sold_percentage = (
        most_sold_revenue / total_revenue * 100
    )

    if most_sold == best_product:

        sales_vs_revenue = (
            f"{most_sold} is both the most sold product "
            f"and the top revenue-generating product."
        )

    else:

        sales_vs_revenue = (
            f"{most_sold} is the most sold product, "
            f"but {best_product} generates the most revenue."
        )

    low_revenue_product = data[
        data["Revenue"] < average_revenue
    ]["Product"].str.cat(sep=", ")

    high_quantity_low_revenue = data[
        (data["Quantity"] > data["Quantity"].mean())
        &
        (data["Revenue"] < average_revenue)
    ]

    high_quantity_low_revenue_names = (
        high_quantity_low_revenue["Product"]
        .str.cat(sep=", ")
    )

    insight = (
        f"{best_category} is the main revenue driver, "
        f"generating {category_percentage[best_category]:.2f}% "
        f"of total revenue"
    )

    insight2 = (
        f"{most_sold} is the most sold product, "
        f"with {data['Quantity'].max()} sold, "
        f"generating ${most_sold_revenue}, "
        f"which contributes {most_sold_percentage:.2f}% "
        f"of total revenue."
    )

    insight3 = (
        f"{high_quantity_low_revenue_names} sell above average "
        f"quantity but generate below average revenue."
    )

    return {
        "quantity": quantity,
        "total_revenue": total_revenue,
        "best_product": best_product,
        "best_category": best_category,
        "average_price": average_price,
        "most_sold": most_sold,
        "lowest_revenue": lowest_revenue,
        "average_revenue": average_revenue,
        "category_percent": category_percentage,
        "insight": insight,
        "insight2": insight2,
        "low_revenue_product": low_revenue_product,
        "insight3": insight3,
        "top_products": top_products,
        "sales_vs_revenue": sales_vs_revenue,
    }


def create_chart(
    x,
    y,
    xlabel,
    ylabel,
    title,
    is_currency
):

    bars = plt.bar(x, y)

    for bar in bars:

        height = bar.get_height()

        if is_currency:
            label = f"${height:,.0f}"
        else:
            label = f"{height:,.0f}"

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + max(y) * 0.02,
            label,
            ha="center"
        )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)

    plt.ylim(
        0,
        max(y) * 1.1
    )

    plt.tight_layout()
    plt.show()


def main():

    required_columns = [
        "Product",
        "Category",
        "Quantity",
        "Price"
    ]

    numeric_columns = [
        "Quantity",
        "Price"
    ]

    text_columns = [
        "Product",
        "Category"
    ]

    while True:

        file_path = "AI_Data_Analyzer/sale.csv"

        data = load_data(file_path)

        if data is not None:

            valid = True

            for column in required_columns:

                if column not in data.columns:

                    print(
                        "The format is not correct!"
                    )

                    valid = False

            if valid:

                for column in numeric_columns:

                    if not pd.api.types.is_numeric_dtype(
                        data[column]
                    ):

                        print(
                            "There is a wrong data"
                        )

                        valid = False

                    if (data[column] < 0).any():

                        print(
                            f"{column} cannot be negative!"
                        )

                        valid = False

                    if data[column].isna().any():

                        print(
                            f"{column} contains missing values!"
                        )

                        valid = False

                for column in text_columns:

                    if (
                        data[column].isna().any()
                        or
                        (data[column].str.strip() == "").any()
                    ):

                        print(
                            f"{column} contains missing values!"
                        )

                        valid = False

            if valid:
                break

    results = analyze_sales(data)

    print(data)

    print(
        "=========== Sales Report ==========="
    )

    print(
        f"Total Quantity: {results['quantity']}"
    )

    print(
        f"Total Revenue: ${results['total_revenue']}"
    )

    print(
        f"Best Product: {results['best_product']}"
    )

    print(
        f"Best Category: {results['best_category']}"
    )

    print(
        f"Average Price: ${results['average_price']}"
    )

    print(
        f"Most Sold Product: {results['most_sold']}"
    )

    print(
        f"Lowest Revenue: {results['lowest_revenue']}"
    )

    print(
        f"Average Revenue: ${results['average_revenue']}"
    )

    print(
        "Top 5 Products by Revenue:"
    )

    for product, revenue in results[
        "top_products"
    ].items():

        print(
            f"{product}: ${revenue:,.0f}"
        )

    for category, percentage in results[
        "category_percent"
    ].items():

        print(
            f"{category} generates "
            f"{percentage:.2f}% of the total revenue"
        )

    print(results["insight"])

    print(results["insight2"])

    print(
        f"Products below average revenue: "
        f"{results['low_revenue_product']}"
    )

    print(results["insight3"])

    print(results["sales_vs_revenue"])


if __name__ == "__main__":
    main()

