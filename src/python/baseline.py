from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict
import math

FILE = "../../data/measurements.txt"


@dataclass
class Measurement:
    station: str
    value: float

    @classmethod
    def from_parts(cls, parts: List[str]):
        return cls(parts[0], float(parts[1]))


@dataclass
class ResultRow:
    min_val: float
    mean: float
    max_val: float

    def __str__(self):
        return f"{self.round(self.min_val)}/{self.round(self.mean)}/{self.round(self.max_val)}"

    def round(self, value: float) -> float:
        return round(value * 10.0) / 10.0


class MeasurementAggregator:
    def __init__(self):
        self.min_val = float('inf')
        self.max_val = float('-inf')
        self.sum = 0.0
        self.count = 0


def main():
    measurements = defaultdict(lambda: MeasurementAggregator())

    # 读取和聚合数据
    with open(FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            measurement = Measurement.from_parts(parts)

            # 更新聚合器
            aggregator = measurements[measurement.station]
            aggregator.min_val = min(aggregator.min_val, measurement.value)
            aggregator.max_val = max(aggregator.max_val, measurement.value)
            aggregator.sum += measurement.value
            aggregator.count += 1

    # 转换结果
    result = {}
    for station, agg in sorted(measurements.items()):
        mean = (round(agg.sum * 10.0) / 10.0) / agg.count
        result[station] = ResultRow(agg.min_val, mean, agg.max_val)

    print(result)


if __name__ == "__main__":
    main()