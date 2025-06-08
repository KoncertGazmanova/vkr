# ai_module/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import SectionOption, GeneratedHeadline
from .serializers import (
    SectionOptionSerializer,
    GeneratedHeadlineSerializer
)

# ===================== #
#     SectionOption     #
# ===================== #

class SectionOptionListCreateView(generics.ListCreateAPIView):
    """
    GET -> список всех SectionOption, POST -> создать новую.
    Пример запроса POST:
    {
       "section_type": "pain",
       "text": "Толстая талия?",
       "ctr": 12.3,
       "cr": 3.5,
       "success_score": 75,
       "is_successful": true
    }
    """
    queryset = SectionOption.objects.all()
    serializer_class = SectionOptionSerializer


class SectionOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET -> одна конкретная запись
    PUT/PATCH -> обновление
    DELETE -> удаление
    """
    queryset = SectionOption.objects.all()
    serializer_class = SectionOptionSerializer


# ========================= #
#  GeneratedHeadline (CRUD) #
# ========================= #

class GeneratedHeadlineListView(generics.ListCreateAPIView):
    """
    GET -> список всех собранных заголовков
    POST -> создать новый заголовок (если хотим руками указать секции)
    """
    queryset = GeneratedHeadline.objects.all().order_by('-created_at')
    serializer_class = GeneratedHeadlineSerializer

    def create(self, request, *args, **kwargs):
        """
        Можно принимать ID нужных секций и собирать 'text'.
        Пример POST:
        {
          "pain_section_id": 1,
          "benefit_section_id": 5,
          "solution_section_id": 10,
          "cta_section_id": 12,
          "proof_section_id": null
        }
        """
        pain_id = request.data.get("pain_section_id")
        benefit_id = request.data.get("benefit_section_id")
        solution_id = request.data.get("solution_section_id")
        cta_id = request.data.get("cta_section_id")
        proof_id = request.data.get("proof_section_id")

        pain_obj = SectionOption.objects.filter(id=pain_id).first() if pain_id else None
        benefit_obj = SectionOption.objects.filter(id=benefit_id).first() if benefit_id else None
        solution_obj = SectionOption.objects.filter(id=solution_id).first() if solution_id else None
        cta_obj = SectionOption.objects.filter(id=cta_id).first() if cta_id else None
        proof_obj = SectionOption.objects.filter(id=proof_id).first() if proof_id else None

        # Сконструируем сам текст 
        # Пример: "[pain] + [benefit] + [solution] + [cta] + [proof]"
        # Можно как угодно объединять, добавлять разделители, заголовки и т.д.
        final_text_parts = []
        if pain_obj:
            final_text_parts.append(pain_obj.text)
        if benefit_obj:
            final_text_parts.append(benefit_obj.text)
        if solution_obj:
            final_text_parts.append(solution_obj.text)
        if cta_obj:
            final_text_parts.append(cta_obj.text)
        if proof_obj:
            final_text_parts.append(proof_obj.text)

        combined_text = " | ".join(final_text_parts)

        new_headline = GeneratedHeadline.objects.create(
            pain_section=pain_obj,
            benefit_section=benefit_obj,
            solution_section=solution_obj,
            cta_section=cta_obj,
            proof_section=proof_obj,
            text=combined_text
        )
        # Сериализуем
        serializer = self.get_serializer(new_headline)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GeneratedHeadlineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/PATCH/DELETE для конкретного заголовка.
    """
    queryset = GeneratedHeadline.objects.all()
    serializer_class = GeneratedHeadlineSerializer


@api_view(['GET'])
def get_headlines_by_section(request):
    """
    GET /api/ai/headlines/by_section/?section_type=benefit&section_id=7
    Возвращает все заголовки, где эта секция используется (успешные).
    """
    section_type = request.GET.get("section_type")
    section_id = request.GET.get("section_id")

    if section_type not in ["pain", "benefit", "solution", "cta", "proof"] or not section_id:
        return Response({"error": "Нужно указать section_type и section_id"}, status=400)

    filter_field = f"{section_type}_section_id"
    query = {filter_field: section_id, "is_successful": True}
    headlines = GeneratedHeadline.objects.filter(**query).order_by("-success_score")

    serializer = GeneratedHeadlineSerializer(headlines, many=True)
    return Response(serializer.data)


# Добавление обработчика для генерации случайного заголовка
@api_view(['POST'])
def generate_random_headline(request):
    """Генерация случайного заголовка."""
    try:
        random_headline = GeneratedHeadline.objects.order_by('?').first()
        if random_headline:
            serializer = GeneratedHeadlineSerializer(random_headline)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Нет доступных заголовков"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Добавление функции для подбора лучшего заголовка
@api_view(['POST'])
def assemble_best_headline(request):
    """Подбор лучшего заголовка из выбранной секции."""
    try:
        section_type = request.data.get("section_type")
        section_id = request.data.get("section_id")

        if not section_type or not section_id:
            return Response({"error": "Необходимо указать section_type и section_id"}, status=status.HTTP_400_BAD_REQUEST)

        filter_field = f"{section_type}_section_id"
        headlines = GeneratedHeadline.objects.filter(**{filter_field: section_id}).order_by("-success_score")

        if headlines.exists():
            best_headline = headlines.first()
            serializer = GeneratedHeadlineSerializer(best_headline)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Нет заголовков для данной секции"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
