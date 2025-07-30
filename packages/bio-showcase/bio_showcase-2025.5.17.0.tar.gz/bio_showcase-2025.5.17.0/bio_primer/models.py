from django.db import models
import json


class PCRResult(models.Model):
    sequence = models.CharField()
    seq_start = models.IntegerField()
    seq_end = models.IntegerField()

    result = models.CharField()


class Primer:
    def __init__(self, d):
        self.sequence = d["SEQUENCE"]
        self.gc_percent = d["GC_PERCENT"]


class ResultObject:
    def __init__(self, result_str: str):
        self.result = json.loads(result_str)
        self.primers_left = []
        self.primers_right = []
        self.primers_internal = []
        for d in self.result['PRIMER_LEFT']:
            primer = Primer(d)
            self.primers_left.append(primer)
        for d in self.result['PRIMER_RIGHT']:
            primer = Primer(d)
            self.primers_right.append(primer)
        for d in self.result['PRIMER_INTERNAL']:
            primer = Primer(d)
            self.primers_internal.append(primer)