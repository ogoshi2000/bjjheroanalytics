import json
from scrapy.spiders import Spider
import os


class StatisticsSpider(Spider):
    name = "Statistics"
    allowed_domains = ["bjjheroes.com"]
    if os.path.exists("statistics.json"):
        os.remove("statistics.json")

    with open("fighters.json") as f:
        data = json.load(f)
    start_urls = [fighter["URL"] for fighter in data]

    def parse(self, response):
        all_rows_data = []
        # Check if the table exists on the page
        fighter_name = response.xpath('//h1[@itemprop="name"]/text()').get()
        table = response.xpath('//table[contains(@class, "table") and contains(@class, "table-striped") and contains(@class, "sort_table")]')
        if table:
            # Select all rows in the table
            rows = table.xpath(".//tr")

            for row in rows[1:]:
                cells_data = []
                cells = row.xpath(".//td")
                cells = cells[1:]
                for index, cell in enumerate(cells):
                    if index == 0:
                        name = cell.xpath(".//span/text()").get()
                        cells_data.append(name)
                    else:
                        cell_text = cell.xpath(".//text()").get()
                        cells_data.append(cell_text.strip() if cell_text else None)

                row_data = {
                    "opponent": cells_data[0] if len(cells) > 0 else None,
                    "w_l": cells_data[1] if len(cells) > 1 else None,
                    "method": cells_data[2] if len(cells) > 2 else None,
                    "competition": cells_data[3] if len(cells) > 3 else None,
                    "weight": cells_data[4] if len(cells) > 4 else None,
                    "stage": cells_data[5] if len(cells) > 5 else None,
                    "year": cells_data[6] if len(cells) > 6 else None,
                }
                all_rows_data.append(row_data)

            item = {"URL": response.url, "Name": fighter_name, "TableData": all_rows_data}
            yield item
        else:
            self.logger.info("Table not found on %s", response.url)
