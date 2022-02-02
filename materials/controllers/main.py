import math
from odoo import http
from odoo.http import request

class CustomWebsiteMaterials(http.Controller):
    @http.route('/bahans', type='http', auth="public", website=True, sitemap=True)
    def web_materials(self, **kwargs):
        search_query = []
        slug_param = '?'
        page_limit = 5
        type_by = kwargs.get('typeby', '')
        page_number = kwargs.get('page', '1')
        
        if len(type_by) != 0:
            search_query.append(('type', '=', type_by))
            slug_param = '?typeby='+type_by+'&'
        
        if page_number.isdigit():
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1
        else:
            page_number = 1
        offset = (page_number - 1) * page_limit
        
        bahan_sql = request.env['materials.bahan'].sudo()
        bahan = bahan_sql.search(search_query, offset=offset,  limit=page_limit)
        
        item_count = len(bahan)
        total_item_count = bahan_sql.search_count(search_query)
        
        max_page_index = math.ceil(total_item_count / page_limit)

        page_displays = []
        for oix in range(5):
            oix = page_number + oix - 2
            if oix > 0 and oix <= max_page_index:
                page_displays.append(oix)

        if 1 not in page_displays:
            if len(page_displays) > 4:
                page_displays[0] = 1
            else:
                page_displays.insert(0, 1)
        if max_page_index not in page_displays:
            if len(page_displays) > 4:
                page_displays[len(page_displays)-1] = max_page_index
            else:
                page_displays.append(max_page_index)
        if item_count < page_limit:
            next_page_index = 0
        else:
            next_page_index = page_number + 1
        
        if page_number > 1:
            prev_page_index = page_number - 1
        else:
            prev_page_index = 0
        
        value = {
            'bahans': bahan,
            'next_page_index': next_page_index,
            'prev_page_index': prev_page_index,
            'page_displays': page_displays,
            'page_number': page_number,
            'slug_param': slug_param,
        }
        
        return request.render("materials.website_materials_template", value)
