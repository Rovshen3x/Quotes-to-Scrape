# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PriceConversionToUSDPipeline:
    currency_conversion_factor = 1.28

    def process_item(self, item, spider):
        # get the current item values
        adapter = ItemAdapter(item)
        if adapter.get("price"):
            # convert the price from pounds to dollars
            adapter["price"] = adapter["price"] * self.currency_conversion_factor
            return item
        else:
            raise DropItem(f"Missing price in {item}")
