# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Julius Network Solutions SARL <contact@julius.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from osv import osv,fields
from tools.translate import _

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def start_acquisition(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        active = self.browse(cr, uid, ids[0])
        name = active.name
        action_context = {'default_type': 'order', 'default_name': 'Preparation ' + name, 'default_picking_id': ids[0]}
        address_id = active.address_id and active.address_id.id or False
        if address_id:
            action_context.update({'default_address_id': address_id})
        location_id = False
        for move in active.move_lines:
            location_id = move.location_dest_id and move.location_dest_id.id or False
            if location_id:
                action_context.update({'default_destination_id': location_id})
                break
        action = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'acquisition.acquisition',
            'view_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock_barcode_reader', 'view_stock_tracking_acquisition_form')[1],
#            'menu_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'menu_stock_root')[1],
            'context': action_context
        }
        return action

stock_picking()

#######################################stock_barcode_reader##############################################
#class stock_move(osv.osv):
#    _inherit = 'stock.move'
#    _columns = {
#         'move_ori_id': fields.many2one('stock.move', 'Origin Move', select=True),
#    }
#
#    def write(self, cr, uid, ids, vals, context=None):
#        result = super(stock_move,self).write(cr, uid, ids, vals, context=context)
#        if not isinstance(ids, list):
#            ids = [ids]
#        for id in ids:
#            state = self.browse(cr, uid, id, context=context).state
#            move_ori_id = self.browse(cr, uid, id, context=context).move_ori_id
#            if state == 'done' and move_ori_id:
#                self.write(cr, uid, [move_ori_id.id], {'state':'done'}, context=context)
#        return result
#
#    def create(self, cr, uid, vals, context=None):
#        production_lot_obj = self.pool.get('stock.production.lot')
#        stock_tracking_obj = self.pool.get('stock.tracking')
#        if vals.get('prodlot_id',False):
#            production_lot_data = production_lot_obj.browse(cr, uid, vals['prodlot_id'], context=context)
#            last_production_lot_move_id = self.search(cr, uid, [('prodlot_id', '=', production_lot_data.id)], limit=1, order='date', context=context)
#            if last_production_lot_move_id:
#                last_production_lot_move = self.browse(cr,uid,last_production_lot_move_id[0])
#                if last_production_lot_move.tracking_id:
#                    ids = [last_production_lot_move.tracking_id.id]
#                    stock_tracking_obj.reset_open(cr, uid, ids, context=context)
#
#        return super(stock_move,self).create(cr, uid, vals, context=context)
#
#stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
