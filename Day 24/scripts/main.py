import logging
from scripts.config import OUTPUT_DIR
from scripts.create_warehouse import create_warehouse
from scripts.generate_date_dimension import generate_date_dimension
from scripts.load_dimensions import load_dimensions
from scripts.load_facts import load_facts
from scripts.validation import validate

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=OUTPUT_DIR/"pipeline.log", level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s", force=True)
    steps = [
        ("Create warehouse",create_warehouse),
        ("Generate date dimension",generate_date_dimension),
        ("Load dimensions",load_dimensions),
        ("Load facts",load_facts),
        ("Validate warehouse",validate),
    ]
    logging.info("Pipeline started")
    for label, fn in steps:
        print(f"\n--- {label} ---")
        logging.info("Starting %s",label)
        fn()
        logging.info("Completed %s",label)
    logging.info("Pipeline completed")
    print("\nPIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
