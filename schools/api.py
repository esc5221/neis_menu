from typing import List

from ninja import Router
from ninja.pagination import paginate


from schools.schemas import SchoolDTO, SchoolListDTO
from schools.models import School

router = Router(tags=["schools"])


@router.get("/{int:id}/", response=SchoolDTO)
# {int:id}를 붙여야 int가 아닌 url pattern이 인식됨.
def get_school(request, id: int):
    return School.objects.get_or_404(id=id)


@router.get("/", response=SchoolListDTO)
def list_schools(request):
    schools = School.objects.all()
    return SchoolListDTO(objects=list(schools))


@router.get("/paged/", response=List[SchoolDTO])
@paginate
def paged_list_schools(request):
    schools = School.objects.all()
    return schools
