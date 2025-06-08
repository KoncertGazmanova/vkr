# ai_module/models.py
from django.db import models
from django.utils import timezone

class SectionOption(models.Model):
    """
    Хранит варианты для различных секций.
    Например, секция типа 'pain' может иметь текст 'Толстая талия?' 
    и свои метрики ctr, cr, is_successful и т.д.
    """
    SECTION_TYPES = [
        ('pain', 'Боль'),
        ('benefit', 'Выгода'),
        ('solution', 'Решение'),
        ('cta', 'Призыв'),
        ('proof', 'Подтверждение'),
    ]

    section_type = models.CharField(
        max_length=20, 
        choices=SECTION_TYPES
    )
    text = models.TextField()

    # Метрики
    ctr = models.FloatField(default=0.0)
    cr = models.FloatField(default=0.0)
    # Можно хранить и прочие статистики: revenue, views и т.п. — на ваше усмотрение
    success_score = models.FloatField(default=0.0)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_section_type_display()} | {self.text[:50]}"


class GeneratedHeadline(models.Model):
    """
    Храним факт «собранного» заголовка как комбинацию секций (pain, benefit, etc.).
    Поле text — финальный склеенный текст (для удобства, чтобы не собирать каждый раз).
    """
    pain_section = models.ForeignKey(
        SectionOption, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="headlines_as_pain"
    )
    benefit_section = models.ForeignKey(
        SectionOption, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="headlines_as_benefit"
    )
    solution_section = models.ForeignKey(
        SectionOption, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="headlines_as_solution"
    )
    cta_section = models.ForeignKey(
        SectionOption, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="headlines_as_cta"
    )
    proof_section = models.ForeignKey(
        SectionOption, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="headlines_as_proof"
    )

    # Готовый сконструированный текст
    text = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    # Метрики/статистика
    ctr = models.FloatField(default=0.0)
    epc = models.FloatField(default=0.0)
    cr = models.FloatField(default=0.0)
    revenue = models.FloatField(default=0.0)
    views = models.IntegerField(default=0)
    leads = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    spend = models.FloatField(default=0.0)
    success_score = models.FloatField(default=0.0)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Headline #{self.pk} (собрано {self.created_at.strftime('%Y-%m-%d')})"
