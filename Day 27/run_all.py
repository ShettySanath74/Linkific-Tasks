"""One-command Day 27 runner."""
import json, subprocess, sys
from pathlib import Path
from scripts.common import PROJECT_ROOT, OUTPUT_DIR, ensure_directories
from scripts.generate_test_data import generate_all
from scripts.extract import extract_customers, extract_sales
from scripts.transform import transform_records
from scripts.load import load_sales
from scripts.quality_check import run_quality_checks
from scripts.performance_test import run_benchmarks
from scripts.parallel_test import run_parallel_comparison
from scripts.quality_metrics import run_validation_metrics

def main():
    ensure_directories()
    print("\\n[1/5] Generating synthetic datasets...")
    generated=generate_all()
    print("Generated:", ", ".join(Path(p).name for p in generated))
    print("\\n[2/5] Running automated tests...")
    test=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=PROJECT_ROOT)
    if test.returncode: raise SystemExit("Automated tests failed; fix failures before continuing.")
    print("\\n[3/5] Running end-to-end pipeline on bundled Day 26 sample...")
    customers=extract_customers(); sales=extract_sales()
    accepted=transform_records(customers,sales)
    db=load_sales(accepted)
    report=run_quality_checks(accepted,db)
    print("Quality report:",report)
    print("\\n[4/5] Running performance benchmarks (1k, 10k, 100k)...")
    perf=run_benchmarks()
    parallel=run_parallel_comparison(10000)
    validation_metrics=run_validation_metrics()
    print("\\n[5/5] Writing execution summary...")
    summary={"automated_tests":"PASSED","sample_pipeline":"PASSED","quality_report":str(report),
             "synthetic_datasets":generated,"performance_report":str(OUTPUT_DIR/"performance"/"performance_report.json"),
             "benchmark_results":perf["results"],"parallel_comparison":parallel,"validation_metrics":validation_metrics}
    (OUTPUT_DIR/"day27_execution_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print("\\nDAY 27 RUN COMPLETED. Summary:",OUTPUT_DIR/"day27_execution_summary.json")

if __name__=="__main__": main()
