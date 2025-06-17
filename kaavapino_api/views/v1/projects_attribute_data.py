from django.http.response import (
    HttpResponseForbidden
)
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    HttpResponse, JsonResponse
)
import logging
import csv
from kaavapino_api.views.serializers.v1 import ProjectV1Serializer
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient
from django.core.cache import cache
from openpyxl import Workbook
from datetime import date

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ProjectV1Serializer

    def get(self, request):
        def get_indexed_identifiers(all_data):
            attribute_data_keys = set()
            for project_name, data in all_data.items():
                for key in data.keys():
                    if key not in ["Projektin nimi", "Pinonumero (projektinumero)"]:
                        attribute_data_keys.add(key)

            indexed_dict = {i: o for i, o in enumerate(attribute_data_keys, start=2)}
            indexed_dict[0] = "Pinonumero (projektinumero)"
            indexed_dict[1] = "Projektin nimi"
            return dict(sorted(indexed_dict.items()))

        if not request.auth:
            return HttpResponse(status=401)

        response_type = request.query_params.get('response_type', "xlsx")
        pino_number = request.query_params.get('pino_number', None)
        pino_number = pino_number.split(",") if pino_number is not None and "," in pino_number else [pino_number] if pino_number else None

        kaavapino_creds = request.auth.access_kaavapino
        if not kaavapino_creds:
            return HttpResponseForbidden("No access!")

        self.client = KaavapinoClient(api_key=kaavapino_creds.credential)

        pino_numbers = pino_number or self.client.get_project_pino_numbers()
        all_data = {}
        for pino_number in pino_numbers:
            cache_key = f'kaavapino_project_{pino_number}'

            project_data = cache.get(cache_key)
            if project_data is None:
                project_data = self.client.get_project_attribute_data_filtered(pino_number)
                cache.set(cache_key, project_data, 60 * 60)  # 15 minutes
            all_data[project_data["Projektin nimi"]] = project_data

        if response_type == "csv":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f"attachment; filename={date.today()}-kaavapino_projects.csv"
            writer = csv.writer(response)

            identifiers_by_index = get_indexed_identifiers(all_data)
            writer.writerow(identifiers_by_index.values())
            rows = []
            for project_data in all_data.values():
                rows.append([str(project_data.get(key, "")) for key in identifiers_by_index.values()])
            writer.writerows(rows)
            return response
        elif response_type == "xlsx":
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f"attachment; filename={date.today()}-kaavapino_projects.xlsx"
            workbook = Workbook()
            sheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])

            identifiers_by_index = get_indexed_identifiers(all_data)
            sheet.append(list(identifiers_by_index.values()))
            for project_data in all_data.values():
                sheet.append([str(project_data.get(key, "")) for key in identifiers_by_index.values()])
            workbook.save(response)
            return response
        else:
            return JsonResponse(all_data)
