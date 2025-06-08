# ai_module/serializers.py
from rest_framework import serializers
from .models import SectionOption, GeneratedHeadline

class SectionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionOption
        fields = (
            'id', 
            'section_type', 
            'text', 
            'ctr', 
            'cr',
            'success_score',
            'is_successful',
        )

class GeneratedHeadlineSerializer(serializers.ModelSerializer):
    # Чтобы при GET-запросах удобно видеть тексты секций, 
    # можно дополнительно прописать вложенные сериализаторы или поля:
    pain_section = SectionOptionSerializer(read_only=True)
    benefit_section = SectionOptionSerializer(read_only=True)
    solution_section = SectionOptionSerializer(read_only=True)
    cta_section = SectionOptionSerializer(read_only=True)
    proof_section = SectionOptionSerializer(read_only=True)

    class Meta:
        model = GeneratedHeadline
        fields = (
            'id',
            'pain_section',
            'benefit_section',
            'solution_section',
            'cta_section',
            'proof_section',
            'text',
            'created_at',
            'ctr',
            'epc',
            'cr',
            'revenue',
            'views',
            'leads',
            'sales',
            'spend',
            'success_score',
            'is_successful',
        )
