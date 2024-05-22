# Raman Spectra Analysis

This project contains a Python class for handling Raman spectra data, loaded from a YAML file.

## Files

- `raman_peaks.yaml`: YAML file containing Raman spectra data.
- `raman_peaks.py`: Python script with the `RamanPeaks` class for handling Raman spectra data.
- `README.md`: This file.

## Usage

1. Ensure you have Python and PyYAML installed.
2. Load the data and use the `RamanPeaks` class as shown in the example.

## Example

```python
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
