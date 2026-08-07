from typing import Any

from django.http import HttpRequest
from inertia import render as inertia_render
from pydantic import BaseModel


def render_inertia_from_dto(
    request: HttpRequest,
    component: str,
    props: BaseModel,
    **kwargs: Any,
) -> Any:
    """Рендерит Inertia-компонент, используя Pydantic DTO.

    DTO сериализуется через ``model_dump(mode="json")`` и передается
    в Inertia в качестве props.

    По соглашению DTO размещаются в директории ``dto/`` каждого приложения.

    Пример:
        dto = ChannelListDTO(...)

        return render_inertia_from_dto(
            request,
            "ChannelAnalytics",
            props=dto,
        )
    """
    return inertia_render(
        request,
        component,
        props=props.model_dump(mode="json"),
        **kwargs,
    )
