
import os
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import Integer, Numeric, String, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
load_dotenv(os.path.join(PROJECT_ROOT, "Day 10", ".env"))


# Build the database URL safely, even if your password has special characters.
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "ecommerce_db"),
)

engine = create_engine(database_url, echo=False)


class Base(DeclarativeBase):
    pass


# This is a separate practice table. Your existing products table is untouched.
class DemoProduct(Base):
    __tablename__ = "day10_demo_products"

    product_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)


def main():
    try:
        # Create only the dedicated practice table if it does not exist.
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            # CREATE
            demo_product = DemoProduct(
                product_name="Day 10 Demo Keyboard",
                category="Practice",
                price=Decimal("999.00"),
            )
            session.add(demo_product)
            session.commit()
            demo_id = demo_product.product_id
            print(f"CREATE: Added demo product with ID {demo_id}")

            # READ
            product = session.get(DemoProduct, demo_id)
            print(
                f"READ: {product.product_name} | "
                f"{product.category} | Rs. {product.price}"
            )

            # UPDATE
            product.price = Decimal("1099.00")
            session.commit()
            print(f"UPDATE: New price = Rs. {product.price}")

            # QUERY using a SQLAlchemy SELECT statement
            statement = (
                select(DemoProduct)
                .where(DemoProduct.category == "Practice")
                .order_by(DemoProduct.price.desc())
            )
            results = session.scalars(statement).all()

            print("\nPractice products:")
            for item in results:
                print(item.product_id, item.product_name, item.price)

            # DELETE only the demo row created during this run.
            session.delete(product)
            session.commit()
            print(f"\nDELETE: Removed demo product ID {demo_id}")

        print("\nSQLAlchemy CRUD demonstration completed successfully.")

    except Exception as error:
        print(f"SQLAlchemy demonstration failed: {error}")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
