def score_campaign(campaign):
    """
    Анализ эффективности кампании с использованием AI.
    Возвращает оценку эффективности кампании.
    """
    # Пример простой логики анализа
    if campaign.total_clicks == 0:
        return 0

    conversion_rate = campaign.total_conversions / campaign.total_clicks * 100
    roi = campaign.roi()

    # Простая формула для оценки
    score = (conversion_rate * 0.5) + (roi * 0.5)
    return score
