from scrapy.exporters import CsvItemExporter


class CSVPipeline(object):

    def __init__(self):
        file_by_type = open('median7.csv', 'w+b')
        file_by_number = open('average7.csv', 'w+b')
        self.exporter_type = CsvItemExporter(file_by_type)
        self.exporter_number = CsvItemExporter(file_by_number)

    def process_item(self, item, spider):
        chart = item.pop('chart')
        if chart == 'type':
            self.exporter_type.export_item(item)
        else:

            self.exporter_number.export_item(item)

        print(item)
        return item
