import pandas as pd
import xml.etree.ElementTree as ET
import os


class DetectorAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, 'data')
        self.output_dir = os.path.join(base_dir, 'output')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def parse_detector_files(self):
        data = {}
        print(f"Searching for detector files in: {self.data_dir}")
        for file in os.listdir(self.data_dir):
            if file.startswith("e2_") and file.endswith(".xml"):
                file_path = os.path.join(self.data_dir, file)
                print(f"Parsing detector file: {file_path}")
                tree = ET.parse(file_path)
                root = tree.getroot()
                detector_id = int(file.split('_')[1].split('.')[0])  # e2_X.xml에서 X를 추출

                intervals = root.findall('interval')
                for index, interval in enumerate(intervals):
                    for attr, value in interval.attrib.items():
                        if attr not in data:
                            data[attr] = {}
                        if detector_id not in data[attr]:
                            data[attr][detector_id] = {}
                        data[attr][detector_id][index] = value

        return data

    def create_dataframes(self):
        data = self.parse_detector_files()
        dataframes = {}

        for attr, det_data in data.items():
            df = pd.DataFrame(det_data)
            df.index.name = 'interval'
            df.columns.name = 'detector'
            dataframes[attr] = df.sort_index().sort_index(axis=1)

        return dataframes

    def save_dataframes_to_csv(self):
        dataframes = self.create_dataframes()
        for attr, df in dataframes.items():
            csv_path = os.path.join(self.output_dir, f"{attr}.csv")
            df.to_csv(csv_path)
            print(f"{attr} data saved to {csv_path}")

    def print_dataframes(self):
        dataframes = self.create_dataframes()
        for attr, df in dataframes.items():
            print(f"\n{attr} Dataframe:")
            print(df)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    analyzer = DetectorAnalyzer(current_dir)
    analyzer.save_dataframes_to_csv()
    analyzer.print_dataframes()