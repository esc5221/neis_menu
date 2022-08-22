from typing import List

from ninja import Router
from ninja.pagination import paginate
from ninja.responses import codes_4xx

from common.schemas import ResponseDetailDTO

from schools.schemas import SchoolDTO, SchoolListDTO, SchoolPostParams
from schools.models import School
from schools.services import SchoolCreateService

router = Router(tags=["schools"])


@router.get("/{int:id}/", response=SchoolDTO)
# {int:id}를 붙여야 int가 아닌 url pattern이 인식됨.
def get_school(request, id: int):
    return School.objects.get_or_404(id=id)


@router.post("/", response={201: SchoolDTO, codes_4xx: ResponseDetailDTO})
def post_school(request, data: SchoolPostParams):
    response_code, result = SchoolCreateService(data)
    if response_code == 201:
        return response_code, result
    else:
        return response_code, {"detail": result}

@router.get("/", response=SchoolListDTO)
def list_schools(request):
    schools = School.objects.all()
    return SchoolListDTO(items=list(schools))


@router.get("/paged/", response=List[SchoolDTO])
@paginate
def paged_list_schools(request):
    schools = School.objects.all()
    return schools
