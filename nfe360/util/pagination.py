from nfe360.models.nfe import Nfe
from flask_paginate import Pagination


def paginate(page: int, data_list: list[Nfe]) -> tuple[Pagination, list[Nfe]]:
        
        if not isinstance(data_list, list) or not isinstance(data_list[0], Nfe):
            raise ValueError('Nenhum dado encontrado no banco')
        
        ITEMS_PER_PAGE = 5
        start_idx: int = (page - 1) * ITEMS_PER_PAGE
        end_idx: int = start_idx + ITEMS_PER_PAGE
        paginated_data_list: list[Nfe] = data_list[start_idx:end_idx]

        pagination = Pagination(
            page=page, total=len(data_list), 
            per_page=ITEMS_PER_PAGE, bs_version=4
        )
        
        return (pagination, paginated_data_list,)