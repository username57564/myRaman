import yaml

class RamanPeaks:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)['raman_peaks']
        
        self.data = {}
        self.main_peaks = {}
        self.sub_peaks = {}

        for substance, peaks in data.items():
            if substance == 'VO2':
                for sub_type, sub_peaks in peaks.items():
                    key = f"{substance} ({sub_type})"
                    self.data[key] = set(sub_peaks['all'])
                    self.main_peaks[key] = set(sub_peaks['main'])
                    self.sub_peaks[key] = self.data[key] - self.main_peaks[key]
                # Default to VO2 (M1)
                self.data[substance] = self.data[f"{substance} (M1)"]
                self.main_peaks[substance] = self.main_peaks[f"{substance} (M1)"]
                self.sub_peaks[substance] = self.sub_peaks[f"{substance} (M1)"]
            else:
                self.data[substance] = set(peaks['all'])
                self.main_peaks[substance] = set(peaks['main'])
                self.sub_peaks[substance] = self.data[substance] - self.main_peaks[substance]

    def add_peaks(self, substance_name: str, raman_peaks: set, main_peaks=()):
        if substance_name in self.data:
            print(f"{substance_name} already exists. Overwriting the data.")
        self.data[substance_name] = set(raman_peaks)
        self.main_peaks[substance_name] = set(main_peaks)
        self.sub_peaks[substance_name] = set(raman_peaks) - set(main_peaks)

    def get_peaks(self, substance_name: str, which: str = "all") -> set:
        if which == "all":
            return self.data.get(substance_name)
        elif which == "main":
            return self.main_peaks.get(substance_name)
        elif which == "sub":
            return self.sub_peaks.get(substance_name)
        else:
            print("Invalid input for 'which' parameter. Choose from 'all', 'main', or 'sub'.")
            return None

    def list_substances(self) -> list:
        return list(self.data.keys())

if __name__ == "__main__":
    # YAML 파일에서 데이터를 로드하여 RamanPeaks 인스턴스 생성
    raman_spectra = RamanPeaks('raman_peaks.yaml')

    # 새로운 물질의 라만 스펙트럼 데이터 추가
    raman_spectra.add_peaks('test', {1, 2, 3, 4, 5}, {2, 4})

    # 특정 물질의 라만 스펙트럼 데이터 조회
    name = "VO2"
    for x in ["all", "main", "sub"]:
        print(f"{name} [{x:>4}]: {raman_spectra.get_peaks(name, x)}")

    # 저장된 모든 물질의 이름 조회
    substances = raman_spectra.list_substances()
    print("Substances:", substances)
