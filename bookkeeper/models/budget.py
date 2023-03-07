"""
Описан класс, представляющий ограничение бюджета
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Budget:
    """
.   Установка ограниченного бюджета на определенный срок
    amount - сумма ограничения
    category - id категории расходов
    length - срок в днях
    pk - id записи в базе данных
    """
    amount: int
    category: int
    length: int = 7
    start_date: datetime = datetime.now()
    end_date: datetime = start_date + timedelta(days=length)
    pk: int = 0
