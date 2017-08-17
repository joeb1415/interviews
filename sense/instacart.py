import os
import pandas as pd


class Instacart:
    def __init__(self):
        self.data_path = 'instacart_2017_05_01'
        self.orders = None
        self.products = None
        self.order_products = None

    def load_data(self, train_only=False):
        self.orders = pd.read_csv(os.sep.join([self.data_path, 'orders.csv']))
        self.products = pd.read_csv(os.sep.join([self.data_path, 'products.csv']))
        self.order_products = pd.read_csv(os.sep.join([self.data_path, 'order_products__train.csv']))

        if train_only:
            return

        order_products2 = pd.read_csv(os.sep.join([self.data_path, 'order_products__prior.csv']))
        self.order_products = self.order_products.append(order_products2)

    def report_1(self):
        """
        Find which product is the most frequently ordered in a given hour of the day.
        Across all days, e.g. "What do people order most at 2pm?"
        """

        order_product_hour = self.orders.merge(self.order_products, on='order_id')
        order_product_hour = order_product_hour[['order_id', 'product_id', 'order_hour_of_day']]

        hour_product_count = order_product_hour.groupby(['order_hour_of_day', 'product_id']).agg('count')

        hour_count = hour_product_count.reset_index()
        hour_count = hour_count.sort_values(['order_hour_of_day', 'order_id'], ascending=[True, False])

        hour_max_count = hour_count.groupby(['order_hour_of_day']).first()
        hour_max_count = hour_max_count.merge(self.products, on='product_id')[['product_name', 'order_id']]
        hour_max_count = hour_max_count.rename(columns={'order_id': 'order_count'})

        return hour_max_count

    def report_2(self, n):
        """
Report 2:

Top n products with the shortest average re-order time

Overview:
Average re-order time for a product is determined from the "days_since_prior_order" column. This represents the days elapsed from when the user placed the same order.
Calculate the average re-order time for a product
Take top n

Deliverables:
A program that outputs the n products with the shortest average re-order times
        """

        product_days = self.orders.merge(self.order_products, on='order_id')
        product_days = product_days[['product_id', 'days_since_prior_order']]
        product_days = product_days.dropna()

        product_mean_days = product_days.groupby('product_id').agg('mean').reset_index()
        product_mean_days = product_mean_days.sort_values(['days_since_prior_order', 'product_id'])  # adding product_id sort for result consistency
        product_mean_days = product_mean_days.reset_index(drop=True)  # renumber index from 0
        product_mean_days = product_mean_days.iloc[:n]

        product_mean_days = product_mean_days.merge(self.products, on='product_id')[['product_name', 'days_since_prior_order']]
        product_mean_days = product_mean_days.rename(columns={'days_since_prior_order': 'mean_days_since_prior_order'})

        return product_mean_days
