from datetime import datetime
import os
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = Counter()

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        # filename = 'results/status_summary_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        filename = os.path.join(
            BASE_DIR,
            'results/status_summary_'
            f'{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.csv')

        total = sum(self.status_counter.values())
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in self.status_counter.items():
                f.write(f'{status},{count}\n')
            f.write(f'Total,{total}\n')
