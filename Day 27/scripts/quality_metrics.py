"""Evaluate validator against labelled valid/invalid cases (false positives/negatives)."""
import json
from pathlib import Path
from scripts.transform import validate_sale
from scripts.common import PROJECT_ROOT

def run_validation_metrics():
    customer_ids={"C1"}
    cases=[
      ({"sale_id":"A1","customer_id":"C1","amount":"100","sale_date":"2026-11-21"},False),
      ({"sale_id":"A2","customer_id":"C1","amount":"0","sale_date":"2026-11-21"},True),
      ({"sale_id":"A3","customer_id":"C1","amount":"-1","sale_date":"2026-11-21"},True),
      ({"sale_id":"A4","customer_id":"BAD","amount":"100","sale_date":"2026-11-21"},True),
      ({"sale_id":"A5","customer_id":"C1","amount":"abc","sale_date":"2026-11-21"},True),
      ({"sale_id":"A6","customer_id":"C1","amount":"100","sale_date":"bad-date"},True),
      ({"sale_id":"","customer_id":"C1","amount":"100","sale_date":"2026-11-21"},True),
      ({"sale_id":"A8","customer_id":"C1","amount":"100","sale_date":"2026-11-21"},False),
    ]
    tp=tn=fp=fn=0; details=[]
    for row,expected_invalid in cases:
        actual_invalid=bool(validate_sale(row,customer_ids,set()))
        if expected_invalid and actual_invalid: tp+=1
        elif not expected_invalid and not actual_invalid: tn+=1
        elif not expected_invalid and actual_invalid: fp+=1
        else: fn+=1
        details.append({"sale_id":row["sale_id"],"expected_invalid":expected_invalid,"actual_invalid":actual_invalid,
                        "reason":validate_sale(row,customer_ids,set())})
    result={"true_positive_invalid_rejected":tp,"true_negative_valid_accepted":tn,
            "false_positive_valid_rejected":fp,"false_negative_invalid_accepted":fn,
            "cases":len(cases),"accuracy":round((tp+tn)/len(cases),4),"details":details,
            "note":"Synthetic labelled validation cases; this measures rule behavior on these fixtures, not production-wide accuracy."}
    out=PROJECT_ROOT/"outputs"/"test_results"; out.mkdir(parents=True,exist_ok=True)
    (out/"validation_confusion_metrics.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("Validation metrics:",{k:v for k,v in result.items() if k!="details"})
    return result

if __name__=="__main__": run_validation_metrics()
