#@title RamanPeaks_v2
import yaml

class RamanPeaks:
    def __init__(self, yaml_file):
        if yaml_file is None:
            yaml_file = os.path.join(os.path.dirname(__file__), 'data', 'raman_peaks.yaml')
        
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)['raman_peaks']
        
        self.data = {}
        self.main_peaks = {}
        self.sub_peaks = {}

        default_substance = list(data.keys())[0]

        for substance, details in data.items():
            # TO DO: details가 all, main, 다른 phase 정보(all, main)로 구성된 경우
            if isinstance(details[list(details.keys())[0]], dict):
                # 첫번째 subtype을 대푯값으로 저장
                general = details[list(details.keys())[0]]
                self.add_peaks(substance, set(general['all']), main_peaks=set(general['main']))
                for sub_type, peaks in details.items():
                    key = f"{substance} ({sub_type})"
                    self.add_peaks(substance, set(peaks['all']), main_peaks=set(peaks['main']), sub_type=sub_type)
            else:
                self.add_peaks(substance, set(details['all']), main_peaks=set(details['main']))

    def add_peaks(self, substance_name: str, raman_peaks: set, main_peaks=(), sub_type=None):
        key = f"{substance_name} ({sub_type})" if sub_type else substance_name
        if key in self.data:
            print(f"{key} already exists. Overwriting the data.")
        self.data[key] = set(raman_peaks)
        self.main_peaks[key] = set(main_peaks)
        self.sub_peaks[key] = set(raman_peaks) - set(main_peaks)

    def get_peaks(self, substance_name: str, which: str = "all") -> set:
        if which == "all":
            return self.data.get(substance_name, None)
        elif which == "main":
            return self.main_peaks.get(substance_name, None)
        elif which == "sub":
            return self.sub_peaks.get(substance_name, None)
        else:
            print("Invalid input for 'which' parameter. Choose from 'all', 'main', or 'sub'.")
            return None

    def list_substances(self) -> list:
        return list(self.data.keys())
    
    def get_default_substance(self) -> str:
        return list(self.data.keys())[0]

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
