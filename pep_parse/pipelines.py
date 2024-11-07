import csv
import datetime as dt
import os

from .constants import BASE_DIR, DATETIME_FORMAT, RESULTS


class PepParsePipeline:

    def __init__(self):
        self.status_count = {}
        self.results = []
        self.file_path = os.path.join(BASE_DIR, RESULTS)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item.get('status')
        if status in self.status_count:
            self.status_count[status] += 1
        else:
            self.status_count[status] = 1
        return item

    def close_spider(self, spider):
        date = dt.datetime.now().strftime(DATETIME_FORMAT)
        filename = f'status_summary_{date}.csv'
        csvfile = os.path.join(self.file_path, filename)
        with open(csvfile, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.status_count.items():
                writer.writerow([status, count])
            writer.writerow(['Total', sum(self.status_count.values())])
