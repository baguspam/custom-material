from urllib import response
import odoo
from odoo import http, models, fields, _
from odoo.http import request, Response
import json
import requests
 
class ApiController(http.Controller):
    @http.route('/api/test/', type="http", auth='public', methods=['GET'], csrf=False)
    def get_sale(self, **kwargs):
        headers = {'Content-Type': 'application/json'}
        value = {
            'order_id': 'S0001',
            'customer': 'Agus Budianto',
            'total': 4000000
        }
        
        return Response(json.dumps(value), headers=headers)
    
    @http.route('/api/get_materials_bahan/', type="http", auth='public', methods=['GET'], csrf=False)
    def get_data_bahan(self, **kwargs): 
        try:    
            query_sql = "SELECT b.id, b.code, b.name, b.type, b.buy_price, b.supplier_id, s.name as supplier_name FROM materials_bahan as b \
                INNER JOIN materials_supplier as s ON b.supplier_id=s.id"
            request.env.cr.execute(query_sql)
            bahan = request.env.cr.dictfetchall()
            print(bahan)
            data = {
                'status':200,
                'error': False,
                'message': 'Success get data Bahan',
                'response': bahan
            }
            return Response(
                json.dumps(data),
                headers={'Content-Type': 'application/json'},
            )
        except :
            return Response(
                json.dumps({
                    'error': True,
                    'message' : 'Error Internal Server',
                }),
                headers={'Content-Type': 'application/json'},
            )
    
    @http.route('/api/create_materials_bahan/', type="http", auth='public', methods=['POST'], csrf=False)
    def get_data_post_bahan(self, **params):
        try:
            code = params.get('code','')
            name = params.get('name','')
            type = params.get('type','')
            type = params.get('type','')
            buy_price = params.get('buy_price','')
            supplier_id = params.get('supplier_id','')
            
            check_data = request.env['materials.bahan'].sudo().search([['code', '=', code]])

            if len(check_data) != 0:
                return Response(
                    json.dumps({
                    'error': True,
                    "message": {
                        "code": "Kode Bahan Sudah Ada"
                    }}),
                    headers={'Content-Type': 'application/json'},
                )

            with http.request.env.cr.savepoint():
                bahan = request.env['materials.bahan'].sudo().create({"code": code, "name": name, "type": type,
                                                                    "buy_price": buy_price,"supplier_id": supplier_id})
                return Response(
                    json.dumps({
                        'error': False,
                        'message' : 'Data bahan berhasil ditambahkan',
                    }),
                    headers={'Content-Type': 'application/json'},
                )
        except:
            return Response(
                json.dumps({
                    'error': True,
                    'message' : 'Error Internal Server',
                }),
                headers={'Content-Type': 'application/json'},
            )
    
    @http.route('/api/update_materials_bahan/', type="http", auth='public', methods=['POST'], csrf=False)
    def update_data_bahan(self, **params):
        try:
            id = params.get('id','')
            code = params.get('code','')
            name = params.get('name','')
            type = params.get('type','')
            type = params.get('type','')
            buy_price = params.get('buy_price','')
            supplier_id = params.get('supplier_id','')
            
            bahan_data = request.env['materials.bahan'].sudo().search([['id', '=', id]])
            if len(bahan_data) == 0:
                return Response(
                    json.dumps({
                        'error': True,
                        'message' : 'Id Tidak Ada',
                    }),
                    headers={'Content-Type': 'application/json'},
                )
            else:
                if len(code)==0:
                    bahan = bahan_data.sudo().write({"name": name, "type": type,
                                                                            "buy_price": buy_price,"supplier_id": supplier_id})
                else :
                    bahan_code = request.env['materials.bahan'].sudo().search([['code', '=', code]])
                    if len(bahan_code) == 0:
                        bahan = bahan_data.sudo().write({"code": code, "name": name, "type": type,
                                                                        "buy_price": buy_price,"supplier_id": supplier_id})
                    else:
                        return Response(
                            json.dumps({
                                'error': True,
                                'message' : 'Kode sudah digunakan',
                            }),
                            headers={'Content-Type': 'application/json'},
                        )
                        
                return Response(
                    json.dumps({
                        'error': False,
                        'message' : 'Data bahan berhasil diupdate',
                    }),
                    headers={'Content-Type': 'application/json'},
                )
        except:
            return Response(
                json.dumps({
                    'error': True,
                    'message' : 'Error Internal Server',
                }),
                headers={'Content-Type': 'application/json'},
            )
            
    @http.route('/api/delete_materials_bahan/<int:id>/', ype="http", auth='public', methods=['GET'], csrf=False)
    def delete_materials_bahan(self,id):
        try:
            bahan = request.env['materials.bahan'].sudo().search([['id', '=', id]])
            bahan.unlink()
            return Response(
                json.dumps({
                    'error': False,
                    'message' : 'Data bahan berhasil dihapus',
                }),
                headers={'Content-Type': 'application/json'},
            )
        except:
            return Response(
                json.dumps({
                    'error': True,
                    'message' : 'Id salah atau tidak ada',
                }),
                headers={'Content-Type': 'application/json'},
            )
            
    @http.route('/api/get_materials_supplier/', type="http", auth='public', methods=['GET'], csrf=False)
    def get_data_supplier(self, **kwargs): 
        try:    
            query_sql = "SELECT name, address FROM materials_supplier ORDER BY id"
            request.env.cr.execute(query_sql)
            bahan = request.env.cr.dictfetchall()
            print(bahan)
            data = {
                'status':200,
                'error': False,
                'message': 'Success get data supplier',
                'response': bahan
            }
            return Response(
                status=200,
                content_type='application/json; charset=utf-8',
                response=json.dumps(data)
            )
        except :
            return Response(
                status=200,
                content_type='application/json; charset=utf-8',
                header =[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': True,
                    'message' : 'Error Internal Server',
                })
            )
        